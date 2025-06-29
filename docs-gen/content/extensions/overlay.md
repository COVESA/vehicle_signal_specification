---
title: "VSS Overlay Mechanism"
weight: 7
---

VSS defines the standard catalog for vehicle signals independent of the used protocol and environment.
In order to adopt the specification we realize that certain additions and modifications to the standard catalog are necessary.
**VSS Overlays** are meant to bring you a standardized way of handling those changes.

The following features with the intended usage patterns are currently supported:
1. **Adding new nodes:** By adding nodes the standard catalog can be extended with proprietary concepts.
1. **Deleting nodes:** Deleting nodes not relevant for the vehicle.
1. **Changing the value of existing metadata:** The standard catalog defines metadata based on what is assumed to be an average vehicle.
Configurations may differ slightly (e.g. the instantiation of number of available seats), or special situations that require a (limited) modification of existing metadata.
1. **Adding new key/value pairs as additional metadata:**
Extending the model with richer information is a fundamental feature enabled by the layer concept.  For example, deploying VSS into a specific scenario or with a particular binding/technology often needs some additional information.
1. **Multiple layer files:** VSS layers can be split into several files in order to clearly separate concerns. Layering allows all the features above to be applied in a composable manner. In order to keep a determinstic result a clear order has to remain.

### How does it work?

Simply said, the tooling accepts, *n* additional spec files, next to the original
specification file, which can overwrite or extend data in the VSS tree defined by
the original specification. Before you start you should know:
- **Overlay files do not need to be valid specification files by themselves but the merged result counts**
  In practice that means, that nodes in the overlay files (e.g. branches) do not need
  to specify all the required attributes (like `type`, `description`, ...) if they are supposed to overwrite certain attributes
  of an already existing branch in vss.
- **You can omit parent branches if there is no need to change them**
  However, the tooling does not allow implicit branches by design.
  So if you are creating new branches in overlays they need to be correctly linked
  to an existing branch in vss.
- **Order matters.** The order on how the overlay files are passed in the cli
  command matters! An example is shown in the figure below.

The Figure below illustrates an example of the main specification and two
separate overlay files, an example call of the tooling and the resulting tree.

![Include directive](/vehicle_signal_specification/images/overlay.drawio.png)<br>
*Figure: Overview on how overlays work within VSS*


```yaml
# In this overlay all parent branches are included.
# If you do not want to change existing branches, it is not necessary to specify them.
# Also note that some elements are missing required attributes (description)
# but since those elements will be merged with the ones in VSS, the result is valid.

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

```yaml
# This overlay would not be valid on its own since `NewBranch` is missing.
# When being applied in conjunction with the previous overlay, it would create
# `HasNewAttribute` accordingly.

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

### Node content in Overlays

If you are adding a node you need to specify all attributes required for that node type.
If you are changing an existing node you typically only need to specify the name and what you would like to overwrite,
like in the `Vehicle.Speed` example below. That also works for overwriting nodes that are created using `instances`.
`vss-tools` will then look up the node name and merges the attributes.

```yaml
# Type and Datatype not needed
Vehicle.Speed:
  unit: m/s

# Overwriting the unit of a node created by instances also works
Vehicle.Occupant.Row1.DriverSide.HeadPosition.Yaw:
  unit: mm
```

### Deleting nodes

It is possible to delete nodes using the `delete` attribute.
You can delete indidvidual signals, branches, instances or a particular signal in a particular instance.
A few examples are shown below.

```YAML
# Removing IsChildLockActive for DriverSide on Second Row
Vehicle.Cabin.Door.Row2.DriverSide.IsChildLockActive:
  datatype: boolean
  type: sensor
  delete: true

# Removing Window for all Door instances
Vehicle.Cabin.Door.Window:
  delete: true

# Removing Vehicle.Speed
Vehicle.Speed:
  delete: true
```

When using the `delete` argument vss-tools will print a summary on how many nodes that are removed.

```bash
Nodes deleted, given=6, overall=18
```

The number for `given` represents number of nodes (branches/sensors/actuators/attributes) explicitly removed.
The `overall` number represents total number, including child nodes for explicitly removed branches.
More detailed output is given in debug mode.
