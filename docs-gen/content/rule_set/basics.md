---
title: "Basic Rules"
date: 2019-08-04T13:05:11+02:00
weight: 1
---
## Specification format
A domain specification is written as a flat YAML list, where each signal and
branch is a self-contained YAML list element.

The YAML list is a single file, called a *vspec* file.

A vspec can, in addition to a YAML list, also contain include directives.

An include directive refers to another vspec file that is to replace the
directive, much like ```#include``` in C/C++. Please note that, from a YAML
perspective, the include directive is just another comment.

## Addressing Nodes

Tree nodes are addressed, left-to-right, from the root of the tree
toward the node itself. Each element in the name is delimited with
a period ("."). The element hops from the root to the leaf is called ```path```.

For example, the dimming status of the rearview mirror in the cabin is addressed:


    Cabin.RearviewMirror.Dimmed


If there are an array of elements, such as door rows 1-3, they will be
addressed with an index branch:

```
Cabin.Door.Row1.Left.IsLocked
Cabin.Door.Row1.Left.Window.Position

Cabin.Door.Row2.Left.IsLocked
Cabin.Door.Row2.Left.Window.Position

Cabin.Door.Row3.Left.IsLocked
Cabin.Door.Row3.Left.Window.Position
```

In a similar fashion, seats are located by row and their left-to-right position.

```
Cabin.Seat.Row1.Pos1.IsBelted  # Left front seat
Cabin.Seat.Row1.Pos2.IsBelted  # Right front seat

Cabin.Seat.Row2.Pos1.IsBelted  # Left rear seat
Cabin.Seat.Row2.Pos2.IsBelted  # Middle rear seat
Cabin.Seat.Row2.Pos3.IsBelted  # Right rear seat
```

The exact use of ```PosX``` elements and how they correlate to actual
positions in the car, is dependent on the actual vehicle using the
spec.

## Parent Nodes
If a new leaf node is defined, all parent branches included in its name must
be included as well, as shown below:

```
[Signal] Cabin.Door.Row1.Left.IsLocked
[Branch] Cabin.Door.Row1.Left
[Branch] Cabin.Door.Row1
[Branch] Cabin.Door
[Branch] Cabin
```

The branches do not have to be defined in any specific order as long
as each branch component is defined somewhere in the vspec file (or an
included vspec file).

## Naming Conventions

The recommended naming convention for node elements is to use camel case notation starting with a capital letter. It is recommended to use only
`A-Z`, `a-z` and `0-9` in node names. For boolean signals it is recommended to start the name with `Is`.

Examples:

```
SomeBranch.AnotherBranch.MySignalName
Cabin.Door.Row1.Left.IsLocked
```

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
Navigation.CurrentLocation:
  type: branch
  description: The current latitude and longitude of the vehicle.
  deprecation: V2.1 moved to Vehicle.CurrentLocation
```  

It is recommended for servers, which are implementing protocols for the vehicle signal specification, to serve old and new nodes during the deprecation period described above.
