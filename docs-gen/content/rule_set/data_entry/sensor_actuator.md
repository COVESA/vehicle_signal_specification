---
title: "Sensors & Actuators"
date: 2019-08-04T12:37:03+02:00
weight: 3
---
A data entry defines a single sensor/actuator and its members. A data
entry example is given below:

```YAML
Speed:
  type: sensor
  description: The vehicle speed.
  comment: For engine speed see Vehicle.Powertrain.CombustionEngine.Engine.Speed.
  datatype: float
  unit: km/h
  min: 0
  max: 300
```

**```Drivetrain.Transmission.Speed```**  
Defines the dot-notated name of the data entry. Please note that
all parental branches included in the name must be defined as well.

**```type```**  
Defines the type of the node. This can be ```branch```,
```sensor```, ```actuator```, ```stream``` or attribute.

**```datatype```**  
The string value of the type specifies the scalar type of the data entry
value. See [data type](#data-type) chapter for a list of available types.

**```description```**  
Describes the meaning and content of the signal.
The `description`shall together with other mandatory members like `datatype` and `unit` provide sufficient information
to understand what the signal contains and how signal values shall be constructed or interpreted.
Recommended to start with a capital letter and end with a dot (`.`).

**```comment ```**  *[optional]* `since version 3.0`
A comment can be used to provide additional informal information on a signal.
This could include background information on the rationale for the signal design,
references to related signals, standards and similar.
Recommended to start with a capital letter and end with a dot (`.`).

**```min```** *[optional]*  
The minimum value, within the interval of the given ```type```, that the
data entry can be assigned.
If omitted, the minimum value will be the "Min" value for the given type.
Cannot be specified if ```enum``` is specified for the same data entry.

**```max```** *[optional]*  
The maximum value, within the interval of the given ```type```, that the
data entry can be assigned.
If omitted, the maximum value will be the "Max" value for the given type.
Cannot be specified if ```enum``` is specified for the same data entry.

**```unit```** *[optional]*    
The unit of measurement that the data entry has. See [Unit
Type](#data-unit-type) chapter for a list of available unit types. This
cannot be specified if ```enum``` is specified as the signal type.

**```sensor```** *[optional]*  
The sensing appliance used to produce the data entry.

**```actuator```** *[optional]*  
The actuating appliance consuming the data entry.
