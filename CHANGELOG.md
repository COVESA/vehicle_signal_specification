# VSS Changelog

The intention of this document is to highlight major changes in the VSS specification (syntax and/or signals).
It shall include all changes that affect backward compatibility or may be important to know when upgrading from one version to another.
It typically does not list all changes to signals.
It includes changes that are included in released version, but also changes planned for upcoming releases.

*This document only contains changes introduced in VSS 3.0 or later!*



## VSS 3.0

[Complete release notes](https://github.com/COVESA/vehicle_signal_specification/releases/tag/v3.0)

### Instantiate

A new attribute `instantiate` has been added to the syntax to exclude a child-node from the instantiation of the *direct* parent node.
This attribute is by default true and is only relevant to use for signals

An example on how this signals shall be handled by tools:

```YAML
Vehicle.X:
  type: branch
  instances: Test[1,2]
  description: High-level vehicle data.

Vehicle.X.InstantiatedSignal:
  type: attribute
  description: "Instantiated Signal"
  datatype: string

Vehicle.X.NotInstantiatedSignal:
  type: attribute
  description: "Not Instantiated Signal"
  datatype: string
  instantiate: False
```

Results in the following dot-notated output:

```
Vehicle.X
Vehicle.X.NotInstantiatedSignal
Vehicle.X.Test1.NotInstantiatedSignal
Vehicle.X.Test2.NotInstantiatedSignal
```
The new attribute is not used for any signals in VSS 3.0.
For more information see [documentation](https://github.com/COVESA/vehicle_signal_specification/blob/master/docs-gen/content/rule_set/instances.md).

### Changed Path to Battery Signals

The path `Vehicle.Powertrain.Battery` was renamed to `Vehicle.Powertrain.TractionBattery`.
The path name was changed to make it clear that the signals in the path concerns the traction battery (high voltage battery) used by electrical or hybrid vehicles,
and not the supply battery (low voltage battery, typically 12 or 24 Volts).

### Enum/Allowed attribute

Before VSS 3.0 the attribute `enum` could be used to list allowed values for a VSS signals, like in the example below:

```
LowVoltageSystemState:
  datatype: string
  type: sensor
  enum: [
    "UNDEFINED", # State of low voltage system not known
    "LOCK",      # Low voltage system off, steering lock or equivalent engaged
    "OFF",       # Low voltage system off, steering lock or equivalent not engaged
    "ACC",       # Vehicle Accessories on/living
    "ON",        # Engine start enabled (e.g. ignition on, diesel pre-heating, electrical drive released)
    "START"      # Engine starter relay closed (not applicable for electrical vehicles)
    ]
  description: State of the supply voltage of the control units (usually 12V).
```

From VSS 3.0 this attribute has been renamed to `allowed`. The background is that the old name was misleading,
as it does not correspond to enum definitions in many programming languages, but rather just is a limitation of what values
that are supported by the signal.


All signals in VSS previously using `enum`has been updated to use `allowed`, like in the example below:

```
LowVoltageSystemState:
  datatype: string
  type: sensor
  allowed: [
    'UNDEFINED', # State of low voltage system not known
    'LOCK',      # Low voltage system off, steering lock or equivalent engaged
    'OFF',       # Low voltage system off, steering lock or equivalent not engaged
    'ACC',       # Vehicle Accessories on/living
    'ON',        # Engine start enabled (e.g. ignition on, diesel pre-heating, electrical drive released)
    'START'      # Engine starter relay closed (not applicable for electrical vehicles)
    ]
  description: State of the supply voltage of the control units (usually 12V).
```

If the old keyword `enum` is used most tools will ignore it and give a warning.

```
Warning: Attribute(s) enum in element Position not a core or known extended attribute.
```

### Seat signals

The signals in `Vehicle.Cabin.Seat` have been significantly refactored.
The background is that the old representation included limitations and ambiguities.

## VSS 3.1

### Struct Support (Experimental)

VSS has been extended with syntax to define structs, and to use them for signals.
For VSS 3.1 support is only experimental and syntax may change.

*Note: Only a subset of VSS-tools for VSS 3.1 supports structs!*

### Actuator and Sensor Attributes

VSS has two attributes `sensor` and `actuator` that gives the possibility to specify which system/entity that provides the value
or tries to actuate the value. A possible hypothetical example is shown below showing that it is `TemperatureSensorUnderDriverSeat` that
provides the values of `Vehicle.Cabin.Temperature` and it is `HVACSystem` that tries to assure that the specified temperature is achieved.
These two attributes have never been used by signals in the VSS repository and it has been decided that these attributes no longer shall
be part of the official VSS syntax. If needed, this type of information shall be provided by overlays.

```
Vehicle.Cabin.Temperature:
  type: actuator
  description: Temperature in cabin
  datatype: float
  unit: km/h
  sensor: 'TemperatureSensorUnderDriverSeat'
  actuator: 'HVACSystem'
```

For VSS 3.1 the two attributes will remain in the VSS Syntax, but are marked as deprecated.
No change to tooling is implemented, as the vss-tools already today give a warning if the attributes are used:

```
Warning: Attribute(s) sensor in element Temperature not a core or known extended attribute.
```

### Deprecated or Deleted signals

* `Vehicle.TravelledDistance` deprecated from 3.1. New signal `Vehicle.TraveledDistance`added.
  Background is to be aligned with VSS style guide using American English.
* `Vehicle.Powertrain.FuelSystem.TimeSinceStart` deprecated from 3.1. New signal `Vehicle.StartTime` added.
  Reason is that `TimeSinceStart` is not powertrain-related and other signals related to current trip are located on top-level.
  After discussion it was agreed that it is better to have a signal for start time rather than duration.
* Refactoring of signals in `Vehicle.Body.Lights` branch performed, some signals have new names.

## VSS 4.0 (Latest Release)

### Struct Support (Official)

The VSS-syntax now supports structs.
Note however that not all exporters in [VSS-tools](https://github.com/COVESA/vss-tools) 4.0 support structs yet.

### Change of instance handling for seats, doors, mirrors and other branches.

Previously many signals used position for instance, where position 1 meant the leftmost item.
This caused problems for some use-cases where it was more practical to reference to a door by its relative position,
like the "DriverSide" door, as you then can describe wanted behavior in the same way for both LHD and RHD vehicles.
By that reason instance handling has for some signal been changed to use `["DriverSide","Middle","PassengerSide"]`.

### Actuator and Sensor Attributes

The attributes `sensor` and `actuator`, deprecated from VSS 3.1,
have been removed from the [VSS syntax](docs-gen/content/rule_set/data_entry/sensor_actuator.md).

### Deprecated or Deleted signals

* `Vehicle.TravelledDistance`
* `Vehicle.Powertrain.FuelSystem.TimeSinceStart`


## Planned Changes VSS 4.1


### Deprecated or Deleted signals

* `Vehicle.Cabin.Seat.*.*.Heating` deprecated from 4.1. New signal `Vehicle.Cabin.Seat.*.*.HeatingCooling` added.

## Planned Changes VSS 5.0

-
