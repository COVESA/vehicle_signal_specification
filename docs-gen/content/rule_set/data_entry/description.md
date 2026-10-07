---
title: "Description Guidelines"
date: 2026-10-01T00:00:00+00:00
weight: 40
---

# Description Guidelines

This chapter defines how `description` (and `comment`) fields for data entries
(branches, sensors, actuators, attributes) in VSS shall be written, so every entry reads consistently across the catalog.

## Golden Rules

1. **Consistent** across all data entries — same structure, same tone.
2. **Dictionary-style, max 3 sentences:** sentence 1 defines what the entry *is* (a concise noun phrase, not a narrative about usage); sentence 2 explains ranges/values if needed; sentence 3 adds a specific note only when relevant. Most entries only need one sentence — do not pad.
3. **Self-contained:** fold in the meaning of the parent branch/sub-system so the description stands alone.
4. **No instance references:** never name an instance value (`Left`/`Right`, `Row1`, `Driver`) — one description serves all instances.
5. **Modular, stand-alone entities:** a branch description never enforces or exhaustively lists its children; refer to them loosely ("may contain elements such as...").
6. **Booleans** are described as `True` / `False` (title case), matching the casing used throughout the catalog.
7. **Allowed values** (the catalog's established mechanism for restricting strings; `enum` is a newer, rarely used alternative) are referenced in UPPERCASE, words separated by `_`, matching the `allowed`/`enum` list exactly. List value explanations **at the end**, only when they add clarity, and only if the breakdown is short. A long or implementation-specific breakdown belongs in `comment:`.
8. **`comment:`** holds supplementary detail that would overload the compact `description` — term clarifications, standards references, calculation/implementation specifics, cross-references to related signals, or OEM/vendor customization notes. Preserve ambiguous domain wording there rather than guessing a rewrite.
9. **Plain English**, consistent spelling (e.g. American English) throughout a contribution.

---

## 1. Structure and compactness

✅ **Correct (dictionary-style, one sentence; three sentences only when each adds information):**
```yaml
Sunroof.Status:
  allowed: [ "CLOSED", "INTERMEDIATE", "OPEN" ]
  description: Current opening state of the sunroof.

DoorsLockStatus:
  allowed: [ "UNLOCKED", "SELECTIVELOCKED", "LOCKED", "SECURED" ]
  description: Indicates whether the doors are physically secured against unauthorized entry. UNLOCKED = doors open to entry; SELECTIVELOCKED = only the driver door unlocked; LOCKED = all doors locked; SECURED = locked with additional theft protection engaged.
```

❌ **Incorrect (narrative instead of definition; padded beyond what's needed):**
```yaml
Sunroof.Status:
  description: This tells you how open the sunroof currently is so an app can display it to the user.

OccupantContext.InterruptibilityIndex:
  description: The Interruptibility Index is a measure of user-engagement in other activities and describes how interruptible the driver or passenger is. The level of occupant-engagement. 0 = not interruptible. 10 = interruptible.
```

---

## 2. Self-contained, instance-free, modular

✅ **Correct (generic, valid for every instance; branch folds in context loosely; leaf absorbs parent's meaning):**
```yaml
Door.IsOpen:
  description: Indicates whether the door is open. True = open; False = closed.

Preconditioning:
  type: branch
  description: Climate preconditioning of the cabin before a trip. May contain elements such as target temperature, schedule, and capability attributes.

Preconditioning.Capability.SetTargetTemp:
  datatype: boolean
  description: Indicates whether the user can set a target temperature for preconditioning. True = capable; False = not capable.
```

❌ **Incorrect (references an instance; declares an exhaustive child list; leaf meaningless without its branch):**
```yaml
Door.IsOpen:
  description: Indicates whether the left front door is open. True = open; False = closed.

Preconditioning:
  type: branch
  description: Climate preconditioning of the cabin before a trip, consisting of TargetTemperature, Schedule and Capability.

Preconditioning.Capability.SetTargetTemp:
  datatype: boolean
  description: Target temperature setting.
```

---

## 3. Allowed and enum values

`allowed` is the catalog's established mechanism for restricting string values; `enum` (integer-backed, with symbolic names) is a newer alternative used only sparingly — do not assume it is the default.

✅ **Correct (cryptic values explained at the end; self-explanatory values left unlisted; long/technical breakdown moved to `comment:` to keep `description` compact):**
```yaml
FlatDetectionQualifier:
  allowed: [ "INITIALIZING", "DETECTED", "DETECTED_WITHOUT_POSITION", "NO_FLAT_DETECTED", "INVALID" ]
  description: Reliability state of tire flat detection. DETECTED = flat detected with wheel position; DETECTED_WITHOUT_POSITION = flat detected, position unknown; NO_FLAT_DETECTED = active, no flat; INVALID = signal not usable.

Window.Status:
  allowed: [ "CLOSED", "INTERMEDIATE", "OPEN" ]
  description: Current opening state of the window.

OperatingMode:
  allowed: [ "CHARGE_DEPLETING", "CHARGE_SUSTAINING", "BLENDED" ]
  description: Current operating mode of the vehicle's range-extending powertrain.
  comment: CHARGE_DEPLETING - vehicle runs primarily on battery power, state of charge decreases. CHARGE_SUSTAINING - generator runs to maintain battery charge level. BLENDED - battery and generator are used simultaneously, typically under high power demand.
```

❌ **Incorrect (lowercase, listed up front; restates every self-evident value):**
```yaml
Window.Status:
  description: state can be closed, intermediate or open.

Seat.Cooling:
  allowed: [ "OFF", "ON", "AUTOMATIC", "NO_CHANGE" ]
  description: Setting for cooling. OFF = off; ON = on; AUTOMATIC = automatic; NO_CHANGE = no change.
```

---

## 4. Comments vs. descriptions

The `description` is the neutral, consumer-facing definition, kept compact. Use `comment:` for anything that would otherwise overload it: term clarifications, standards references, calculation/implementation detail, cross-references to related signals, or OEM/vendor customization notes — and preserve uncertain domain
wording there rather than guessing.

✅ **Correct:**
```yaml
Trunk:
  type: branch
  description: State of the vehicle's trunk.
  comment: A trunk is a luggage compartment in a vehicle.

SupportedFuel:
  allowed: [ "E5_95", "E5_98", "E10_95", "E10_98" ]
  description: Detailed information on fuels supported by the vehicle.
  comment: Allowed values are not standardized; each OEM can specify detailed descriptions of array elements.

TireDetectionQualifier:
  description: Operational status and health of the tire monitoring system, reported per responsible function master.
  comment: Exact per-state ECU semantics unconfirmed; original wording preserved for the maintainer.
```

❌ **Incorrect (standards/implementation detail crammed into the consumer-facing description instead of `comment:`):**
```yaml
Trunk.AbsoluteVolume:
  description: Volume of the trunk calculated per SAE J1100-2009 clause 4.3.2, excluding sub-trunk compartments, measured with seats in design position, and may vary by up to 5% depending on measurement method.
```

---

## 5. Do / Don't quick reference

| Do | Don't |
|----|-------|
| Say what the entry **is**, as a dictionary-style definition. | Restate the name or narrate its usage/purpose. |
| Keep to **3 sentences max** (most entries only need one). | Write paragraphs. |
| Use `True` / `False` for booleans. | Use `TRUE`/`FALSE`, lowercase, or leave states implicit. |
| Put allowed values UPPERCASE **at the end**, only if helpful; favor `allowed` over `enum`. | List self-explanatory values, put them first, or write a long breakdown in `description`. |
| Fold in **parent sub-system** context; refer to children loosely. | Rely on the tree, reference an instance, or declare an exhaustive child list. |
| Move standards refs, calculation detail, and OEM notes to `comment:`; preserve ambiguous lines there. | Overload `description` with implementation detail, or rewrite lines whose meaning is unsure. |

---

## 6. Review procedure

Descriptions are reviewed against this baseline **entry by entry**. If an entry's meaning is **vague**, or a rewrite risks **losing or changing domain-specific meaning**, do not guess — flag it, keep the original text in a `comment:`, and report it for confirmation by someone familiar with the signal before finalizing.
