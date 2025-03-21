---
title: "VSS Extension Profiles"
date: 2023-05-18T13:31:46+0000
chapter: false
weight: 10
---

The VSS syntax specifies a set of attributes that a VSS datapoint must have or can have.
Correct use of those attributes are checked by [VSS-Tools](https://github.com/COVESA/vss-tools/).
It is allowed to use additional attributes to define additional characteristics of VSS datapoints.
This could for example be useful for defining deployment-related data, like information on how a datapoint
shall be stored or transmitted.
This information typically does not fit in the standard catalog, but could be provided in a use-case specific
[overlay](../../rule_set/overlay.md).


A simple example could be:

```yaml
Vehicle.Speed:
    type: sensor
    unit: "km/h"
    datatype: float
    interval_ms: 1000
    source: "ecu0xAA"
```

... to define source and update interval of the VSS `Vehicle.Speed` datapoint for a specific deployment.
VSS-Tools has a [mechanism](https://github.com/COVESA/vss-tools/blob/master/docs/vspec.md#handling-of-overlays-and-extensions)
to consider provided extra attributes.

Users of VSS often need the same type of additional data, and for that reason it has been decided that the COVESA VSS-project will maintain a list of extension profiles.
An extension profile describes how VSS extended attributes can be used to provide additional information in a specific area to VSS datapoints.
Potential examples could include network serialization, security attributes and safety attributes.
They shall as of today not be seen as "standardized profiles" or "recommended profiles".

The extension profiles may be defined within the [VSS repository](https://github.com/COVESA/vehicle_signal_specification) or somewhere else.
Extension profiles defined within the [VSS repository](https://github.com/COVESA/vehicle_signal_specification) are managed like all other assets within the repository,
i.e. if someone want to contribute or change an extension profile they will need to create a Pull Request which then will be discussed within the project.


## VSS Extension Profiles

* [Eclipse Kuksa VSS-DBC mapping](https://github.com/eclipse-kuksa/kuksa-can-provider/tree/main/mapping)
* [VSS Winnie the Pooh Extension Profile](template.md)
