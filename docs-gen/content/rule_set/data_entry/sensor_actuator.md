---
title: "Sensors & Actuators"
date: 2019-08-04T12:37:03+02:00
weight: 30
---

Sensors are signals to read values of properties in a vehicle. Values of sensors typically change over time. Reading a sensor shall return the current actual value of the related property, e.g. the current speed or the current position of the seat.

Actuators are used to control the desired value of a property. Some properties in a vehicle cannot change instantly. A typical example is position of a seat or a window. Reading a value of an actuator shall return the current actual value, e.g. the current position of the seat, rather than the wanted/desired position. A typical example could be if someone wants to change the position of a seat from 0 to 100. This can be changed by setting the corresponding actuator to 100. If the actuator is read directly after the set request it will still return 0 as it might take some seconds before the seat reaches the wanted position of 100. If the seat by some reason is blocked or cannot be moved due to safety reasons it might never reach the wanted position. It is up to the vehicle to decide how long time it shall try to reach the desired value and what to do if it needs to give up.

A data entry for a sensor or actuator defines its members. A data
entry example for a data property is given below:

```YAML
Speed:
  type: sensor
  identifier: Vehicle.Speed
  elementType: SignalType
  featureOfInterest: Vehicle
  property: DataProperty.Speed
  description: The vehicle speed.
  definition: The rate of change in the vehicle position per unit of time
  comment: For engine speed see Vehicle.Powertrain.CombustionEngine.Engine.Speed.
  datatype: float
  unit: km/h
  min: 0
  max: 300
```

**```Speed```**
Defines the dot-notated name of the data entry. Please note that
all parental branches included in the name must be defined as well.

**```type```**
Defines the type of the node.

**```identifier```** *[optional]*
A set of characters that uniquely identifies the signal.  This is generally the branch and the property.

**```elementType```** *[optional]*
A type that classifies the attribute in regards to the Vehicle Signal domain
- ```SignalType```: The entry defines a property of a feature of interest.

**```featureOfInterest```** *[optional]*
The identifier of the physical object whose properties can be observed and possibly manipulated by signals of this type

**```property```** *[optional]*
The identifier of the data property or object property being reported by signals of this type.
For data properties, the `property` itself has a `datatype` and optional constraints on `unit`, `min`, and `max`.  Those defined for the signal should correspond or provide some explanation of why they differ.  If `unit`, `min`, or `max` are omitted, they are assumed to default to those defined by the `property`.

**```description```**
Describes the meaning and content of the signal.
The `description`shall together with other mandatory members like `datatype` and `unit` provide sufficient information
to understand what the signal contains and how signal values shall be constructed or interpreted.
Recommended to start with a capital letter and end with a dot (`.`).


**```definition```*** *[optional]*
A formal specification that includes the necessary and sufficient conditions for distinguishing this signal definition from anything else.  It is similar to a dictionary definition, and the conditions put forth can translate to formal axioms in an ontology and can be used for inferencing and automation.

**```comment ```**  *[optional]* `since version 3.0`
A comment can be used to provide additional informal information on a signal.
This could include background information on the rationale for the signal design,
references to related signals, standards and similar.
Recommended to start with a capital letter and end with a dot (`.`).

**```datatype```**
The string value of the type specifies the scalar type of the data entry
value. See [data type](/vehicle_signal_specification/rule_set/data_entry/data_types/) chapter for a list of available types.

**```unit```** *[optional]*
The unit of measurement that the data entry has. See [Data Unit Types](/vehicle_signal_specification/rule_set/data_entry/data_unit_types/)
chapter for a list of available unit types. This
cannot be specified if ```allowed``` is defined as the signal type.

**```min```** *[optional]*
The minimum value, within the interval of the given ```type```, that the
data entry can be assigned.
If omitted, the minimum value will be the "Min" value for the given type.
Cannot be specified if ```allowed``` is defined for the same data entry.

**```max```** *[optional]*
The maximum value, within the interval of the given ```type```, that the
data entry can be assigned.
If omitted, the maximum value will be the "Max" value for the given type.
Cannot be specified if ```allowed``` is defined for the same data entry.


A data entry example for an object property is given below:
```YAML
AirDistribution:
  datatype: string
  type: actuator
  identifier: Vehicle.Cabin.HVAC.Station.AirDistribution
  elementType: SignalType
  featureOfInterest: Vehicle.Cabin.HVAC.Station
  property: ObjectProperty.VerticalDirection  
  allowed: ['UP', 'MIDDLE', 'DOWN']
  description: Direction of airstream
  definition: The course over which something moves from up to down
```

**```property```** *[optional]*
The identifier of the data property or object property being reported by signals of this type.
For object properties, the `property` itself has a set of `allowed` values.  Those defined for the signal should correspond or provide some explanation of why they differ.  If omitted, they are assumed to default to those defined by the `property`.