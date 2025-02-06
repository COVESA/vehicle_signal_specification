---
title: "Instances"
date: 2019-07-31T15:27:36+02:00
weight: 5
---

VSS resembles primarily the physical structure of the vehicle, so
quite often there is a need to repeat branches and data entries
(e.g. doors, axles, etc). To avoid hard-coded repetitions of
branches and data entries in the specification an instance-concept is supported.
Instances remove the need of repeating definitions, by defining at the node itself how often it occurs in
the resulting tree. They are meant as a short-cut in the specification and
interpreted by the tools. As an example is shown below for doors:

<!-- Image source in docs-gen/image_source/instance_tree.puml -->
![Example tree](/vehicle_signal_specification/images/instance_tree.png)

When expanded this corresponds to:

<!-- Image source in docs-gen/image_source/instance_tree_expand.puml -->
![Example tree](/vehicle_signal_specification/images/instance_tree_expand.png?width=60pc)

## Definition

### How can I create instances for my `branch`?

1. An instance can be defined in any branch.
2. The instantiation is done for every node in the following path.
3. Instances are defined with the key-word `instances`, followed by its
   definition, which can be either:
   * a list of strings, where each element defines a single instance, e.g.
     `['DriverSide','PassengerSide']` results into two instances of every following
     data entry in the path, named `DriverSide` and `PassengerSide`
   * a string, followed by a range defined through `[n,m]`, with `n,m` as integer and `n <= m`,
     which defines the number of instances.
     `Position[1,4]` results into 4 instances of every following
     data entry in the path, named `Position1`, `Position2`, `Position3`
     and `Position4`.
4. If multiple instances occur in one node or on the path to a data entry,
   the instances get combined, by the order of occurrence. Following the example above,
   four position instances will be created for each of the 'DriverSide' and 'PasengerSide' instances,
   resulting into a total number of 8 instances.

### Use of instances in VSS Standard Catalog

The VSS standard catalog is configured to represent a typical passenger vehicle,
with two axles and two rows of seats. For other vehicles, see [recommendations on instance mismatch]({{% ref "#recommendation-instance-mismatch" %}} ) below.

Typical naming conventions used in VSS standard catalog include:

* When instances are defined by a range, e.g., `Position[m,n]`, VSS standard catalog use `1` as start index for the first instance.
* The instance definition `Row[n,m]`, e.g., `Row[1,2]`, is used to indicate that there are multiple rows of the entity. Rows are counted from the front of the vehicle.
* For items located on either left or right side of the vehicle VSS standard catalog use two different conventions:
  * In some cases instances are defined relative to driver position, e.g., `["DriverSide", "PassengerSide"]`.
  * In other cases instances are defined based on physical position, e.g., `["Left","Right"]`.

### How can I exclude child-nodes from instantiation?

Often it makes sense to instantiate all child-nodes of a branch.
But there could be cases, when nodes are linked more the general concept of
a branch, but not to the single instance.

To exclude a child-node from the instantiation of the *direct* parent node, set the
keyword `instantiate` to `false` (`true` by default). Please check the following
example for details.

## Example

The example from above in the specification:

```yaml
# Cabin.vspec
Door:
  type: branch
  instances:
    - Row[1,2]
    - ["DriverSide","PassengerSide"]
  description: All doors, including windows and switches
#include SingleDoor.vspec Door

Door.SomeSignal:
  datatype: uint8
  type: attribute
  instantiate: false
  description: A door signal that should not be instantiated.
```


```yaml
# SingleDoor.vspec

#
# Definition of a single door
#
IsOpen:
  datatype: boolean
  type: actuator
  description: Is door open or closed
```

Results in the following signals:

```
Vehicle.Cabin.Door.SomeSignal
Vehicle.Cabin.Door.Row1.DriverSide.IsOpen
Vehicle.Cabin.Door.Row1.PassengerSide.IsOpen
Vehicle.Cabin.Door.Row2.DriverSide.IsOpen
Vehicle.Cabin.Door.Row2.PassengerSide.IsOpen
```

## Redefinition

It is possible to override the default instantiation provided by VSS by redefining the branch with
different instantiation information. If multiple definitions of a branch exist with different
instance definitions, then the last found definition will be used.
As an example, if three row of doors are needed, then the default VSS instance definition
can be overridden by redefining the Door branch as shown in the example below.

```yaml
#Redefinition changing number of rows from 2 to 3
#The redefinition must appear "after" the original definition
Vehicle.Cabin.Door:
  type: branch
  instances:
    - Row[1,3]
    - ["DriverSide","PassengerSide"]
  description: All doors, including windows and switches
```

## Recommendations

VSS standard catalog is designed to cover a wide range of vehicles.
This means that the default instantiation used in VSS may not fit every vehicle.
An example can be seen in the windshield signals defined in `Body.vspec`, parts of them are shown below.
VSS offers the possibility to control windshield heating separately for front and rear windshield,
and VSS also gives the possibility to report washer fluid level separately for each windshield.
This fits very well for a vehicle that has separate washer fluid containers for front and rear windshield
and that offers heating for both windshields. But that is not the case for all vehicles,
it is not even certain that all vehicles have two windshields. This sections gives recommendations on how
to use VSS for a vehicle if the VSS specification does not offer an exact match of the capabilities of the vehicle.

```yaml
Windshield:
  type: branch
  instances: ["Front", "Rear"]
  description: Windshield signals

Windshield.Heating:
  type: branch
  description: Windshield heater signals

Windshield.Heating.Status:
  datatype: boolean
  type: actuator
  description: Windshield heater status. 0 - off, 1 - on

Windshield.WasherFluid:
  type: branch
  description: Windshield washer fluid signals

Windshield.WasherFluid.LevelLow:
  datatype: boolean
  type: sensor
  description: Low level indication for washer fluid. True = Level Low. False = Level OK.
```

### Recommendation: Instance Mismatch

If a vehicle does not have as many instances as specified in VSS then one
of the following methods are recommended:

- Redefine the branch. If a vehicle for example does not have a rear windshield
then change instance definition in an [overlay]({{% ref "overlay" %}} ) :

```yaml
Vehicle.Body.Windshield:
  type: branch
  instances: ["Front"]
  description: Windshield signals
```

- Accept that a `branch Vehicle.Body.Windshield.Rear` will exist in the generated VSS representation,
  use mechanisms outside VSS to ignore that branch.

### Recommendation: Features shared among instances

If a feature is shared among instances, it is recommended to publish that feature for all concerned instances.

Example: In VSS washer fluid can be handled separately for front and rear windshield.
If a vehicle use a common container serving both front and rear windshield,
then it is recommended that the vehicle report information on that container in both
`Vehicle.Body.Windshield.Front.WasherFluid.LevelLow` and `Vehicle.Body.Windshield.Rear.WasherFluid.LevelLow`.

### Recommendation: Features lacking for some instances

Not all instances in a vehicle might have the same features. If e.g. the front windshield
from the example above lack a heater, then it is recommended to use mechanisms outside VSS
to ignore `Vehicle.Body.Windshield.Front.Heating`.
