---
title: "Overview"
date: 2019-07-30T14:46:01+02:00
weight: 1
chapter: false
---

## What is VSS?
The Vehicle Signal Specification introduces a domain taxonomy for vehicle signals.
In short this means that VSS introduces:

* A syntax for defining vehicle signals in a structured manner.
* A catalog of signals related to vehicles.

It can be used as standard in automotive applications to communicate information
around the vehicle, which is semantically well defined. It focuses on vehicle
signals, in the sense of classical attributes, sensors and actuators with the raw data
communicated over vehicle buses and data which is more commonly associated with
the infotainment system alike.

A standardized vehicle data specification allows an industry actor to use a
common naming space for communication and, ultimately, abstracts underlying
vehicle implementation details.

While the data in the VSS standard catalog aims to be vendor-independent,
vendor specific extensions and adaptations complying with the VSS syntax rules can be specified
(see [Overlays](/vehicle_signal_specification/docs-gen/content/rule_set/overlay.md).

### What's in
* Standardized data definition for vehicle signals.
* Same semantic understanding across different domains.
* Basic definition for interfaces working on vehicle data (w3c, etc.).

### What's out
* Everything outside the vehicle signal domain (customer, weather, etc.).
* Concrete interface definition.

## Example
The figure below shows an example snapshot of a generated tree of the
specification. The leafs contain the actual information as shown in the figure.
Before going into detail of the specification, let's dig deeper into taxonomies.

![Example tree](/vehicle_signal_specification/images/tree.png?classes=shadow&width=60pc)

## VSS usage for other domains

The VSS catalog focuses on signals related to vehicles.
It is not the intention of the VSS project to add signals for other domains.
The syntax used for defining VSS signals and related tooling could however be used to define similar signal trees
for other domains.
