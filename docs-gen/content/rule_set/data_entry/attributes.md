---
title: "Attributes"
date: 2019-08-04T12:37:31+02:00
weight: 4
---

An attribute is an entity that has a  default value, specified by
its ```default``` member.
The standard Vehicle Signal Specification does not include default values for all attributes.
If a default value has not been specified then the OEM must define a default value matching the actual vehicle.
If the standard defines a default value but it does not fit the actual vehicle,
then the OEM must override the standard default value.

Attribute values can also change, similar to sensor values.
The latter can be useful for attribute values that are likely to change during the lifetime of the vehicle.
However, attribute values should typically not change more than once per ignition cycle,
or else it should be defined as a sensor instead.

Below is an example of a complete attribute describing engine power

```YAML
MaxPower:
  datatype: uint16
  type: attribute
  default: 0
  unit: kW
  description: Peak power, in kilowatts, that engine can generate.
```

It is possible to give default values also for arrays. In this case square brackets shall be used. The value for each element in the array shall be specified. The size of the array is given by the number of elements specified within the square brackets.

Example 1: Empty Array

```YAML
  default: []
```

Example 2: Array with 3 elements, first element has value 1, second element value 2, third element value 0

```YAML
  default: [1, 2, 0]
```

Full example, array with two elements, first with value2, second with value 3:

```YAML
SeatPosCount:
  datatype: uint8[]
  type: attribute
  default: [2, 3]
  description: Number of seats across each row from the front to the rear
```
