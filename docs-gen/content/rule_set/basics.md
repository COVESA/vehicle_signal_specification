---
title: "Basic Rules"
date: 2019-08-04T13:05:11+02:00
weight: 1
---
## Specification format

The Vehicle Signal Specification domain specification consist of *vspec* files.
*vspec* files are YAML files following the rule set defined for VSS.
They also support the use of include directives to refer to other *vspec* files, much like ```#include``` in C/C++. .
Please note that, from a YAML perspective, the include directive is just another comment.

The file [VehicleSignalSpecification.vspec](https://github.com/COVESA/vehicle_signal_specification/blob/master/spec/VehicleSignalSpecification.vspec) serves as root
and includes other *vspec* files from the [VSS repository](https://github.com/COVESA/vehicle_signal_specification).

The raw specification files can with help of tools in the [vss-tools repository](https://github.com/COVESA/vss-tools) be converted to other formats that are more user friendly to read. Converted representations are also included as release artifacts for each [VSS release](https://github.com/COVESA/vehicle_signal_specification/releases).

## Addressing Nodes

Tree nodes are addressed, left-to-right, from the root of the tree
toward the node itself. Each element in the name is delimited with
a period ("."). The element hops from the root to the leaf is called ```path```.

For example, the dimming status of the rearview mirror in the cabin is addressed:


    Vehicle.Cabin.RearviewMirror.Dimmed


If there are an array of elements, such as door rows 1-3, they will be
addressed with an index branch:

```
Vehicle.Cabin.Door.Row1.Left.IsLocked
Vehicle.Cabin.Door.Row1.Left.Window.Position

Vehicle.Cabin.Door.Row2.Left.IsLocked
Vehicle.Cabin.Door.Row2.Left.Window.Position

Vehicle.Cabin.Door.Row3.Left.IsLocked
Vehicle.Cabin.Door.Row3.Left.Window.Position
```

In a similar fashion, seats are located by row and their left-to-right position.

```
Vehicle.Cabin.Seat.Row1.Pos1.IsBelted  # Left front seat
Vehicle.Cabin.Seat.Row1.Pos2.IsBelted  # Right front seat

Vehicle.Cabin.Seat.Row2.Pos1.IsBelted  # Left rear seat
Vehicle.Cabin.Seat.Row2.Pos2.IsBelted  # Middle rear seat
Vehicle.Cabin.Seat.Row2.Pos3.IsBelted  # Right rear seat
```

The exact use of ```PosX``` elements and how they correlate to actual
positions in the car, is dependent on the actual vehicle using the
spec.

## Parent Nodes
If a new leaf node is defined, all parent branches included in its name must
be included as well, as shown below:

```
[Signal] Vehicle.Cabin.Door.Row1.Left.IsLocked
[Branch] Vehicle.Cabin.Door.Row1.Left
[Branch] Vehicle.Cabin.Door.Row1
[Branch] Vehicle.Cabin.Door
[Branch] Vehicle.Cabin
[Branch] Vehicle
```

The branches do not have to be defined in any specific order as long
as each branch component is defined somewhere in the vspec file (or an
included vspec file).

## Deprecation `since version 2.1`

During the process of model development, nodes might be
moved or deleted. Giving developers a chance to adopt to the
changes, the original nodes are marked as deprecated with the following rules.

* Nodes, which are moved in the tree or are intended to be removed from the specification are marked with the deprecation keyword.
* The string following the deprecation keyword shall start with the version, when the node was deprecated starting with `V` (e.g. `V2.1`) followed by the reason for deprecation.
* If the node was moved, it shall be indicated by `moved to` followed by the new node name in dot notation as deprecation reason. This keyword shall be used only
if the meta-data of the moved node hasn't changed.
* If the node is intended to be removed from the specification or the meta data changed, it shall be indicated by `removed` and optionally the reason for the removal as deprecation reason.
* Nodes which are deprecated will be removed from the specification, either in the second minor update or, if earlier, the next major update.

### Example
```YAML
Vehicle.Navigation.CurrentLocation:
  type: branch
  description: The current latitude and longitude of the vehicle.
  deprecation: V2.1 moved to Vehicle.CurrentLocation
```

It is recommended for servers, which are implementing protocols for the vehicle signal specification, to serve old and new nodes during the deprecation period described above.

## Style Guide

The VSS specification must adhere to YAML syntax. To keep the standardized VSS specification in this repository consistent the following style guide is provided.

### Naming Conventions

The recommended naming convention for node elements is to use camel case notation starting with a capital letter. It is recommended to use only
`A-Z`, `a-z` and `0-9` in node names. For boolean signals it is recommended to start the name with `Is`.

Examples:

```
SomeBranch.AnotherBranch.MySignalName
Vehicle.Cabin.Door.Row1.Left.IsLocked
```
Naming convention for string literals can be found in the [chapter](/vehicle_signal_specification/rule_set/data_entry/allowed)for specifying allowed values.

### Line Length

It is recommended that line length for files in this repository ( e.g. `*.vspec` and `*.md` files) shall not exceed 120 characters. This is not a strict limit, it is e.g. not recommended to split long URLs present in files over multiple lines.
