---
title: "Description Guidelines"
date: 2026-10-01T00:00:00+00:00
weight: 40
---

# Description Guidelines

This chapter defines how `description` (and `comment`) fields for data entries
(branches, sensors, actuators, attributes) in VSS shall be written. It is the
baseline for reviewing and enhancing descriptions so that every entry reads
consistently across the catalog.

## Golden Rules (summary)

1. **Consistent** across all data entries — same structure, same tone.
2. **Maximum 3 sentences.** Add a sentence only when it carries new information.
3. **Structure:** (1) what the entry is, (2) what its values/ranges mean, (3) a specific note when relevant.
4. **Self-contained:** fold in the meaning of the parent branch so the description stands alone.
5. **No instance references:** fold in the parent sub-system (e.g. *traction battery*, *trunk*), but never
   name an instance value (`Left`/`Right`, `Row1`, `Driver`) — one description serves all instances.
6. **Plain English**, using consistent spelling (e.g. American English) throughout a contribution.
7. **Booleans** are described as `TRUE` / `FALSE`.
8. **Allowed/enum values** are written in UPPERCASE, listed **at the end**, and only when they add clarity.
   Separate words with `_`, e.g. `ADDED_VALUE`. Value explanations must match the `allowed`/`enum` list
   exactly.
9. **Non-English expressions** are translated, with the original kept in parentheses, e.g. a German term
   such as ("Fahrerlebnisschalter").
10. **`comment:`** holds implementation-, vendor-, or domain-specific remarks — not the `description`.
11. **Dictionary-style first sentence:** define what the entry *is* as a concise noun phrase, the way a
    dictionary entry would — not a narrative about how or why it is used.
12. **Modular, stand-alone entities:** branches and leaves are independent. A branch description never
    enforces or exhaustively lists its children; refer to them loosely ("may contain elements such as...")
    since the sub-tree can change independently.

---

## 1. Structure — up to three sentences

Write in this order and stop as soon as the entry is clear:

| Sentence | Purpose | Always required? |
|----------|---------|------------------|
| 1 | **What** the data entry is about. | Yes |
| 2 | **Extended explanation** — what the ranges, units, or values mean. | Only if values/ranges need it |
| 3 | **Specific note** — edge cases, invalid states, related entries. | Only when relevant |

Keep sentences **compact**. Do not pad with a second or third sentence if the first already says everything.

### 1.1 Sentence 1 is a dictionary-style definition

The first sentence must read like a dictionary entry: a concise noun phrase that defines what
the entry **is**. It does not narrate how the entry is used, why it exists, or by whom.

✅ **Correct (dictionary-style — defines the entry):**
```yaml
Sunroof.Status:
  allowed: [ "CLOSED", "INTERMEDIATE", "OPEN" ]
  description: Current opening state of the sunroof.
```

❌ **Incorrect (narrative — describes usage/purpose instead of defining the entry):**
```yaml
Sunroof.Status:
  description: This tells you how open the sunroof currently is so an app can display it to the user.
```

✅ **Correct (three sentences, each adds information):**
```yaml
DoorsLockStatus:
  allowed: [ "UNLOCKED", "SELECTIVELOCKED", "LOCKED", "SECURED" ]
  description: Indicates whether the doors are physically secured against unauthorized entry. UNLOCKED = doors open to entry; SELECTIVELOCKED = only the driver door unlocked; LOCKED = all doors locked; SECURED = locked with additional theft protection engaged.
```

❌ **Incorrect (restates the name, no information):**
```yaml
DoorsLockStatus:
  description: Status of doors.
```

❌ **Incorrect (too long — repeats itself and exceeds 3 sentences):**
```yaml
OccupantContext.InterruptibilityIndex:
  min: 0
  max: 10
  description: The Interruptibility Index is a measure of user-engagement in other activities and describes how interruptible the driver or passenger is, for e.g. proactive assistant recommendations. The level of occupant-engagement. 0 = not interruptible. 10 = interruptible.
```

✅ **Correct (same meaning, compact):**
```yaml
OccupantContext.InterruptibilityIndex:
  min: 0
  max: 10
  description: How interruptible the occupant is, e.g. for proactive assistant recommendations. 0 = not interruptible; 10 = fully interruptible.
```

---

## 2. Self-contained descriptions

A description must be understandable without reading the parent branch. Fold the relevant
parent context into the child description so it stands alone.

**Do not reference instances.** One description is shared by every instance of its branch
(e.g. `Row1`/`Row2`, `Left`/`Right`/`Center`, `Driver`/`Passenger`). Write the text so it is
correct for all instances — never bake in a specific instance value.

✅ **Correct (generic — valid for every instance):**
```yaml
Door.IsOpen:
  description: Indicates whether the door is open. TRUE = open; FALSE = closed.
```

❌ **Incorrect (references an instance):**
```yaml
Door.IsOpen:
  description: Indicates whether the left front door is open. TRUE = open; FALSE = closed.
```

Parent **branch** descriptions should summarize what the sub-tree contains, so a reader
knows the scope at a glance.

✅ **Correct:**
```yaml
Trunk:
  type: branch
  description: State of the vehicle's trunk, e.g. may contain elements such as lock, open/closed status and door position.
```

### 2.1 Branches and leaves are modular, stand-alone entities

Every branch and every leaf is an independent, stand-alone entity. A branch description must
never **enforce** or **exhaustively declare** its children, because the sub-tree can gain,
lose, or rename leaves independently of the branch. Refer to possible children loosely — "may
contain elements such as...", "could include..." — rather than as a fixed, guaranteed list.

✅ **Correct (loose reference, no enforced connection):**
```yaml
Preconditioning:
  type: branch
  description: Climate preconditioning of the cabin before a trip. May contain elements such as target temperature, schedule, and capability attributes.
```

❌ **Incorrect (declares an exhaustive, enforced list of children):**
```yaml
Preconditioning:
  type: branch
  description: Climate preconditioning of the cabin before a trip, consisting of TargetTemperature, Schedule and Capability.
```

A leaf whose name alone is generic (`Mileage`, `MaxCurrent`) must absorb the qualifier from
its parent so the reader knows *which* mileage or *whose* current is meant.

✅ **Correct (folds the "last service" context of the parent):**
```yaml
LastService.Mileage:
  unit: km
  description: Odometer reading at the time of the last workshop service.
```

❌ **Incorrect (meaningless without the branch):**
```yaml
LastService.Mileage:
  unit: km
  description: Mileage.
```

✅ **Correct (makes clear the value belongs to the connected station, not the vehicle):**
```yaml
ConnectedChargingStation.MaxCurrent:
  unit: A
  description: Maximum current the connected charging station can provide.
```

### When the branch meaning is essential

Some leaf entries are ambiguous — or actively misleading — without their branch. Under a
`Capability` branch, a leaf like `SetTargetTemp` is **not** a temperature value but a yes/no
*capability*. The leaf description must fold in the branch meaning so it cannot be misread.

Parent branch:
```yaml
Preconditioning.Capability:
  type: branch
  description: Availability and capability of attributes used for climate preconditioning.
```

✅ **Correct (folds the "capability" meaning of the parent into the leaf):**
```yaml
Preconditioning.Capability.SetTargetTemp:
  datatype: boolean
  description: Indicates whether the user can set a target temperature for preconditioning. TRUE = capable; FALSE = not capable.
```

❌ **Incorrect (reads like the temperature value, losing the "capability" meaning):**
```yaml
Preconditioning.Capability.SetTargetTemp:
  datatype: boolean
  description: Target temperature setting.
```

---

## 3. Booleans

Describe both states explicitly as `TRUE` / `FALSE`.

✅ **Correct:**
```yaml
Sunroof.Available:
  datatype: boolean
  description: Indicates whether the vehicle is equipped with a sunroof. TRUE = equipped; FALSE = not equipped.
```

❌ **Incorrect:**
```yaml
Sunroof.Available:
  datatype: boolean
  description: Sunroof available in the vehicle.
```

---

## 4. Allowed and enum values

- Reference allowed/enum values in **UPPERCASE**, matching the list exactly, words separated by `_`.
- Put value explanations **at the end** of the description, after the general sentence.
- Explain values **only when they add clarity.** If the values are self-explanatory
  (e.g. `CLOSED` / `OPEN`, `ON` / `OFF`), do **not** list them.

✅ **Correct (values are cryptic — explain them at the end):**
```yaml
FlatDetectionQualifier:
  allowed: [ "INITIALIZING", "DETECTED", "DETECTED_WITHOUT_POSITION", "NO_FLAT_DETECTED", "INVALID" ]
  description: Reliability state of tire flat detection. DETECTED = flat detected with wheel position; DETECTED_WITHOUT_POSITION = flat detected, position unknown; NO_FLAT_DETECTED = active, no flat; INVALID = signal not usable.
```

✅ **Correct (values are self-explanatory — do not list them):**
```yaml
Window.Status:
  allowed: [ "CLOSED", "INTERMEDIATE", "OPEN" ]
  description: Current opening state of the window.
```

❌ **Incorrect (lowercase, listed up front, no added clarity):**
```yaml
Window.Status:
  description: state can be closed, intermediate or open.
```

✅ **Correct (explain only the value that needs it):**
```yaml
Seat.Cooling:
  allowed: [ "OFF", "ON", "AUTOMATIC", "NO_CHANGE" ]
  description: Seat cooling/ventilation setting applied during climate preconditioning; NO_CHANGE keeps the current setting.
```

❌ **Incorrect (restates every self-evident value, adds nothing):**
```yaml
Seat.Cooling:
  allowed: [ "OFF", "ON", "AUTOMATIC", "NO_CHANGE" ]
  description: Setting for cooling. OFF = off; ON = on; AUTOMATIC = automatic; NO_CHANGE = no change.
```

✅ **Correct (values encode a non-obvious concept — spell them out):**
```yaml
HeatingCapability:
  allowed: [ "NOT_CODED", "CODED_WITH_AUTOMATIC", "CODED_WITHOUT_AUTOMATIC" ]
  description: Whether seat heating is coded (equipped) in the vehicle. NOT_CODED = not equipped; CODED_WITH_AUTOMATIC = equipped with automatic mode; CODED_WITHOUT_AUTOMATIC = equipped without automatic mode.
```

---

## 5. Comments vs. Descriptions

The `description` is the neutral, consumer-facing definition. Use `comment:` for anything
that is vendor-internal, integration-specific, or domain-ambiguous.

- **Vendor / integration specifics** → `comment:`.
- **Domain-specific ambiguity** → keep the original wording untouched in a `comment:`;
  do **not** rewrite a line whose precise domain meaning you are unsure of — preserve it.

✅ **Correct:**
```yaml
Seat.Massage.TypeActive:
  description: Currently active massage program.
  comment: Referred to as "massage program" in some OEM implementations.
```

✅ **Correct (internal contact and timeline belong in the comment):**
```yaml
ChargingPort.StatusClearText:
  description: Additional charging-plug status needed to correctly interpret ChargingPort.Status on certain vehicles.
  comment: Vendor-specific workaround; see internal issue tracker for the owning team and rollout timeline.
```

✅ **Correct (unsure of exact ECU semantics — preserve the original wording in the comment):**
```yaml
TireDetectionQualifier:
  description: Operational status and health of the tire monitoring system, reported per responsible function master.
  comment: Exact per-state ECU semantics unconfirmed; original wording preserved for the maintainer.
```

❌ **Incorrect (vendor-internal jargon leaks into the consumer-facing description):**
```yaml
ChargingPort.StatusClearText:
  description: Workaround for internal ticket ABC-123; onboard fix expected next release. Charging-plug status text.
```

---

## 6. Language

- **Plain English**, with consistent spelling across a contribution (e.g. American English:
  color, not colour; behavior, not behaviour).
- **Non-English terms** are translated, keeping the original in parentheses.

✅ **Correct:**
```yaml
FES:
  type: branch
  description: Information related to the driving experience switch ("Fahrerlebnisschalter"), used to select the driving mode.
```

❌ **Incorrect (untranslated non-English term, no context):**
```yaml
FES:
  description: Information related to the "Fahrerlebnisschalter"
```

---

## 7. Do / Don't quick reference

| Do | Don't |
|----|-------|
| Say what the entry **is**, as a dictionary-style definition. | Restate the name or narrate its usage/purpose. |
| Keep to **3 sentences max**. | Write paragraphs. |
| Use `TRUE` / `FALSE` for booleans. | Use `True`/`False` or leave states implicit. |
| Put allowed/enum values UPPERCASE **at the end**, only if helpful. | List self-explanatory values or put them first. |
| Fold in **parent sub-system** context. | Rely on the tree or reference an instance (e.g. "left front door"). |
| Refer to children loosely ("may contain elements such as..."). | Declare an exhaustive, enforced child list in a branch description. |
| Translate non-English terms, keep original in parentheses. | Leave untranslated non-English terms. |
| Move vendor/integration notes to `comment:`. | Mix internal remarks into `description`. |
| Preserve ambiguous domain lines in `comment:`. | Rewrite lines whose meaning you are unsure of. |

---

## 8. Review procedure

Descriptions are reviewed against this baseline **entry by entry**. During review:

- If an entry's meaning is **vague**, or a rewrite risks **losing or changing
  domain-specific meaning**, **do not guess** — flag it and keep the original text in a
  `comment:` until clarified.
- Report every such vague or domain-sensitive entry for confirmation by someone familiar
  with the signal before finalizing.
