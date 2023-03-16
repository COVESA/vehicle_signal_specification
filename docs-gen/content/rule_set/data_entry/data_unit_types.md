---
title: "Data Unit Types"
date: 2019-08-04T12:36:12+02:00
weight: 20
---

## Introduction to Data Unit Types in VSS

It is in VSS possible for signals to specify a unit of measurement from a list of predefined data unit types.
For most signals in the VSS standard catalog, a data unit type has been selected. A typical example is `Vehicle.Speed`, as shown below.

```
Vehicle.Speed:
  datatype: float
  type: sensor
  unit: km/h
  description: Vehicle speed.
```

The ambition when selecting data unit types for signals in VSS standard catalog has been to use either a unit based on SI-units,
or a unit commonly used within the vehicle industry. For the `Vehicle.Speed` example above this means that `km/h` has been selected,
even if `m/s` from an SI-perspective would have been a better choice.

It must be noted that the selected unit does not imply that the value of `Vehicle.Speed` always needs to be sent or visualized
as `km/h` (with float as datatype). A user interface or API may show or request vehicle speed in any unit it likes,
and a transport protocol may send speed in another unit, possibly also involving scaling and offset.
But in protocols not explicitly specifying data unit types (like [VISS](https://raw.githack.com/w3c/automotive/gh-pages/spec/VISSv2_Core.html))
it is expected that `Vehicle.Speed` is sent and received as `km/h` (without scaling or offset).

In some cases it is natural to omit the data unit type. This concerns typically signals where data type `string` is used,
but also signals where the value just represents a number, like in the example below:

```
Vehicle.Cabin.DoorCount:
  datatype: uint8
  type: attribute
  default: 4
  description: Number of doors in vehicle.
```
### Logical Data Unit Types

VSS supports `percent` as data unit type, typically with 0 to 100% as the allowed range.
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


## List of supported Data Unit Types

This list composed with definition according to International Units (SI) and few automotive specific units: [Specification](https://www.iso.org/standard/30669.html), [Wikipedia](https://en.wikipedia.org/wiki/International_System_of_Units)


Unit type     | Domain                          | Description
:-------------|:--------------------------------|:-------------
mm            | Distance                        | Distance measured in millimeters
cm            | Distance                        | Distance measured in centimeters
m             | Distance                        | Distance measured in meters
km            | Distance                        | Distance measured in kilometers
inch          | Distance                        | Distance measured in inches
km/h          | Speed                           | Speed measured in kilometers per hours
m/s           | Speed                           | Speed measured in meters per second
m/s^2         | Acceleration                    | Acceleration measured in meters per second squared
cm/s^2        | Acceleration                    | Acceleration measured in centimeters per second squared
ml            | Volume                          | Volume measured in milliliters
l             | Volume                          | Volume measured in liters
cm^3          | Volume                          | Volume measured in cubic centimeters
celsius       | Temperature                     | Temperature measured in degree celsius
degrees       | Angle                           | Angle measured in degrees
degrees/s     | Angular Speed                   | Angular speed measured in degrees per second
W             | Power                           | Power measured in watts
kW            | Power                           | Power measured in kilowatts
PS            | Power                           | Power measured in horsepower
kWh           | Energy Consumption              | Energy consumption measured in kilowatt hours
g             | Weight                          | Mass measured in grams
kg            | Weight                          | Mass measured in kilograms
lbs           | Weight                          | Mass measured in pounds
V             | Electric Potential              | Electric potential measured in volts
A             | Electric Current                | Electric current measured in amperes
Ah            | Electric Charge                 | Electric charge measured in ampere hours
ms            | Time                            | Time measured in milliseconds
s             | Time                            | Time measured in seconds
min           | Time                            | Time measured in minutes
h             | Time                            | Time measured in hours
day           | Time                            | Time measured in days
weeks         | Time                            | Time measured in weeks
months        | Time                            | Time measured in months
years         | Time                            | Time measured in years
UNIX Timestamp| Time                            | Unix time is a system for describing a point in time. It is the number of seconds that have elapsed since the Unix epoch, excluding leap seconds.
mbar          | Pressure                        | Pressure measured in millibars
Pa            | Pressure                        | Pressure measured in pascal
kPa           | Pressure                        | Pressure measured in kilopascal
stars         | Rating                          | Rating measured in stars
g/s           | Mass per time                   | Mass per time measured in grams per second
g/km          | Mass per distance               | Mass per distance measured in grams per kilometers
kWh/100km     | Energy Consumption per distance | Energy consumption per distance measured in kilowatt hours per 100 kilometers
ml/100km      | Volume per distance             | Volume per distance measured in milliliters per 100 kilometers
l/100km       | Volume per distance             | Volume per distance measured in liters per 100 kilometers
l/h           | Flow                            | Flow measured in liters per hour
mpg           | Distance per Volume             | Distance per volume measured in miles per gallon
N             | Force                           | Force measured in newton
Nm            | Torque                          | Torque measured in newton meters
rpm           | Rotational Speed                | Rotational speed measured in revolutions per minute
Hz            | Frequency                       | Frequency measured in hertz
ratio         | Relation                        | Relation measured as ratio
percent       | Relation                        | Relation measured in percent
... | ... | ...

VSS tooling use the list specified in [config.yaml](https://github.com/COVESA/vss-tools/blob/master/vspec/config.yaml) to validate that only supported types are used in the signal specification.
