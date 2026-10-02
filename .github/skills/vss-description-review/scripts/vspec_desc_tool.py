#!/usr/bin/env python3
"""Deterministic helper for the vss-description-review skill (stdlib only, no deps).

Replaces the "read every .vspec file by hand" and "hand-craft one string-replace per
entry" parts of the review with scriptable passes:

  scan   - parse spec/**/*.vspec and emit one JSON object per data entry (its
           description/comment/type/datatype/allowed/enum, a 'line' number, and
           the immediate parent branch's description/comment for self-containment
           checks), plus mechanically-detectable rule_flags (boolean casing,
           value-list casing, sentence count, possible instance-name leakage,
           missing description). This is the input an LLM should reason over
           instead of re-reading raw files.

  apply  - take a JSON array of edit directives (produced after reasoning over
           the scan output) and rewrite the files: set description/comment on a
           named entry, or insert a "Human check of description required" flag
           comment above it. Entries are located by exact dotted name on every
           single edit, so ordering of the input array never matters.

  status - track which .vspec files have already been reviewed, in
           review-status.json next to this skill, so repeated full-catalog
           sweeps don't redo work already covered by a merged PR.

vspec data entries are flat top-level keys (e.g. "Trunk.AbsoluteVolume:") with a
2-space-indented field block, so a lightweight line parser is enough - no YAML
library or vss-tools install required.

Usage:
    python vspec_desc_tool.py scan [path-or-glob ...] > entries.jsonl
    python vspec_desc_tool.py apply edits.json
    python vspec_desc_tool.py status [list]
    python vspec_desc_tool.py status mark <file> --model "<model name>" [--flags-open N] [--pr <url>]
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_GLOB = "spec/**/*.vspec"
STATUS_FILE = Path(__file__).resolve().parent.parent / "review-status.json"

ENTRY_RE = re.compile(r"^([A-Za-z][\w.]*):\s*$")
FIELD_RE = re.compile(r"^  (\w+):\s?(.*)$")
FLAG_PREFIX = "# Human check of description required"

# Conservative instance-name markers from docs-gen/content/rule_set/data_entry/description.md
INSTANCE_WORD_RE = re.compile(
    r"\b(left|right|driver|passenger|front|rear|center|row\d|pos\d)\b", re.IGNORECASE
)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def iter_entries(lines):
    """Yield (name, start_line_1based, end_line_exclusive, fields) for each top-level entry."""
    i, n = 0, len(lines)
    while i < n:
        m = ENTRY_RE.match(lines[i])
        if not m:
            i += 1
            continue
        name = m.group(1)
        start = i
        i += 1
        fields = {}
        while i < n:
            line = lines[i]
            if line.strip() == "" or line.lstrip().startswith("#"):
                i += 1
                continue
            if not line.startswith("  "):
                break
            fm = FIELD_RE.match(line)
            if not fm:
                i += 1
                continue
            key, val = fm.group(1), fm.group(2)
            j = i + 1
            extra = []
            while j < n and lines[j].strip() != "" and lines[j].startswith("  ") and not FIELD_RE.match(lines[j]):
                extra.append(lines[j].strip())
                j += 1
            if extra:
                val = (val + " " + " ".join(extra)).strip()
                i = j
            else:
                i += 1
            fields[key] = val
        yield name, start + 1, i, fields  # 1-based start line, exclusive end index


def find_entry(lines, entry_name):
    for name, start_1based, end, fields in iter_entries(lines):
        if name == entry_name:
            return start_1based - 1, end, fields  # 0-based start index
    return None


def build_index(glob_pattern=DEFAULT_GLOB):
    """Map every entry name in the catalog to its file/description/comment, for parent lookups."""
    index = {}
    for path in sorted(REPO_ROOT.glob(glob_pattern)):
        rel = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
        lines = path.read_text(encoding="utf-8").splitlines()
        for name, _start, _end, fields in iter_entries(lines):
            index[name] = {
                "file": rel,
                "type": fields.get("type"),
                "description": fields.get("description"),
                "comment": fields.get("comment"),
            }
    return index


def resolve_parent(entry_name, index):
    """Walk up the dotted name to the nearest ancestor that exists as its own entry."""
    parts = entry_name.split(".")
    for cut in range(len(parts) - 1, 0, -1):
        candidate = ".".join(parts[:cut])
        if candidate in index:
            return candidate, index[candidate]
    return None, None


# ---------------------------------------------------------------------------
# scan
# ---------------------------------------------------------------------------

def check_entry(fields):
    flags = []
    desc = fields.get("description", "")
    etype = fields.get("type", "")
    datatype = fields.get("datatype", "")
    allowed = fields.get("allowed", "") or fields.get("enum", "")

    if etype != "branch" and not desc:
        flags.append("missing_description")
        return flags  # nothing else to check without a description

    if datatype == "boolean":
        if re.search(r"\bTRUE\b|\bFALSE\b", desc):
            flags.append("boolean_casing:uppercase")
        if re.search(r"\btrue\b|\bfalse\b", desc):
            flags.append("boolean_casing:lowercase")
        if not re.search(r"\bTrue\b", desc) or not re.search(r"\bFalse\b", desc):
            flags.append("boolean_missing_true_false")

    if allowed:
        for value in re.findall(r"['\"]([A-Z0-9_]+)['\"]", allowed):
            if len(value) < 3:
                continue  # too short to word-match reliably (e.g. single-letter engine shapes 'V', 'W')
            if re.search(rf"\b{re.escape(value.lower())}\b", desc.lower()) and value not in desc:
                flags.append(f"value_casing:{value}")

    sentence_count = len(re.findall(r"\.(?:\s|$)", desc))
    if sentence_count > 3:
        flags.append("too_many_sentences")

    for match in INSTANCE_WORD_RE.finditer(desc):
        flags.append(f"possible_instance_reference:{match.group(1).lower()}")

    return sorted(set(flags))


def scan(paths):
    index = build_index()
    for path in paths:
        rel = path.relative_to(REPO_ROOT) if path.is_absolute() else path
        rel_str = str(rel).replace("\\", "/")
        is_template = rel_str.startswith("spec/include/")
        lines = path.read_text(encoding="utf-8").splitlines()
        for name, start_line, _end, fields in iter_entries(lines):
            parent_name, parent_info = resolve_parent(name, index)
            record = {
                "file": rel_str,
                "entry": name,
                "line": start_line,
                "type": fields.get("type"),
                "datatype": fields.get("datatype"),
                "description": fields.get("description"),
                "comment": fields.get("comment"),
                "allowed": fields.get("allowed") or fields.get("enum"),
                "parent": parent_name,
                "parent_description": parent_info["description"] if parent_info else None,
                "parent_comment": parent_info["comment"] if parent_info else None,
                # spec/include/*.vspec entries are reusable templates applied to many
                # different parents via '#include ... <Prefix>' - they must stay generic,
                # NOT fold in the meaning of whichever single parent happens to be resolved above.
                "reusable_include_template": is_template,
                "rule_flags": check_entry(fields),
            }
            print(json.dumps(record))


# ---------------------------------------------------------------------------
# apply
# ---------------------------------------------------------------------------

def field_extent(lines, field_line, block_end):
    """Return the exclusive end index of a field's value, including folded continuation lines
    (mirrors the continuation-consuming logic in iter_entries - a multi-line description/comment
    must have ALL of its lines removed when rewritten, not just the first, or the stale
    continuation text would silently fold into the new YAML scalar)."""
    j = field_line + 1
    while j < block_end and lines[j].strip() != "" and lines[j].startswith("  ") and not FIELD_RE.match(lines[j]):
        j += 1
    return j


def set_field(lines, start, end, key, value):
    pattern = re.compile(rf"^  {re.escape(key)}:")
    for i in range(start + 1, end):
        if pattern.match(lines[i]):
            field_end = field_extent(lines, i, end)
            lines[i:field_end] = [f"  {key}: {value}"]
            return
    insert_at = end
    for i in range(start + 1, end):
        if lines[i].startswith("  description:"):
            insert_at = field_extent(lines, i, end)
            break
    lines.insert(insert_at, f"  {key}: {value}")


def add_flag(lines, start, reason):
    if start > 0 and lines[start - 1].strip().startswith(FLAG_PREFIX):
        indent = lines[start - 1][: len(lines[start - 1]) - len(lines[start - 1].lstrip())]
        lines[start - 1] = f"{indent}{FLAG_PREFIX}: {reason}"
        return
    indent = lines[start][: len(lines[start]) - len(lines[start].lstrip())]
    lines.insert(start, f"{indent}{FLAG_PREFIX}: {reason}")


def apply_edits(edits_path):
    edits = json.loads(Path(edits_path).read_text(encoding="utf-8"))
    by_file = {}
    for edit in edits:
        by_file.setdefault(edit["file"], []).append(edit)

    applied, skipped = 0, []
    for file_rel, file_edits in by_file.items():
        path = REPO_ROOT / file_rel
        lines = path.read_text(encoding="utf-8").splitlines()
        for edit in file_edits:
            found = find_entry(lines, edit["entry"])
            if found is None:
                skipped.append(edit)
                continue
            start, end, _fields = found
            if "description" in edit:
                set_field(lines, start, end, "description", edit["description"])
                found = find_entry(lines, edit["entry"])
                start, end, _fields = found
            if "comment" in edit:
                set_field(lines, start, end, "comment", edit["comment"])
                found = find_entry(lines, edit["entry"])
                start, end, _fields = found
            if "flag" in edit:
                add_flag(lines, start, edit["flag"])
            applied += 1
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Applied {applied} edit(s).", file=sys.stderr)
    if skipped:
        print(f"Skipped {len(skipped)} edit(s), entry not found:", file=sys.stderr)
        for edit in skipped:
            print(f"  {edit['file']}: {edit['entry']}", file=sys.stderr)


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

def load_status():
    if STATUS_FILE.exists():
        return json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    return {}


def save_status(data):
    STATUS_FILE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def status_mark(file_rel, model, flags_open, pr=None):
    data = load_status()
    data[file_rel] = {
        "reviewed_at": dt.date.today().isoformat(),
        "model": model,
        "flags_open": flags_open,
        "pr": pr,
    }
    save_status(data)
    print(f"Marked {file_rel} as reviewed (model={model}, flags_open={flags_open}, pr={pr}).", file=sys.stderr)


def status_list():
    data = load_status()
    all_files = sorted(
        str(p.relative_to(REPO_ROOT)).replace("\\", "/") for p in REPO_ROOT.glob(DEFAULT_GLOB)
    )
    for f in all_files:
        entry = data.get(f)
        if entry:
            pr_suffix = f", {entry['pr']}" if entry.get("pr") else ""
            print(f"[x] {f}  (reviewed {entry['reviewed_at']} by {entry['model']}, open flags: {entry.get('flags_open', '?')}{pr_suffix})")
        else:
            print(f"[ ] {f}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def resolve_paths(args):
    if not args:
        return sorted(REPO_ROOT.glob(DEFAULT_GLOB))
    paths = []
    for arg in args:
        p = Path(arg)
        if p.is_absolute() and p.is_file():
            paths.append(p)
        elif p.is_file():
            paths.append((REPO_ROOT / p) if not p.exists() else p)
        else:
            paths.extend(sorted(REPO_ROOT.glob(arg)))
    return paths


def main():
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
        if rest and rest[0] == "mark":
            args = rest[1:]
            if not args:
                print("usage: vspec_desc_tool.py status mark <file> --model <name> [--flags-open N] [--pr <url>]", file=sys.stderr)
                sys.exit(1)
            file_rel, opts = args[0], args[1:]
            model, flags_open, pr = None, 0, None
            it = iter(opts)
            for opt in it:
                if opt == "--model":
                    model = next(it, None)
                elif opt == "--flags-open":
                    flags_open = int(next(it, 0))
                elif opt == "--pr":
                    pr = next(it, None)
            if not model:
                print("usage: vspec_desc_tool.py status mark <file> --model <name> [--flags-open N] [--pr <url>]", file=sys.stderr)
                sys.exit(1)
            status_mark(file_rel, model, flags_open, pr)
        else:
            status_list()


if __name__ == "__main__":
    main()
