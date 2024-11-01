---
title: "Branch Entry"
date: 2019-07-31T15:27:36+02:00
weight: 1
---

A branch entry describes a tree branch (or node) containing other branches and
signals.

A branch entry example is given below:

```yaml
Vehicle.Trunk:
  type: branch
  description: All signals related to the rear trunk
  aggregate: false
```
Each data entry has a name, in the example above `Vehicle.Trunk`.
VSS use a dot-notated name style where the full path of a branch consists of all parent branches from the root node separated by dots and at the end the name of the current branch. In the standard VSS catalog the root node is called `Vehicle`.

When using `*.vspec` files to define a VSS catalog it is not necessary to give the full dot-notated name for each branch as the
`*.vspec` format supports [includes](../includes/) that can be used to append entries to a specific branch.

## Mandatory Branch Attributes

This is the list of attributes that must be specified for every data entry.

Attribute    | Description                 | Comment
-------------|-----------------------------|--------
`type`       | Defines the type of the node. For a branch this must be `branch`. | The default for `type` is `branch`.
`description`| Describes the meaning and content of the branch. Recommended to start with a capital letter and end with a dot (`.`).

## Optional Data Entry Attributes

In additon to the mandatory attributes some optional attributes have been defined.
There may be additional constraints on their usage not specified in the table below.

Attribute    | Description                 | Comment
-------------|-----------------------------|--------
`comment`    | A comment can be used to provide additional informal information on a branch. This could include background information on the rationale for the branch, references to related branches, standards and similar. Recommended to start with a capital letter and end with a dot (`.`). | *since version 3.0*
`instances`        | For specifying that multiple instances of this branch exist, for more information see documentation on [instances](/vehicle_signal_specification/rule_set/instances/).
`aggregate` | Defines whether or not this branch is an aggregate. If not defined, this defaults to ```false```. An aggregate is a collection of signals that make sense to handle together in a system. A typical example could be GNSS location, where latitude and longitude make sense to read and write together. This is supposed to be deployment and tool specific, and for that reason no branches are aggregates by default in VSS. For branches that both have `instances` defined and `aggregate: true`, then aggregate refers to the signals for individual instances, i.e. signals for different instances can be handled separately.
