---
title: "Data Units"
date: 2019-08-04T12:36:12+02:00
weight: 20
---

## Introduction to Data Units in VSS

It is in VSS possible for signals to specify a unit of measurement from a list of predefined data units.
For most signals in the VSS standard catalog, a data unit has been selected. A typical example is `Vehicle.Speed`, as shown below.

```
Vehicle.Speed:
  datatype: float
  type: sensor
  unit: km/h
  description: Vehicle speed.
```

The ambition when selecting data unit for signals in VSS standard catalog has been to use either a unit based on SI-units,
or a unit commonly used within the vehicle industry. For the `Vehicle.Speed` example above this means that `km/h` has been selected,
even if `m/s` from an SI-perspective would have been a better choice.

It must be noted that the selected unit does not imply that the value of `Vehicle.Speed` always needs to be sent or visualized
as `km/h` (with float as datatype). A user interface or API may show or request vehicle speed in any unit it likes,
and a transport protocol may send speed in another unit, possibly also involving scaling and offset.
But in protocols not explicitly specifying data units (like [VISS](https://raw.githack.com/w3c/automotive/gh-pages/spec/VISSv2_Core.html))
it is expected that `Vehicle.Speed` is sent and received as `km/h` (without scaling or offset).

In some cases it is natural to omit the data unit. This concerns typically signals where datatype `string` is used,
but also signals where the value just represents a number (dimensionless quantities), like in the example below:

```
Vehicle.Cabin.DoorCount:
  datatype: uint8
  type: attribute
  default: 4
  description: Number of doors in vehicle.
```
### Logical Data Units

VSS supports `percent` as data unit, typically with 0 to 100% as the allowed range.
In some cases, the definition on how to calculate the signal value is obvious, like for `Vehicle.Powertrain.FuelSystem.Level`
below. It is likely that all VSS users will calculate fuel level in the same way, i.e. the meaning of a fuel level of 50%
is well agreed, the liters of fuel in the tank is exactly 50% of nominal capacity.

```
Vehicle.Powertrain.FuelSystem.Level:
  datatype: uint8
  type: sensor
  unit: percent
  min: 0
  max: 100
  description: Level in fuel tank as percent of capacity. 0 = empty. 100 = full.

```

In other cases, the formula for calculating the signal is not obvious and is not specified in VSS. A typical example is shown below for clutch wear.
While most VSS users likely can agree that a brand new clutch shall have 0 as "ClutchWear",
the exact formula for calculating clutch wear for a used clutch will likely be vehicle specific.
Some vehicles might monitor actual wear, others might estimate it based on vehicle usage.
This is in VSS called a logical range, a VSS user knows what range to use but are free to define the formula for calculating the value.
Values from different vehicles (of different make/model) can not always be compared, as the formula used for calculation may differ.

```
Vehicle.Powertrain.Transmission.ClutchWear:
  datatype: uint8
  type: sensor
  unit: percent
  max: 100
  description: Clutch wear as percent. 0 = no wear. 100 = worn.
```


## List of supported Data Unit

The VSS syntax does not in itself specify what units can be used, the unit attribute as declared for signals in *.vspec files is optional and can contain an arbitrary string value.
[VSS-Tools](https://github.com/COVESA/vss-tools) however require that all units used are defined.
Units are defined by including them in a unit file with syntax as described below.
One or more unit files can be specified by the `-u` parameter and, if not given, the tools search for a file `units.yaml`
in the same directory as the root *.vspec file.

For the VSS standard catalog the VSS-project has defined a set of units that can be used for signals in the VSS standard catalog.
This list is composed of definitions according to International Units (SI) and few automotive-specific units:
[Specification](https://www.iso.org/standard/30669.html), [Wikipedia](https://en.wikipedia.org/wiki/International_System_of_Units)

The VSS list of units for the standard catalog exists in [units.yaml](https://github.com/COVESA/vehicle_signal_specification/blob/master/spec/units.yaml).


## Unit file syntax

Unit files follow the syntax defined below:

```
[
 <vss-unit-identifier>: # Typically unit abbreviation, like km/h or mm, but
    definition: <string>
    [unit: <string>] # Full name of unit, optional, if not given assumed to be equal to vss-unit-identifier
    quantity: <string> # Quantity of the unit.
    [allowed-datatypes] : ['numeric', 'string', uint8', ...]] # Allowed datatypes in VSS standard catalog
    [deprecation: <reason>]
]*
```

The VSS term `quantity` corresponds roughly to the term `quantity` as defined in for example ISO 80000.
Typical example are `length`, `mass` and `velocity` that all can be expressed in SI-units.
However, from a VSS perspective quantities do not need to correspond to physical quantities.
It could be an arbitrary term, but it is generally expected that it is possible to convert between values
using different units but defined with the same quantity.

Example:

```
m:
  definition: Length measured in meters
  unit: meter
  quantity: length
  allowed-datatypes: ['numeric']

mm:
  definition: Length measured in millimeters
  unit: millimeter
  quantity: length
  allowed-datatypes: ['numeric']
```

As `m` and `mm` are defined with the same quantity it is expected that you can convert a value from `m` to `mm`.

The `allowed-datatypes` attributes can be used to specify which VSS datatypes can contain values of a particular unit.
For most units the symbolic datatype `numeric` meaning any float or integer datatype can be used.
As an example, both `uint8` and `float` can be used to represent a length value.
If using `uint8` you will have range restrictions, but that might be acceptable for some signals.
For some units more specific datatype restrictions are relevant. Some examples:

* A date/time expressed in ISO 8061 format can only be represented as a string
* A UNIX Timestamp signal must be at least 32 bit unsigned to be able to handle date/time after year 2038.

The `deprecation` keyword can be used to indicate that a specific unit may be removed in the future.
Tooling shall preferably give a warning if a signal uses a deprecated unit or the unit used belongs to a deprecated quantity.
The reason should preferably list when and why the unit is deprecated, a hypothetical example is given below:

```

  inch:
    definition: Distance measured in inches
    unit: inch
    quantity: distance
    deprecation: V5.0 replaced by 'in'
  in:
    definition: Distance measured in inches
    unit: inch
    quantity: distance
```


The unit syntax has recently been changed. To simplify transition to the new syntax it is recommended that
tooling also supports unit files using the old syntax described below.

```
units:
  [
    <vss-unit-identifier>: # Typically unit abbreviation, like km/h or mm, but
      label: <string> # Replaced with "unit"
      description: <string> # Replaced with "definition"
      quantity: <string>
  ]*
```

## Quantity file syntax


Defing quantities is recommended, but currently optional for backward compatibility reasons.
If tooling supports quantity files it can verify that all units provided in unit files
use defined quantities.

```

  [
    <vss-quantity-identifier>: # Identifier preferably taken from a standard, like ISO 80000
      definition: <string>
      [remark: <string>] # remark as defined in for example ISO 80000
      [comment: <string>]
      [deprecation: <reason>]
  ]*

```


The VSS list of quantitiess for the standard catalog exists in [quantities.yaml](https://github.com/COVESA/vehicle_signal_specification/blob/master/spec/quantities.yaml).

## Defining custom units

It is possible to define custom units in a unit file.
Assume for instance you want to have a signal showing remaining range in [furlong](https://en.wikipedia.org/wiki/Furlong).
Then you could add an additional unit `furlong`. No need to specify `unit` or `symbol` as they equals the default (i.e. "furlong").
As this is unit not commonly used and not described in any standards, it might be relevant to describe how it can be converted to other units.
That is however only informative, as it a custom unit a downstream implementation supporting unit conversion may not support automatic conversion
of furlong to other units.

```
units:
  furlong:
    definition: Length measured in furlong, 1 furlong equals 201.1680 m
    quantity: length
    allowed-datatypes: ['numeric']
```
