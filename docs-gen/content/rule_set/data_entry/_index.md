---
title: "Data Entry"
date: 2019-08-04T11:11:30+02:00
chapter: true
weight: 2
---

# Data Entry
Leaf nodes of the tree contain metadata describing the data associated to the node.
In order to help application developers, who are using the specification, it makes a distinction between three types of signals -
[```sensor```](/vehicle_signal_specification/rule_set/data_entry/sensor_actuator/),
[```actuator```](/vehicle_signal_specification/rule_set/data_entry/sensor_actuator/) - and
[```attribute```](/vehicle_signal_specification/rule_set/data_entry/attributes/).
The difference between sensors/actuators and attributes is that sensors/actuators typically have
a publisher (or producer) that updates the signal value continuously when a change occur while an
attribute has a set value that should typically not change more than once per ignition cycle.

Examples and more information you'll find in the
[Sensors & Actuators chapter](/vehicle_signal_specification/rule_set/data_entry/sensor_actuator/) and
[Attributes chapter](/vehicle_signal_specification/rule_set/data_entry/attributes/).
