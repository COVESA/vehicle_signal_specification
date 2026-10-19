---
name: vss-description-review
description: 'Review VSS data entries (branches, sensors, actuators, attributes) in `*.vspec` files, rewrite `description` and `comment` fields to comply with the description guidelines. Flags entries that are too vague. Use when: asked to review/update/unify/audit VSS descriptions, check a `vspec` file or branch for description guideline compliance, or review newly proposed/changed elements'
argument-hint: 'Optional: file(s)/path or branch to review; omit for a scoping discussion'
---

# VSS Description Review

Checks the `description:` and `comment:` fields of VSS data entries against the
[description guidelines](../../../docs-gen/content/rule_set/data_entry/description.md), then fixes them or flags them for a human.

## Boundaries — read first

This skill does **one thing**: review descriptions and edit `description`/`comment` in the **working tree**.
It never publishes anything. While running this skill you must **not**:

- create branches, commit, amend, or push,
- open or update pull requests or issues, or post PR/review comments (no GitHub write tools, no `gh pr ...`),
- edit anything other than `description`/`comment` text and `# Human check of description required` comments.

When finished, report the findings in the chat and leave the diff to the user, who reviews it and decides
what to commit and submit (see [CONTRIBUTING.md](../../../CONTRIBUTING.md)). If asked to commit, push or open a PR as well, say that this is
outside the skill and let the user do it.

The skill can serve as the description check of a `/review` task. When reviewing someone else's change,
only report findings in the chat; the human decides what to post.

## Prerequisites

[uv](https://docs.astral.sh/uv/) runs the helper script and installs its dependency (PyYAML) automatically,
so no manual setup is needed for the skill itself. To verify the result, install vss-tools, see
[BUILD.md](../../../BUILD.md) and [scripts/install_vss_tools.sh](../../../scripts/install_vss_tools.sh) (use a virtual environment).

## When to Use

- "Review/update/fix/unify descriptions in `spec/...`"
- "Check the new signals in my branch for description compliance"
- "Audit `Vehicle.X` for description guideline violations"

## Step 1 — Load the baseline

Always re-read [description.md](../../../docs-gen/content/rule_set/data_entry/description.md) first; it is the
single source of truth. Do not rely on a memorized copy of the rules, since this file changes over time.

## Step 2 — Determine scope

Ask if not already clear:

- **Specific file(s) or entries** given by the user → review those.
- **Changed or newly proposed elements** → diff against the target branch (e.g.
  `git diff upstream/master...HEAD -- 'spec/**/*.vspec'`) and review only the added/changed entries.
- **Whole catalog** → this touches dozens of files; confirm with the user before starting. Work through the files
  one at a time and report per file, so the user can review and commit them separately.
  `uv run .github/skills/vss-description-review/scripts/vspec_desc_tool.py status` lists the files recorded as
  reviewed (in `review-status.json`, created by `status mark`); skip those unless asked to re-review them.

## Step 3 — Scan instead of reading raw files

Run [scripts/vspec_desc_tool.py](./scripts/vspec_desc_tool.py) to get
a structured, pre-extracted dataset instead of grepping/reading every `.vspec` file by hand:

```
uv run .github/skills/vss-description-review/scripts/vspec_desc_tool.py scan [path-or-glob ...] > entries.jsonl
```

With no arguments it scans all of `spec/**/*.vspec`. Each output line is one JSON entry:
`file`, `entry` (dotted name), `line`, `type`, `datatype`, `description`, `comment`, `allowed`,
`parent`/`parent_description`/`parent_comment`, `reusable_include_template`, and `rule_flags` — a list of
mechanically-detectable issues (`missing_description`, `boolean_casing:*`, `boolean_missing_true_false`,
`value_casing:<VALUE>`, `too_many_sentences`, `possible_instance_reference:<name>` — an instance name declared
by `instances:` somewhere in the catalog). Reason over this JSONL,
not the original files — it contains the `description`/`comment` text already, so opening the `.vspec`
source is rarely needed.

**Branch-to-entity context is included automatically.** `parent`/`parent_description`/`parent_comment` are
the nearest ancestor entry resolved across the *entire* catalog (not just the file being scanned), so rule 3
(self-contained — fold in the parent's meaning) and the modular-branch rules can be applied directly from
the JSONL without a second lookup pass. Two caveats:

- If `reusable_include_template` is `true` (the entry lives under `spec/include/*.vspec`), it is a generic
  snippet reused by many different parents via `#include ... <Prefix>` — do **not** fold in whichever single
  `parent`/`parent_description` the index happened to resolve; keep the description generic instead.
- `parent` can be `null` for a root-level entry, or for a leaf whose real parent is only assembled at
  include-time (prefix added by the including file) rather than written as a literal dotted name anywhere —
  in that case fall back to reading the including file's `#include ... <Prefix>` line for context.
- If the nearest ancestor name is defined in several files (and not in the scanned file), `parent` is `null`
  and `parent_ambiguous_in` lists those files — look at the including file instead of guessing.

`rule_flags` only catches the mechanical rules. Still judge the semantic rules the script cannot check
(dictionary-style first sentence, self-containment, modular/loose branch wording) — but do this by reading
the compact JSONL fields (including `parent_description`), not the raw file.

## Step 4 — Classify and collect edits

For every in-scope entry, classify it and, instead of editing files directly, append one directive to a
single `edits.json` array (grouping is handled by the script):

- **Compliant** → no directive needed.
- **Fixable without domain guessing** (pure style: casing, padding, instance leakage, value-list placement,
  moving a long breakdown to `comment:`) → `{"file": ..., "entry": ..., "description": "...", "comment": "..."}`
  (omit whichever field is unchanged).
- **Vague or domain-ambiguous** (the correct meaning cannot be determined from the node name, siblings,
  existing `comment:`, or unit/datatype/allowed values) → **do not guess the text**. Add
  `{"file": ..., "entry": ..., "flag": "<short reason>"}` instead.

Never touch `datatype`, `unit`, `allowed`, `enum`, `min`/`max`, `instances`, or node names — only
`description`/`comment`/`flag` directives. Never flag-and-rewrite the same entry's existing `comment:` text
when its precise meaning is uncertain — leave it as-is and only add the flag.

## Step 5 — Apply edits with the script

```
uv run .github/skills/vss-description-review/scripts/vspec_desc_tool.py apply edits.json
```

This locates every entry by its exact dotted name (fresh per edit, so directive order never matters),
rewrites `description:`/`comment:` in place and leaves the rest of the file untouched. Text is written via
PyYAML, so special characters such as `: ` are quoted correctly, and text longer than 120 characters becomes a
folded block scalar (`>-`). It inserts `# Human check of description required: <reason>` directly above flagged
entries and prints which edits were skipped (entry not found), so typos in `edits.json` are caught immediately.
The edits stay in the working tree for the user to review.

## Step 6 — Report and hand back

Do not commit, push, or open a PR (see [Boundaries](#boundaries--read-first)). Instead, tell the user:

- which entries were changed and which rule(s) each change addresses, grouped by file (derive this from
  `edits.json` rather than re-deriving it from the diff),
- every `# Human check of description required` flag that was added, with file path and node name,
- that the diff is ready for their review, and that before submitting they should run
  `make mandatory_targets` (needs vss-tools) and `pre-commit run --all-files` (see [BUILD.md](../../../BUILD.md)).

Only if the user asks for it, record the file as reviewed in the local tracker (the user commits it):

```
uv run .github/skills/vss-description-review/scripts/vspec_desc_tool.py status mark <file> \
  --model "<model name>" --flags-open <count>
```

## Safety notes

- The skill never commits, pushes, opens PRs, or posts comments (see [Boundaries](#boundaries--read-first)).
- A full-catalog sweep touches dozens of files — confirm scope before starting and work file by file.
- When uncertain, flag per Step 4 instead of guessing; a wrong rewrite that silently changes signal meaning
  is worse than an unreviewed description.
- `rule_flags` from the scanner are heuristics (e.g. `possible_instance_reference` and `value_casing` can be
  false positives on short/common words) — use them to prioritize attention, not as an automatic verdict.
