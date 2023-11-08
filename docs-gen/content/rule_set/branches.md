---
title: "Branch Entry"
date: 2019-07-31T15:27:36+02:00
weight: 1
---

A branch entry describes a tree branch (or node) containing other branches and
signals.  Branches typically represent either a feature of interest (an object whose properties are being observed or reported), or a node that acts as a parent to a group of related properties.

A branch entry representing a feature of interest is exemplified below:

```YAML
Trunk:
  type: branch
  identifier: Vehicle.Body.Trunk
  elementType: FeatureOfInterest
  instances: ["Front", "Rear"]
  definition: An enclosed lockable storage area in a sedan, coupe, or convertible separate from the passenger cabin
  description: Trunk status.
  comment: A trunk is a luggage compartment in a vehicle.
           Depending on vehicle, it can be either in the front or back of the vehicle.
           Some vehicles may have trunks both at the front and at the rear of the vehicle.
```

A branch entry representing a parent node is exemplified below:

```YAML
Windshield.Wiping:
  type: branch
  elementType: Node
  description: Windshield wiper signals.
```

The following elements are defined:

**`Trunk:`** or **`Windshield.Wiping:`**
The list element name defines the dot-notated signal name to the signal.
Please note that all parental branches included in the name must be defined as
well.  In the case of ```Trunk```, it is a child of ```Vehicle.Body``` and thus both ```Vehicle``` and ```Vehicle.Body``` need to be defined.

**```type```**
The value ```branch``` specifies that this is a branch entry. This is the default, in case ```type``` is omitted.

**```identifier```** *[optional]* 
A set of characters that uniquely identifies the branch, usually the full path

**```elementType```** *[optional]* 
A type that categorizes the branch's role in the vehicle signal domain, or as a Node if the branch exists purely for tree traversal and has no vehicle signal domain signifcance on its own.
- ```FeatureOfInterest```: A physical object whose properties can be observed and possibly manipulated.
- ```Node```: A physical object whose properties can be observed and possibly manipulated.

**```definition```*** [optional]* 
A formal specification that includes the necessary and sufficient conditions for distinguishing this branch from anything else.  It is similar to a dictionary definition, and the conditions put forth can translate to formal axioms in an ontology and can be used for inferencing and automation.

**```description```**
Describes the meaning and content of the branch.  Descriptions can include any kind of information that helps humans conceptualize the entry, such as examples, physical properties, etc.
Recommended to start with a capital letter and end with a dot (`.`).

**```comment ```**  *[optional]* `since version 3.0`
A comment can be used to provide additional informal information on a branch.
This could include background information on the rationale for the branch,
references to related branches, standards and similar.
Recommended to start with a capital letter and end with a dot (`.`).

**```instances```** *[optional]*
For specifying that multiple instances of this branch exist, for more information see documentation on
[instances](/vehicle_signal_specification/rule_set/instances/).

**```aggregate```** *[optional]*
Defines whether or not this branch is an aggregate.
If not defined, this defaults to ```false```.
An aggregate is a collection of signals that make sense to handle together in a system.
A typical example could be GNSS location, where latitude and longitude make sense to read
and write together. This is supposed to be deployment and tool specific,
and for that reason no branches are aggregates by default in VSS.
For branches that both have `instances` defined and `aggregate: true`, then aggregate refers to the signals for
individual instances, i.e. signals for different instances can be handled separately.
