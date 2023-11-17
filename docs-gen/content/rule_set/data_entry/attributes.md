---
title: "Attributes"
date: 2019-08-04T12:37:31+02:00
weight: 40
---

An attribute is a signal definition that has a default value, specified by
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
  identifier: Vehicle.Powertrain.CombustionEngine.MaxPower
  elementType: SignalType
  featureOfInterest: Vehicle.Powertrain.CombustionEngine
  property: DataProperty.MaximumPower
  default: 0
  unit: kW
  definition: The maximum power that a combustion engine can generate
  description: Peak power, in kilowatts, that engine can generate.
```

The following elements are defined:

**`MaxPower`**
The list element name defines the leaf node of the dot-notated signal name, which generally corresponds to the property.

**`datatype:`**
A classification that prescribes which values a data element can take and what type of mathematical, relational or logical operations 
can be applied to them.  See [Data Types](/vehicle_signal_specification/rule_set/data_entry/data_types/) 

**```type```**
The value ```attribute``` specifies that this signal may have a default value.

**```identifier```** *[optional]*
A set of characters that uniquely identifies the signal.  This is generally the branch and the property.

**```elementType```** *[optional]*
A type that classifies the attribute in regards to the Vehicle Signal domain
- ```SignalType``` The entry defines a property of a feature of interest.

**```featureOfInterest```** *[optional]*
The identifier of the physical object whose properties can be observed and possibly manipulated by signals of this type

**```property```** *[optional]*
The identifier of the property being reported by signals of this type

**```unit```**
The unit of measurement that the data entry has. See [Data Unit Types](/vehicle_signal_specification/rule_set/data_entry/data_unit_types/)
chapter for a list of available unit types.

**```definition```*** *[optional]*
A formal specification that includes the necessary and sufficient conditions for distinguishing this signal definition from anything else.  It is similar to a dictionary definition, and the conditions put forth can translate to formal axioms in an ontology and can be used for inferencing and automation.

**```description```**
Describes the meaning and content of the property.  Descriptions can include any kind of information that helps humans conceptualize the entry, such as examples, physical properties, etc.
Recommended to start with a capital letter and end with a dot (`.`).

**```default```**
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

Using default values for structs is not allowed!
