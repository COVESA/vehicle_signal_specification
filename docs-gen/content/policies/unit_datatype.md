---
title: "Unit and Datatype Policy"
date: 2019-08-04T12:46:30+02:00
weight: 5
---


## Introduction



Each signal in VSS has a datatype and unless it only represent a counter also a unit.
The VSS standard catalog includes a large number of units in the [unit definition file](https://github.com/COVESA/vehicle_signal_specification/blob/master/spec/units.yaml), but not all are intended to be used in the VSS standard catalog.


### Unit Policy

VSS signals typically use the unit used by humans when talking about the value, but prefers SI-units or derived SI-units when feasible. Prefixed units, like millimeter or kilometer are acceptable to get a value that is easier to understand for a human or that better fits requirements on datatypes or assumed precision.


#### Examples and Exceptions

* For time `hour` is an accepted unit when `second` precision typically is not needed, like signals recording vehicle life time or combined units like `Ah` and `km/h`
* For speed `km/h` is the preferred unit for vehicle speed, as that is the common unit to present speed to (European) drivers
* Inches as unit are acceptable when the signal correspond to a size rather than a measurement and the size typically is measured in inches, also in countries typically using SI-units. A typical example is `Axle.WheelDiameter`
* Celsius shall be used as  temperature unit

### Datatype Policy

VSS provides a default datatype for each signal. VSS is not concerned with how signals are transmitted and does not consider scaling/offset typically used in transport protocols. An implementation may use a different datatype than specified in the VSS standard catalog.

The selected combination of unit and datatype shall cover likely expectations on value range and precision.
If it is unlikely that someone is interested in decimals for the value for the selected unit, select a signed or unsigned integer type.
Select a size which with reasonable margins can cover all vehicles.
If it is likely that decimal values are needed, select float or, if relevant, double.

#### Examples

* `Vehicle.TraveledDistance` uses `meter` and `uint32`. This has been selected as meter resolution is assumed to be sufficient (no need for decimals), and `uint32` gives for vehicles with high mileage better precision that `float`. It is unlikely that the signal will wrap around, so no need for `uint64`.
