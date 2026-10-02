---
name: vss-description-review
description: 'Review VSS data entries (branches, sensors, actuators, attributes) in spec/**/*.vspec files, rewrite `description`/`comment` fields to comply with the Description Guidelines, and open a Pull Request with the results. Flags entries that are too vague to fix without guessing. Use when: asked to review/update/unify/audit VSS descriptions, check a .vspec file or branch for description-guideline compliance, or review newly proposed/changed VSS elements before merge.'
argument-hint: 'Optional: file(s)/path or branch/PR to review; omit for a scoping discussion'
---

# VSS Description Review

Reviews `description:` (and `comment:`) fields of VSS data entries against the project's
[Description Guidelines](../../../docs-gen/content/rule_set/data_entry/description.md) and either fixes them
or flags them for a human. Works both as a retroactive audit of existing catalog entries and as a pre-merge
check on newly proposed VSS elements.

## When to Use

- "Review/update/fix/unify descriptions in `spec/...`"
- "Check this PR's new signals for description compliance"
- "Audit `Vehicle.X` for description guideline violations"

## Step 1 — Load the baseline

Always re-read [description.md](../../../docs-gen/content/rule_set/data_entry/description.md) first; it is the
single source of truth. Do not rely on a memorized copy of the rules, since this file changes over time.

## Step 2 — Determine scope

**One `.vspec` file = one PR.** Never bundle edits to multiple files into a single PR; if the requested
scope spans several files, work through them one at a time, each ending in its own branch and PR.

Before picking a file, check [review-status.json](./review-status.json) (read via
`python scripts/vspec_desc_tool.py status`) — files already marked reviewed should be skipped on a repeat
sweep unless the user explicitly asks to re-review them (e.g. after a guideline change).

Ask if not already clear:

- **Specific file(s)/branch path** given by the user → review those `.vspec` files, one PR each.
- **"New" / "proposed" elements, or a PR/branch** → diff against `master` (e.g.
  `git diff master...<branch> -- spec/**/*.vspec`) and review only added/changed entries, per file.
- **Whole catalog** → this touches dozens of files; confirm with the user before starting, then work
  through `status`'s unreviewed list one file (one PR) at a time.

## Step 3 — Scan instead of reading raw files

Run [scripts/vspec_desc_tool.py](./scripts/vspec_desc_tool.py) (stdlib-only Python, no install needed) to get
a structured, pre-extracted dataset instead of grepping/reading every `.vspec` file by hand:

```
python .github/skills/vss-description-review/scripts/vspec_desc_tool.py scan [path-or-glob ...] > entries.jsonl
```

With no arguments it scans all of `spec/**/*.vspec`. Each output line is one JSON entry:
`file`, `entry` (dotted name), `line`, `type`, `datatype`, `description`, `comment`, `allowed`,
`parent`/`parent_description`/`parent_comment`, `reusable_include_template`, and `rule_flags` — a list of
mechanically-detectable issues (`missing_description`, `boolean_casing:*`, `boolean_missing_true_false`,
`value_casing:<VALUE>`, `too_many_sentences`, `possible_instance_reference:<word>`). Reason over this JSONL,
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
python .github/skills/vss-description-review/scripts/vspec_desc_tool.py apply edits.json
```

This locates every entry by its exact dotted name (fresh per edit, so directive order never matters),
rewrites `description:`/`comment:` in place, and inserts
`# Human check of description required: <reason>` directly above flagged entries. It prints which edits were
skipped (entry not found) so typos in `entries.json` are caught immediately instead of silently failing.
Review the resulting diff before committing.

## Step 6 — Applying to newly proposed elements

When reviewing a PR or draft branch instead of the existing catalog, run the scan against only the
added/changed files from the diff, then apply the same Step 4–5 procedure restricted to the added/changed
entries. If you are not the PR author, prefer leaving GitHub PR review comments (via the PR review tools)
pointing at the specific lines instead of pushing commits directly.

## Step 7 — Commit and open the PR

1. Create a local branch for the review, scoped to the **single `.vspec` file** being reviewed (do not
   commit directly on `master`, and do not mix in a second file — see Step 2).
2. Commit with a sign-off line per [CONTRIBUTING.md](../../../CONTRIBUTING.md)
   (`Signed-off-by: Firstname Lastname <you@example.com>`, i.e. `git commit -s`).
3. Before pushing, suggest running `make travis-targets` and `pre-commit run --all-files` (see
   [BUILD.md](../../../BUILD.md)) to catch unrelated CI failures.
4. Push and open a Pull Request (use the GitHub PR tools/skill available in this environment).
   - **PR title must include the LLM model used for the review**, e.g.
     `Description review: spec/Body/Body.vspec (model: <model name>)`.
   - The PR description must include:
     - which rule(s) each changed entry now complies with (brief, grouped by file) — derive this from
       `edits.json` rather than re-deriving it from the diff,
     - a dedicated list of every `# Human check of description required` flag added, with file path and
       node name, so maintainers can resolve them quickly.
5. After opening the PR, update the tracker:
   ```
   python .github/skills/vss-description-review/scripts/vspec_desc_tool.py status mark <file> \
     --model "<model name>" --flags-open <count> --pr <PR URL>
   ```
   Commit `review-status.json` as part of the same PR (or a quick follow-up commit on the same branch) so
   the next sweep knows this file is already covered.

## Safety notes

- A full-catalog sweep touches dozens of files — confirm scope before starting, and always split into one
  PR per `.vspec` file (Step 2), never one giant PR.
- When uncertain, flag per Step 4 instead of guessing; a wrong rewrite that silently changes signal meaning
  is worse than an unreviewed description.
- `rule_flags` from the scanner are heuristics (e.g. `possible_instance_reference` and `value_casing` can be
  false positives on short/common words) — use them to prioritize attention, not as an automatic verdict.
