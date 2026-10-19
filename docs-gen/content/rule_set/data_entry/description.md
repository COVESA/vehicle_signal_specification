---
title: "Description Guidelines"
date: 2026-10-01T00:00:00+00:00
weight: 35
---

# Description Guidelines

Guidelines for `description` and `comment` attributes

## Golden Rules

1. **Consistent** across all data entries — same structure, same tone.
2. **Dictionary-style, max 3 sentences:** sentence 1 defines what the entry *is* (a concise noun phrase, not a narrative about usage); sentence 2 explains ranges/values if needed; sentence 3 adds a specific note only when relevant. Most entries only need one sentence — do not pad.
3. **Self-contained:** fold in the meaning of the parent branch/sub-system so the description stands alone.
4. **No instance references:** never name an instance value (`Left`/`Right`, `Row1`, `Driver`) — one description serves all instances.
5. **Modular, stand-alone entities:** a branch description never enforces or exhaustively lists its children; refer to them loosely ("may contain elements such as...").
6. **`comment:`** details that would overload the compact `description` — term clarifications, standards references, calculation/implementation specifics, cross-references to related signals, or OEM/vendor customization notes.
7. **Plain English**, consistent spelling (e.g. American English) throughout a contribution.
8. **Text, not layout:** descriptions and comments are processed by tools that do not preserve line breaks, so do not rely on them (no ASCII art or manual formatting). Keep source lines at 120 characters or fewer by using a folded block scalar (`>-`) for longer text.

---

## Examples

### Structure and compactness

✅ **Good (dictionary-style, one sentence; three sentences only when each adds information):**
```yaml
Sunroof.Status:
  allowed: [ "CLOSED", "INTERMEDIATE", "OPEN" ]
  description: Current opening state of the sunroof.

DoorsLockStatus:
  allowed: [ "UNLOCKED", "SELECTIVELOCKED", "LOCKED", "SECURED" ]
  description: >-
    Indicates whether the doors are physically secured against unauthorized entry. UNLOCKED = doors open to entry;
    SELECTIVELOCKED = only the driver door unlocked; LOCKED = all doors locked; SECURED = locked with additional
    theft protection engaged.
```

❌ **Bad (narrative instead of definition; padded beyond what's needed):**
```yaml
Sunroof.Status:
  description: This tells you how open the sunroof currently is so an app can display it to the user.

OccupantContext.InterruptibilityIndex:
  description: The Interruptibility Index is a measure of user-engagement in other activities and describes how interruptible the driver or passenger is. The level of occupant-engagement. 0 = not interruptible. 10 = interruptible.
```

---

### Self-contained, instance-free, modular

Boolean states are written as `True` / `False`, as in the example below.

✅ **Good (generic, valid for every instance; branch folds in context loosely; leaf absorbs parent's meaning):**
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

❌ **Bad (references an instance; declares an exhaustive child list; leaf meaningless without its branch):**
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

### Allowed and enum values

`allowed` is the catalog's established mechanism for restricting string values; `enum` (integer-backed, with symbolic names) is a newer alternative used only sparingly — do not assume it is the default.
Values are written exactly as in the `allowed`/`enum` list (UPPERCASE, words separated by `_`). Explain them at the end of the description, only when they add clarity and only if the breakdown is short; a long or implementation-specific breakdown belongs in `comment:`.

✅ **Good (cryptic values explained at the end; self-explanatory values left unlisted; long/technical breakdown moved to `comment:` to keep `description` compact):**
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
  comment: >-
    CHARGE_DEPLETING - vehicle runs primarily on battery power, state of charge decreases. CHARGE_SUSTAINING -
    generator runs to maintain battery charge level. BLENDED - battery and generator are used simultaneously,
    typically under high power demand.
```

❌ **Bad (lowercase, listed up front; restates every self-evident value):**
```yaml
Window.Status:
  description: state can be closed, intermediate or open.

Seat.Cooling:
  allowed: [ "OFF", "ON", "AUTOMATIC", "NO_CHANGE" ]
  description: Setting for cooling. OFF = off; ON = on; AUTOMATIC = automatic; NO_CHANGE = no change.
```

---

### Comments vs. descriptions

The `description` is the neutral, consumer-facing definition, kept compact. Use `comment:` for anything that would otherwise overload it: term clarifications, standards references, calculation/implementation detail, cross-references to related signals, or OEM/vendor customization notes — and preserve uncertain domain
wording there rather than guessing.

✅ **Good:**
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

❌ **Bad (standards/implementation detail crammed into the consumer-facing description instead of `comment:`):**
```yaml
Trunk.AbsoluteVolume:
  description: Volume of the trunk calculated per SAE J1100-2009 clause 4.3.2, excluding sub-trunk compartments, measured with seats in design position, and may vary by up to 5% depending on measurement method.
```

---

## Using the review skill

See [Description Review Skill](/vehicle_signal_specification/policies/description_review_skill) for how to check descriptions against these guidelines with an AI coding assistant.
