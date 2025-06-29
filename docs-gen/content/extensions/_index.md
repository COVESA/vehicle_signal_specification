---
title: "Extending and Customizing VSS"
chapter: false
weight: 27
---


The VSS-project is active in three areas:

* Defining a metamodel (syntax) for VSS datapoints.
* Defining the VSS Standard Catalog.
* Implementation of tooling ([VSS-Tools](https://github.com/COVESA/vss-tools)).

The VSS Standard Catalog defines a common view of the major
attributes, sensors and actuators of vehicles. This is used in many different scenarios,
protocols and environments. Additional meta data might be required for data-governance,
-quality or -sources. The instantiation of branches might not fit your vehicle.
Some signals in the VSS Signal Catalog may not be relevant or appropriate for your use-case,
and proprietary signals might be needed for extending the specification for your own use-cases


## General methods for extending and customizing VSS

Correct use of those attributes are checked by [VSS-Tools](https://github.com/COVESA/vss-tools/).
It is allowed to use additional attributes to define additional characteristics of VSS datapoints.
This could for example be useful for defining deployment-related data, like information on how a datapoint
shall be stored or transmitted.

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

The VSS-project defines the VSS Signal Catalog. It is possible that you need to adapt the content of the catalog for your deployment,
by adding, removing or changing signals.

As a VSS user you have in principle three methods for extending or customizing VSS

1. You can select to not use the VSS Standard Catalog, and instead use a catalog that you have defined yourself.
2. You can use a fork of the [VSS repository](https://github.com/COVESA/vehicle_signal_specification) and modify the contents as needed.
3. You can use the [VSS overlay mechanism](overlay.md) to define changes to be applied on top of the VSS Standard Catalog

The advantage with the third alternative compared to the second alternative is that it can give a separation between the basic model
and deployment information, and reduced risk for merge conflicts if upgrading to a new version of the VSS Standard Catalog.


## Extentions for extending VSS Signal Catalog with additional signals

With the feature of overlays, we introduced a new folder in the
repository called `overlays`. In there you'll find two additional folders with overlays:

* `profiles`: Vehicle profiles are larger overlays to adapt VSS to a specific vehicle category, like motorbikes.
* `extensions`: VSS Signal Catalog Extensions are smaller overlays typically to be applied after applying vehicle profiles (if any).

{{% notice warning %}}
**DISCLAIMER:**
The overlays in those folders shall currently be seen as examples only, and are not part of the official VSS specification.
{{% /notice %}}

## VSS Model Profiles

Users of VSS often need the same type of additional data, and for that reason it has been decided that the COVESA VSS-project will maintain a list of extension profiles.
A VSS Model Profile describes how VSS extended attributes can be used to provide additional information in a specific area to VSS datapoints.
Potential examples could include network serialization, security attributes and safety attributes.
They shall as of today not be seen as "standardized profiles" or "recommended profiles".

The extension profiles may be defined within the [VSS repository](https://github.com/COVESA/vehicle_signal_specification) or somewhere else.
Extension profiles defined within the [VSS repository](https://github.com/COVESA/vehicle_signal_specification) are managed like all other assets within the repository,
i.e. if someone want to contribute or change an extension profile they will need to create a Pull Request which then will be discussed within the project.

This information typically does not fit in the standard catalog, but could be provided in a use-case specific
[overlay](overlay.md).


### Existing VSS Model Profiles

* [Eclipse Kuksa VSS-DBC mapping](https://github.com/eclipse-kuksa/kuksa-can-provider/tree/main/mapping)
* [Cybersecurity Profile](cybersecurity_profile.md)
* [Network Serialization Profile](network_serialization_profile.md)
