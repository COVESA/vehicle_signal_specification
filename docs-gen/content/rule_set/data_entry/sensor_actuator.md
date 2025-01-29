---
title: "Sensors, Actuators and Attributes"
date: 2019-08-04T12:37:03+02:00
weight: 30
---

# Property Types Overview

## `sensor` type
Sensors are properties that, from a VSS-perspective, are read-only.
The values of a `sensor` property typically change over time and within an ignition cycle (i.e., a driving journey).
Reading a `sensor` shall return the actual value of the related property (e.g., the current speed or the current position of the seat).

## `actuator` type
Similarly, actuators are properties that, from a VSS-perspective, can be read and written.
Actuators in VSS can be used to represent both the actual value (i.e., read) and the desired value of a property (i.e., write).
The value written to a property that involves a slow mechanical action or certain motion might not be immediately reflected in a read operation if the property value is read immediately after a write operation.
Some properties like `Window.Position` or `Seat.Position` are clear examples of things that might not change instantly.
Hence, the written value (i.e., the desired target) and actual value may differ.
Unless otherwise specified it is assumed that APIs implementing access to VSS data shall return actual value for read/subscribe-operations,
and update the desired value for write-operations.

A typical example could be if someone wants to change the position of a seat from 0 to 100. This can be changed by setting the corresponding actuator to 100.
If the actuator is read directly after the set request it will still return 0 as it might take some seconds before the seat reaches the wanted position of 100.
If the seat by some reason is blocked or cannot be moved due to safety reasons it might never reach the wanted position.
It is up to the vehicle to decide how long time it shall try to reach the desired value and what to do if it needs to give up.

## `attribute` type
Attributes are properties whose values do not change within an ignition cycle (i.e., a driving journey).
In other words, characteristics that are often static.
For example, the color and model of a car.
If a default value has not been specified, then the user of the specification must define the associated value matching the actual vehicle.
For example, the specification might have the attribute `Brand` without a default value associated.
Then, the user of the specification is responsible to assign `Some example brand` as the value for that attribute.
If the standard defines a default value but it does not fit the actual vehicle,
then the OEM must override the standard default value.

Attribute values can also change, similar to sensor values.
The latter can be useful for attribute values that are likely to change during the lifetime of the vehicle.
However, attribute values should typically not change more than once per ignition cycle,
or else it should be defined as a sensor instead.

# Data Entry

A data entry for a signal defines its members. A data
entry example is given below:

```yaml
Vehicle.Speed:
  type: sensor
  datatype: float
  unit: km/h
  description: Vehicle speed.
```

Each data entry has a name, in the example above `Vehicle.Speed`.
VSS use a dot-notated name style where the full path of a data entry consists of all parent branches from the root node separated by dots and at the end the name of the data entry itself. In the standard VSS catalog the root node is called `Vehicle`.

When using `*.vspec` files to define a VSS catalog it is not necessary to give the full dot-notated name for each data-entry, as the
`*.vspec` format supports [includes](../includes/) that can be used to append entries to a specific branch.

In addition to `sensor`, `actuator`and `attribute` VSS also support entries to describe [struct data types](/vehicle_signal_specification/rule_set/data_entry/data_types_struct/). The information on data entry attributes below is partially valid also for structs.

## Mandatory Data Entry Attributes

This is the list of attributes that must be specified for every data entry.

Attribute    | Description                 | Comment
-------------|-----------------------------|--------
`type`       | Defines the type of the node. This can be `branch`, `sensor`, `actuator` or `attribute`.
`datatype`   | Specifies the scalar type of the data entry value.  See [datatype](/vehicle_signal_specification/rule_set/data_entry/data_types/) chapter for a list of available datatypes. Shall not be used for `branch` entries.|
`description`| Describes the meaning and content of the signal. The `description`shall together with other members like `datatype` and `unit` provide sufficient information to understand what the signal contains and how signal values shall be constructed or interpreted. Recommended to start with a capital letter and end with a dot (`.`).

## Optional Data Entry Attributes

In additon to the mandatory attributes some optional attributes have been defined.
There may be additional constraints on their usage not specified in the table below.

Attribute    | Description                 | Comment
-------------|-----------------------------|--------
`comment`    | A comment can be used to provide additional informal information on a signal. This could include background information on the rationale for the signal design, references to related signals, standards and similar. Recommended to start with a capital letter and end with a dot (`.`). | *since version 3.0*
`min`        | The minimum value, within the interval of the given `datatype`, that the data entry can be assigned. If omitted, the minimum value will be the "Min" value for the given datatype. Cannot be specified if `allowed` is defined for the same data entry.
`max` | The maximum value, within the interval of the given `datatype`, that the data entry can be assigned. If omitted, the maximum value will be the "Max" value for the given datatype. Cannot be specified if `allowed` is defined for the same data entry.
`unit` | The unit of measurement that the data entry has. See [Data Units](/vehicle_signal_specification/rule_set/data_entry/data_units/) chapter for a list of available units. Cannot be specified if `allowed` is defined for the same data entry.
`pattern` | Can be used for datatype `string` and `string[]`  to specify a regular expression that limits allowed values for the data entry. The expression must be supported by [Python Regular Expressions](https://docs.python.org/3/howto/regex.html) | *since version 6.0*
`default` | Default value for the data entry. See [Default Values](/vehicle_signal_specification/rule_set/data_entry/default/).
`allowed`| Allowed values for the data entry. See [Allowed Values](/vehicle_signal_specification/rule_set/data_entry/allowed/).
`arraysize`| If the `datatype`is an array, this atrribute can be used to specify the size of the array. See [datatype](/vehicle_signal_specification/rule_set/data_entry/data_types/)
