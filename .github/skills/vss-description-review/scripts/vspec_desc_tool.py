#!/usr/bin/env -S uv run --script
# Copyright (c) 2026 Contributors to COVESA
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License 2.0 which is available at
# https://www.mozilla.org/en-US/MPL/2.0/
#
# SPDX-License-Identifier: MPL-2.0
#
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0.2"]
# ///
"""Print VSS data entries of `*.vspec` files as JSON and write edited description/comment fields back.

Commands:

  scan   Print one JSON object per data entry: file, line, type, datatype, description, comment, allowed
         values, nearest parent entry, and rule_flags (boolean casing, allowed-value casing, sentence count,
         instance names in the description, missing description).

  apply  Read a JSON array of edits and rewrite the named entries in place. An edit sets `description` and/or
         `comment`, or adds a `# Human check of description required: <reason>` comment above the entry
         (`flag`). Only the affected fields are replaced; the rest of the file stays unchanged.

  status Show or record which files have been reviewed, in review-status.json next to the skill.

The tool only reads and writes files in the working tree. It does not run git or access the network.

Usage:
    uv run vspec_desc_tool.py scan [path-or-glob ...] > entries.jsonl
    uv run vspec_desc_tool.py apply edits.json
    uv run vspec_desc_tool.py status [list]
    uv run vspec_desc_tool.py status mark <file> --model "<model name>" [--flags-open N] [--pr <url>]
"""
import datetime as dt
import json
import re
import sys
import textwrap
from pathlib import Path
from typing import Any, NamedTuple

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_GLOB = "spec/**/*.vspec"
STATUS_FILE = Path(__file__).resolve().parent.parent / "review-status.json"
MAX_LINE_LENGTH = 120

FLAG_PREFIX = "# Human check of description required"
INSTANCE_RANGE_RE = re.compile(r"^(\w*)\[(\d+),\s*(\d+)\]$")


class Entry(NamedTuple):
    """A top-level vspec entry. Line indexes are 0-based and `end` is exclusive."""

    name: str
    start: int
    end: int
    fields: dict[str, Any]
    extents: dict[str, tuple[int, int]]  # field name -> (start, end) lines


class Catalog(NamedTuple):
    # Entry name -> one record per file defining it.
    index: dict[str, list[dict[str, Any]]]
    # Instance names declared via `instances:` anywhere in the catalog, e.g. Left, Row1.
    instance_names: set[str]


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def _trim_trailing(lines: list[str], start: int, end: int, comments_too: bool) -> int:
    while end - 1 > start and (
        lines[end - 1].strip() == "" or (comments_too and lines[end - 1].lstrip().startswith("#"))
    ):
        end -= 1
    return end


def parse_entries(lines: list[str]) -> list[Entry]:
    """Parse vspec lines with PyYAML and return the top-level entries."""
    loader = yaml.SafeLoader("\n".join(lines) + "\n")
    try:
        root = loader.get_single_node()
        if not isinstance(root, yaml.MappingNode):
            return []
        top = root.value
        entries = []
        for idx, (key_node, value_node) in enumerate(top):
            start = key_node.start_mark.line
            next_start = top[idx + 1][0].start_mark.line if idx + 1 < len(top) else len(lines)
            end = _trim_trailing(lines, start, next_start, comments_too=True)
            fields: dict[str, Any] = {}
            extents: dict[str, tuple[int, int]] = {}
            if isinstance(value_node, yaml.MappingNode):
                for field_key, field_value in value_node.value:
                    name = field_key.value
                    fields[name] = loader.construct_object(field_value, deep=True)
                    field_start = field_key.start_mark.line
                    field_end = field_value.end_mark.line + (1 if field_value.end_mark.column > 0 else 0)
                    field_end = _trim_trailing(lines, field_start, min(field_end, end), comments_too=False)
                    extents[name] = (field_start, max(field_end, field_start + 1))
            entries.append(Entry(key_node.value, start, end, fields, extents))
        return entries
    finally:
        loader.dispose()


def find_entry(lines: list[str], entry_name: str) -> Entry | None:
    for entry in parse_entries(lines):
        if entry.name == entry_name:
            return entry
    return None


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def write_lines(path: Path, lines: list[str]) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")


def expand_instance(item: str) -> list[str]:
    """Expand a vspec instance declaration: `Row[1,3]` gives Row1, Row2, Row3; other names are kept."""
    match = INSTANCE_RANGE_RE.match(item.strip())
    if not match:
        return [item.strip()]
    prefix, low, high = match.group(1), int(match.group(2)), int(match.group(3))
    return [f"{prefix}{number}" for number in range(low, high + 1)]


def flatten_instances(raw: Any) -> list[str]:
    if isinstance(raw, str):
        return expand_instance(raw)
    if isinstance(raw, list):
        return [name for item in raw for name in flatten_instances(item)]
    return []


def build_catalog(glob_pattern: str = DEFAULT_GLOB) -> Catalog:
    index: dict[str, list[dict[str, Any]]] = {}
    instance_names: set[str] = set()
    for path in sorted(REPO_ROOT.glob(glob_pattern)):
        rel = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
        for entry in parse_entries(read_lines(path)):
            index.setdefault(entry.name, []).append({
                "file": rel,
                "type": entry.fields.get("type"),
                "description": entry.fields.get("description"),
                "comment": entry.fields.get("comment"),
            })
            instance_names.update(flatten_instances(entry.fields.get("instances")))
    return Catalog(index, instance_names)


def resolve_parent(
    entry_name: str, file_rel: str, index: dict[str, list[dict[str, Any]]]
) -> tuple[str | None, dict[str, Any] | None, list[str]]:
    """Walk up the dotted name to the nearest ancestor entry.

    Returns (name, info, ambiguous_files). A name defined in several files is resolved to the
    definition in the same file if there is one; otherwise it is reported as ambiguous instead of guessed.
    """
    parts = entry_name.split(".")
    for cut in range(len(parts) - 1, 0, -1):
        candidate = ".".join(parts[:cut])
        matches = index.get(candidate)
        if not matches:
            continue
        same_file = [m for m in matches if m["file"] == file_rel]
        if same_file:
            return candidate, same_file[0], []
        if len(matches) == 1:
            return candidate, matches[0], []
        return None, None, sorted(m["file"] for m in matches)
    return None, None, []


# ---------------------------------------------------------------------------
# scan
# ---------------------------------------------------------------------------

def allowed_values(fields: dict[str, Any]) -> list[str]:
    raw = fields.get("allowed") or fields.get("enum") or []
    if isinstance(raw, dict):
        raw = list(raw)
    return [str(value) for value in raw] if isinstance(raw, list) else []


def check_entry(fields: dict[str, Any], instance_names: set[str]) -> list[str]:
    flags = []
    desc = str(fields.get("description") or "")
    entry_type = fields.get("type", "")
    datatype = fields.get("datatype", "")

    if entry_type != "branch" and not desc:
        flags.append("missing_description")
        return flags  # nothing else to check without a description

    if datatype == "boolean":
        if re.search(r"\bTRUE\b|\bFALSE\b", desc):
            flags.append("boolean_casing:uppercase")
        if re.search(r"\btrue\b|\bfalse\b", desc):
            flags.append("boolean_casing:lowercase")
        if not re.search(r"\bTrue\b", desc) or not re.search(r"\bFalse\b", desc):
            flags.append("boolean_missing_true_false")

    for value in allowed_values(fields):
        if not re.fullmatch(r"[A-Z0-9_]+", value) or len(value) < 3:
            continue  # too short to word-match reliably (e.g. single-letter engine shapes 'V', 'W')
        if re.search(rf"\b{re.escape(value.lower())}\b", desc.lower()) and value not in desc:
            flags.append(f"value_casing:{value}")

    if len(re.findall(r"\.(?:\s|$)", desc)) > 3:
        flags.append("too_many_sentences")

    for name in sorted(instance_names):
        if re.search(rf"\b{re.escape(name)}\b", desc):
            flags.append(f"possible_instance_reference:{name}")

    return sorted(set(flags))


def scan(paths: list[Path]) -> None:
    catalog = build_catalog()
    for path in paths:
        rel = path.relative_to(REPO_ROOT) if path.is_absolute() else path
        rel_str = str(rel).replace("\\", "/")
        is_template = rel_str.startswith("spec/include/")
        for entry in parse_entries(read_lines(path)):
            fields = entry.fields
            parent_name, parent_info, ambiguous = resolve_parent(entry.name, rel_str, catalog.index)
            record = {
                "file": rel_str,
                "entry": entry.name,
                "line": entry.start + 1,
                "type": fields.get("type"),
                "datatype": fields.get("datatype"),
                "description": fields.get("description"),
                "comment": fields.get("comment"),
                "allowed": allowed_values(fields) or None,
                "parent": parent_name,
                "parent_description": parent_info["description"] if parent_info else None,
                "parent_comment": parent_info["comment"] if parent_info else None,
                # spec/include/*.vspec entries are reusable templates applied to many
                # different parents via '#include ... <Prefix>' - they must stay generic,
                # NOT fold in the meaning of whichever single parent happens to be resolved above.
                "reusable_include_template": is_template,
                "rule_flags": check_entry(fields, catalog.instance_names),
            }
            if ambiguous:
                record["parent_ambiguous_in"] = ambiguous
            print(json.dumps(record))


# ---------------------------------------------------------------------------
# apply
# ---------------------------------------------------------------------------

def render_field(key: str, value: str) -> list[str]:
    """Render a 2-space indented YAML field; long text becomes a folded block scalar (>-).

    PyYAML decides the quoting, so special characters such as ': ' can never corrupt the file.
    The block form is re-parsed and must round-trip to the exact same string.
    """
    flat = yaml.safe_dump({key: value}, default_flow_style=False, width=10 ** 6, allow_unicode=True).rstrip("\n")
    flat = "  " + flat
    if len(flat) <= MAX_LINE_LENGTH and "\n" not in flat:
        return [flat]
    if "\n" in value:
        block = [f"  {key}: |-"] + [f"    {line}".rstrip() for line in value.split("\n")]
    else:
        wrapped = textwrap.wrap(value, width=MAX_LINE_LENGTH - 4, break_long_words=False, break_on_hyphens=False)
        block = [f"  {key}: >-"] + [f"    {line}" for line in wrapped]
    if yaml.safe_load("\n".join(block)).get(key) == value:
        return block
    return flat.split("\n")


def set_field(lines: list[str], entry: Entry, key: str, value: str) -> None:
    rendered = render_field(key, value.strip())
    if key in entry.extents:
        start, end = entry.extents[key]
        lines[start:end] = rendered
        return
    insert_at = entry.extents["description"][1] if "description" in entry.extents else entry.end
    lines[insert_at:insert_at] = rendered


def add_flag(lines: list[str], entry: Entry, reason: str) -> None:
    start = entry.start
    if start > 0 and lines[start - 1].strip().startswith(FLAG_PREFIX):
        lines[start - 1] = f"{FLAG_PREFIX}: {reason}"
        return
    lines.insert(start, f"{FLAG_PREFIX}: {reason}")


def apply_edits(edits_path: str) -> None:
    edits = json.loads(Path(edits_path).read_text(encoding="utf-8-sig"))
    by_file: dict[str, list[dict[str, str]]] = {}
    for edit in edits:
        by_file.setdefault(edit["file"], []).append(edit)

    applied = 0
    skipped = []
    for file_rel, file_edits in by_file.items():
        path = REPO_ROOT / file_rel
        lines = read_lines(path)
        for edit in file_edits:
            if find_entry(lines, edit["entry"]) is None:
                skipped.append(edit)
                continue
            # Re-parse after every change so line numbers are always fresh.
            for key in ("description", "comment"):
                if key in edit:
                    set_field(lines, find_entry(lines, edit["entry"]), key, edit[key])
            if "flag" in edit:
                add_flag(lines, find_entry(lines, edit["entry"]), edit["flag"])
            applied += 1
        write_lines(path, lines)

    print(f"Applied {applied} edit(s).", file=sys.stderr)
    if skipped:
        print(f"Skipped {len(skipped)} edit(s), entry not found:", file=sys.stderr)
        for edit in skipped:
            print(f"  {edit['file']}: {edit['entry']}", file=sys.stderr)


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

def load_status() -> dict[str, dict[str, Any]]:
    if STATUS_FILE.exists():
        return json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    return {}


def save_status(data: dict[str, dict[str, Any]]) -> None:
    STATUS_FILE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def status_mark(file_rel: str, model: str, flags_open: int, pr: str | None = None) -> None:
    data = load_status()
    data[file_rel] = {
        "reviewed_at": dt.date.today().isoformat(),
        "model": model,
        "flags_open": flags_open,
        "pr": pr,
    }
    save_status(data)
    print(f"Marked {file_rel} as reviewed (model={model}, flags_open={flags_open}, pr={pr}).", file=sys.stderr)


def status_list() -> None:
    data = load_status()
    all_files = sorted(
        str(p.relative_to(REPO_ROOT)).replace("\\", "/") for p in REPO_ROOT.glob(DEFAULT_GLOB)
    )
    for file_rel in all_files:
        entry = data.get(file_rel)
        if entry:
            pr_suffix = f", {entry['pr']}" if entry.get("pr") else ""
            flags_open = entry.get("flags_open", "?")
            print(f"[x] {file_rel}  (reviewed {entry['reviewed_at']} by {entry['model']}, "
                  f"open flags: {flags_open}{pr_suffix})")
        else:
            print(f"[ ] {file_rel}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def resolve_paths(args: list[str]) -> list[Path]:
    if not args:
        return sorted(REPO_ROOT.glob(DEFAULT_GLOB))
    paths: list[Path] = []
    for arg in args:
        path = Path(arg)
        if path.is_absolute() and path.is_file():
            paths.append(path)
        elif path.is_file():
            paths.append((REPO_ROOT / path) if not path.exists() else path)
        else:
            paths.extend(sorted(REPO_ROOT.glob(arg)))
    return paths


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("scan", "apply", "status"):
        print(__doc__)
        sys.exit(1)
    command = sys.argv[1]
    if command == "scan":
        scan(resolve_paths(sys.argv[2:]))
    elif command == "apply":
        if len(sys.argv) < 3:
            print("usage: vspec_desc_tool.py apply edits.json", file=sys.stderr)
            sys.exit(1)
        apply_edits(sys.argv[2])
    elif command == "status":
        rest = sys.argv[2:]
        status_usage = "usage: vspec_desc_tool.py status mark <file> --model <name> [--flags-open N] [--pr <url>]"
        if rest and rest[0] == "mark":
            args = rest[1:]
            if not args:
                print(status_usage, file=sys.stderr)
                sys.exit(1)
            file_rel, opts = args[0], args[1:]
            model: str | None = None
            flags_open = 0
            pr: str | None = None
            it = iter(opts)
            for opt in it:
                if opt == "--model":
                    model = next(it, None)
                elif opt == "--flags-open":
                    flags_open = int(next(it, 0))
                elif opt == "--pr":
                    pr = next(it, None)
            if not model:
                print(status_usage, file=sys.stderr)
                sys.exit(1)
            status_mark(file_rel, model, flags_open, pr)
        else:
            status_list()


if __name__ == "__main__":
    main()
