---
title: "Sensors & Actuators"
date: 2019-08-04T12:37:03+02:00
weight: 3
---

Sensors are signals to read values of properties in a vehicle. Values of signals typically change over time. Reading a sensor shall return the current actual value of the related property, e.g. the current speed or the current position of the seat. 

Actuators are used to control the desired value of a property. Some properties in a vehicle cannot change instantly. A typical example is position of a seat or a window. Reading a value of an actuator shall return the current actual value, e.g. the current position of the seat, rather than the wanted/desired position. A typical example could be if someone wants to change the position of a seat from 0 to 100. This can be changed by setting the corresponding actuator to 100. If the actuator is read directly after the set request it will still return 0 as it might take some seconds before the seat reaches the wanted position of 100. If the seat by some reason is blocked or cannot be moved due to safety reasons it might never reach the wanted position. It is up to the vehicle to decide how long time it shall try to reach the desired value and what to do if it needs to give up.

A data entry for a sensor or actuator defines its members. A data
entry example is given below:

```YAML
Speed:
  type: sensor
  description: The vehicle speed, as measured by the drivetrain.
  datatype: uint16
  unit: km/h
  min: 0
  max: 300
```

**```Drivetrain.Transmission.Speed```**  
Defines the dot-notated name of the data entry. Please note that
all parental branches included in the name must be defined as well.

**```type```**  
Defines the type of the node. This can be `branch`,
`sensor`, `actuator` or `attribute`.

**```description```**  
A description string to be included (when applicable) in the various
specification files generated from this data entry.

**```datatype```**  
The string value of the type specifies the scalar type of the data entry
value. See [data type](#data-type) chapter for a list of available types.

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
