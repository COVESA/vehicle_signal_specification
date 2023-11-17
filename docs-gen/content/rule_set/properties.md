---
title: "Property Entry"
date: 2023-11-07
weight: 1
---

A property entry describes an attribute, quality, or characteristic of a feature of interest. There are two flavors of properties:
- ```DataProperty```: A property whose values are literals
- ```ObjectProperty```: A property whose values are an object, often represented as an element in an enumeration

A ```data property``` entry is exemplified below.  A data property is constrained by a datatype and (optionally) unit, min, and/or max.

```YAML
DataProperty.RotationalSpeedPercent:
  type: dataProperty
  identifier: DataProperty.RotationalSpeedPercent
  elementType: DataProperty
  datatype: uint8
  unit: percent
  min: 0
  max: 100
  definition: A percent of circular movements around a central axis during a particular
              time interval compared to the maximum possible or allowed
  description: The speed of a rotating part, such as the blades in a fan, on a scale of
               0 to 100 where 0 = still or off, and 100 = max or full
```

The following elements are defined:

**`DataProperty.RotationalSpeedPercent:`**
The list element name defines the property identifier.  Properties are identified by their element type and name.  

**```type```**
The value ```dataProperty``` specifies that this is a data property entry.

**```identifier```**
A set of characters that uniquely identifies the property.  This is redundant to the heading and added for consistency with branches and signals.

**```elementType```**
A type that categorizes whether values for the property are literals or objects.
- ```DataProperty```: The property takes literals as values.
- ```ObjectProperty```: The property takes pre-defined objects, such as enumeration elements, as values.

**```datatype```**
A classification that prescribes which values a data element can take and what type of mathematical, relational or logical operations 
can be applied to them.  See [Data Types](/vehicle_signal_specification/rule_set/data_entry/data_types/)

**```unit```** *[optional]*
The unit of measurement that the data entry has. See [Data Unit Types](/vehicle_signal_specification/rule_set/data_entry/data_unit_types/)
chapter for a list of available unit types. This

**```min```** *[optional]*
The minimum value, within the interval of the given ```type```, that the
data entry can be assigned.
If omitted, the minimum value will be the "Min" value for the given type.

**```max```** *[optional]*
The maximum value, within the interval of the given ```type```, that the
data entry can be assigned.
If omitted, the maximum value will be the "Max" value for the given type.

**```definition```**
A formal specification that includes the necessary and sufficient conditions for distinguishing this property from anything else.  It is similar to a dictionary definition, and the conditions put forth can translate to formal axioms in an ontology and can be used for inferencing and automation.

**```description```** *[optional]*
Describes the meaning and content of the property.  Descriptions can include any kind of information that helps humans conceptualize the entry, such as examples, sybmols, usage guidance, etc.
Recommended to start with a capital letter and end with a dot (`.`).

An ```object property``` entry is exemplified below.  The ```allowed``` field enumerates the possible values.

```YAML
ObjectProperty.VerticalOrientation:
  type: objectProperty
  identifier: ObjectProperty.VerticalOrientation
  elementType: ObjectProperty
  allowed: ['UP', 'MIDDLE', 'DOWN']
  definition: An ordinal category indicating a position on, or direction of, the z (vertical) axis
  description: Typical examples include whether a vent it pointing up or down, or the pitch of a vehicle
```
**`ObjectProperty.VerticalOrientation:`**
The list element name defines the property identifier.  Properties are identified by their element type and name.  

**```type```**
The value ```objectProperty``` specifies that this is an object property entry.

**```identifier```** 
A set of characters that uniquely identifies the ```property```.  This is redundant to the heading and added for consistency with branches and signals.

**```elementType```** 
A type that categorizes whether values for the property are literals or objects.
- ```DataProperty```: The property takes literals as values
- ```ObjectProperty```: The property takes a pre-defined objects, such as enumeration elements, as values.

**```allowed```** 
The set of values allowed for this object property

**```definition```***
A formal specification that includes the necessary and sufficient conditions for distinguishing this property from anything else.  It is similar to a dictionary definition, and the conditions put forth can translate to formal axioms in an ontology and can be used for inferencing and automation.

**```description```** [optional]* 
Describes the meaning and content of the property.  Descriptions can include any kind of information that helps humans conceptualize the entry, such as examples, sybmols, usage guidance, etc.
Recommended to start with a capital letter and end with a dot (`.`).

