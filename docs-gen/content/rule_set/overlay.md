---
title: "Overlay"
date: 2019-08-04T12:46:30+02:00
weight: 7
---

VSS defines the standard catalog for vehicle signals independent of the used protocol and environment.
In order to adopt the specification we realize that certain additions and modifications to the standard catalog are necessary.
**VSS Overlays** are meant to bring you a standardized way of handling those changes.

The following features with the intended usage patterns are currently supported:
1. **Adding new nodes:** By adding nodes the standard catalog can be extended with proprietary concepts.
1. **Changing the value of existing metadata:** The standard catalog defines metadata based on what is assumed to be an average vehicle.
Configurations may differ slightly (e.g. the instantiation of number of available seats), or special situations that require a (limited) modification of existing metadata.
1. **Adding new key/value pairs as additional metadata:**
Extending the model with richer information is a fundamental feature enabled by the layer concept.  For example, deploying VSS into a specific scenario or with a particular binding/technology often needs some additional information.
1. **Multiple layer files:** VSS layers can be split into several files in order to clearly separate concerns. Layering allows all the features above to be applied in a composable manner. In order to keep a determinstic result a clear order has to remain.

### Scenarios for using Overlays

The standard catalog is specified within COVESA and defines a common view of the major
attributes, sensors and actuators of vehicles. This is used in many different scenarios,
protocols and environments. Additional meta data might be required for data-governance,
-quality or -sources. The instantiation of branches might not fit your vehicle.
Proprietary signals might be needed for extending the specification for your own use-cases.
Up to now you were on your own in these scenarios. Overlays give you the chance to change
and modify the standard catalog in a standardized way.

### How does it work?

Simply said, the tooling accepts, *n* additional spec files, next to the original
specification file, which can overwrite or extend data in the VSS tree defined by
the original specification.Before you start you should know:
- **Overlay-files have to be valid specification files by themselves.**
  In practice that means, that the path to a node has to be well defined.
- **You can omit parent branches if there is no need to change them**
  Tooling supports implicit branches.
- **Order matters.** The order on how the overlay files are called in the CLI
  command matters! An example is shown in the figure below.

The Figure below illustrates an example of the main specification and two
separate overlay files, an example call of the tooling and the resulting tree.

![Include directive](/vehicle_signal_specification/images/overlay.drawio.png)<br>
*Figure: Overview on how overlays work within VSS*


```YAML
# In this overlay all parent branches are included.
# That is not mandatory, as tooling supports implicit branches.

Vehicle:
    type: branch

Vehicle.Cabin:
    type: branch

Vehicle.Cabin.NewBranch: #< introduction of a new branch
    type: branch
    description: "new test branch"

Vehicle.Cabin.NewBranch.HasNewSignal: #< introduction of a new signal
    type: sensor
    description: "new test signal"
    datatype: int8

Vehicle.Cabin.Door:
    type: branch

Vehicle.Cabin.Door.IsOpen:
    type: sensor #< change of node type
    datatype: boolean
```
*File: overlay_1.vspec*

```YAML

# This overlay use implicit branches.
# This means that tooling will either reuse the existing Vehicle.Cabin.NewBranch,
# or if not found create it with default values.

Vehicle.Cabin.NewBranch.HasNewAttribute: #< ...with a new attribute
    type: attribute
    description: "new test attribute"
    datatype: string

Vehicle.Cabin.Door.IsOpen:
    type: sensor
    newKey: value  #< Add a new key to the node and add a value
    datatype: boolean

```
*File: overlay_2.vspec*

### Overlays in the standard catalog

With the feature of overlays, we introduced a new folder in the
repository called `overlays`. In there you'll find two additional folders:

* `profiles`: Larger overlays to adapt VSS to a specific vehicle category, like motorbikes.
* `extensions`: Smaller overlays typically to be applied after applying profiles (if any).

{{% notice warning %}}
**DISCLAIMER:** Use of overlays is a new concept for VSS.
The overlays in those folders shall currently be seen as examples only, and are not part of the official VSS specification.
{{% /notice %}}
