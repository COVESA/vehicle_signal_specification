# Struct Proposal

This document tries to define with examples what shall be (theoretically) supported in VSS after adding struct support.
I.e. what you can do still claiming that the model is correct VSS.
It only to a limited extent show implications for vss-tools, and then only for syntactic/semantic checks.
As of now it does not state how exporters are affected.

## Proposed VSS 4.0 acceptance criteria and increments

We need to decide how far we must go before we can release VSS 4.0, we does not need to go the whole way in one step

### Increment 1

* Syntax can be used without VSS-tools complaining
* No semantic check by VSS-tools
* No documentation
* Not used in VSS standard catalog
* Struct not supported by VSS-tools exporters


### Increment 2

* Semantic check on type-references by VSS-tools
* Syntax documented
* Well defined behavior for all exporters (e.g. either support, and/or give warning if used)

### Increment 3

* All "standard" exporters in vss-tools support structs
* Guidelines on when to consider using structs rather than branches documented

### Increment 4

* We may start to use structs in VSS standard catalog.

## Simple Usage

```
DeliveryInfo:
  type: struct
  description: A struct type containing info for each delivery
  
DeliveryInfo.Address:
  datatype: string
  type: item
  description: Destination address

DeliveryInfo.Receiver:
  datatype: string
  type: item
  description: Name of receiver

Delivery:
  datatype: DeliveryInfo
  type: sensor
  description: Delivery
```

For VSS 4.0 it is not necessary that vss-tools do semantic check, i.e. if someone would add an extra `f` by mistake like this:

```

Delivery:
  datatype: DeliveryInffo
  comment: Note: Spelling error on line above, will only be detected if semantic check is implemented
  type: sensor
  description: Delivery
```

... then VSS-tools does not necessarily need to give an error (stretch goal to have semantic check that referred type exist).

## Name resolution

For now, two ways of referring to a type shall be considered correct:

* Reference by (leaf) name to a struct definition within same branch
* Reference by absolute path

Relative paths (e.g. `../Powertrain.SomeStruct`) shall not be supported.
Structs in parent branches will not be visible, in those cases absolute path needs to be used instead

Examples:


```
A:
  type: branch
  description: Branch A.

A.DeliveryInfo:
  type: struct
  
A.DeliveryInfo.Address:
  datatype: string
  type: item

A.DeliveryInfo.Receiver:
  datatype: string
  type: item

A.Delivery1:
  datatype: DeliveryInfo /* OK - As DeliveryInfo defined in same branch as Delivery1 */
  type: sensor


A.Delivery2:
  datatype: A.DeliveryInfo /* OK - Addressing using absolute path */
  type: sensor

A.B:
  type: branch

A.B.Delivery3:
  datatype: DeliveryInfo /* ERROR - No DeliverInfo defined in branch A.B */
  type: sensor

A.B.Delivery4:
  datatype: A.DeliveryInfo /* OK - Addressing using absolute path */
  type: sensor
  
A.B.Deliver5:
  datatype: ../DeliveryInfo /* ERROR - Relative paths not supported */
  type: sensor

```

### Order of declaration/definition

The struct type must be defined before it is used.

**TBD: I think this makes it easier for our implementation, but the question is if we want this to be a requirement also in the long term**

Example:

```
A:
  type: branch
  description: Branch A.
  
  
A.Delivery1:
  datatype: DeliveryInfo /* ERROR - DeliveryInfo has not been defined yet! */
  type: sensor

A.DeliveryInfo:
  type: struct
  
A.DeliveryInfo.Address:
  datatype: string
  type: item

A.DeliveryInfo.Receiver:
  datatype: string
  type: item

A.Delivery2:
  datatype: DeliveryInfo /* OK - Now DeliveryInfo has been defined */
  type: sensor
```

## Expectations on VSS implementations (e.g. VISS, KUKSA.val)

It is expected of implementation (long-term) to support atomic read/write/subscribe of signals defined by struct.
They may support read of parts of signal, e.g. `DeliveryList.Receiver`

## Array Support

It shall be possible to specify that there shall be a struct of the array


```
DeliveryInfo:
  type: struct
  description: A struct type containing info for each delivery
  
DeliveryInfo.Address:
  datatype: string
  type: item
  description: Destination address

DeliveryInfo.Receiver:
  datatype: string
  type: item
  description: Name of receiver

DeliveryList:
  datatype: DeliveryInfo[]
  type: sensor
  description: List of deliveries
```

By default the array has an arbitrary number of element and may be empty.
If a fixed size array is wanted the keyword `arraysize` can be used to specify size:

```
DeliveryList:
  datatype: DeliveryInfo[]
  arraysize: 5
  type: sensor
  description: List of deliveries
```


### Expectations on VSS implementations (e.g. VISS, KUKSA.val)

For array types (like above) VSS implementations may support several mechanisms

* It is expected that they can support read/write/subscribe of the whole array, i.e. write all or read all in the same request
* They may optionally support additional operations like
    * Writing/Reading a single instance, e.g. `DeliveryList[2]` (index mechanism is implementation dependent)
    * Appending/Deleting individual instances
    * Searching for instances with specific conditions.
    
## Structure in Structure

It shall be possible to refer to a structure type from within a structure

```
OpenHours:
  type: struct
  description: A struct type containing information on open hours
  
OpenHours.Open:
  datatype: uint8
  type: item
  max: 24
  description: Time the address opens
  
OpenHours.Close:
  datatype: uint8
  type: item
  max: 24
  description: Time the address close

DeliveryInfo:
  type: struct
  description: A struct type containing info for each delivery
  
DeliveryInfo.Address:
  datatype: string
  type: item
  description: Destination address

DeliveryInfo.Receiver:
  datatype: string
  type: item
  description: Name of receiver
  
DeliveryInfo.Open:
  datatype: OpenHours
  type: item
  description: When is receiver available

Delivery:
  datatype: DeliveryInfo
  type: sensor
  description: Delivery
```

For now it shall not be allowed to define a struct within a struct, all structs must be defined within a branch.

## Inline Struct

As an alternate approach we could consider supporting inline / anonymous structs

```

DeliveryList:
  datatype: struct[]
  type: sensor
  description: List of deliveries
  
DeliveryList.Address:
  datatype: string
  type: item
  description: Destination address

DeliveryList.Receiver:
  datatype: string
  type: item
  description: Name of receiver

```

This could also work for struct in struct

```


DeliveryList:
  datatype: struct[]
  type: sensor
  description: List of deliveries
  
DeliveryList.Address:
  datatype: string
  type: item
  description: Destination address

DeliveryList.Receiver:
  datatype: string
  type: item
  description: Name of receiver

DeliveryInfo.Open:
  datatype: struct
  type: item
  description: When is receiver available

DeliveryInfo.Open.Open:
  datatype: uint8
  type: item
  max: 24
  description: Time the address opens
  
DeliveryInfo.Open.Close:
  datatype: uint8
  type: item
  max: 24
  description: Time the address close
  
```
**Proposal: For now inline/anonymous structs shall not be allowed! That could potentially be added later if needed**

## Default Values

VSS supports [default values for attributes](https://covesa.github.io/vehicle_signal_specification/rule_set/data_entry/attributes/),
and there is a [discussion](https://github.com/COVESA/vehicle_signal_specification/issues/377)
to allow it also for sensors/actuators. 

For structs it needs to be discussed if default values shall be given on the signal itself or on individual items.

Example showing default values on items:

```
DeliveryInfo:
  type: struct
  description: A struct type containing info for each delivery
  
DeliveryInfo.Address:
  datatype: string
  type: item
  default: 'Feuerbach'
  description: Destination address

DeliveryInfo.Receiver:
  datatype: string
  type: item
  default: 'Bosch'
  description: Name of receiver

FirstDelivery:
  datatype: DeliveryInfo
  type: attribute
  description: First delivery
```



For structs the following syntax could be used


```
{<value of element 1>, < value of element 2>, ...}
```
Example showing `default` on signal of struct type:

```
FirstDelivery:
  datatype: DeliveryInfo
  type: attribute
  default: {'Munich','BMW'}
  description: First delivery
```


Default values could also be supported for arrays:

```
DeliveryList:
  datatype: DeliveryInfo[]
  type: attribute
  default: [{'Munich','BMW'},{'Feuerbach','Bosch'}]
  description: List of deliveries
```

TBD: How important do we see it to support default values for structs? So far we do not do any syntatic/semantic checks on default values, i.e. check that they are compatible with the used type.
I do not know if any exporter as of today do something "advanced" with the given default value.
If they just copy it as-is or ignores it then adding struct support would not be a big effort.
But translating it to something useful for the target format might be a bigger effort.

**Proposal: It shall for now not be allowed to use default for signals of struct type or for items! **


## Allowed Values

VSS supports [specification of allowed values](https://covesa.github.io/vehicle_signal_specification/rule_set/data_entry/allowed/).
As of today it is theoretically supported for all datatypes, but there is an [issue](https://github.com/COVESA/vehicle_signal_specification/issues/502)
discussing if it is to be supported only for string data and possible integer-based types.

Using `allowed` for `type: item` shall be supported (if `allowed` is supported for the used datatype).

```
DeliveryInfo:
  type: struct
  description: A struct type containing info for each delivery
  
DeliveryInfo.Address:
  datatype: string
  type: item
  allowed: ['Munich','Feuerbach']
  description: Destination address

DeliveryInfo.Receiver:
  datatype: string
  type: item
  allowed: ['BMW','Bosch']
  description: Name of receiver

DeliveryList:
  datatype: DeliveryInfo[]
  type: sensor
  description: List of deliveries
```


Theoretically `allowed` for signals of struct type could be supported if supported for all contained data types.
The example below follows the guidelines for [array types](https://covesa.github.io/vehicle_signal_specification/rule_set/data_entry/allowed/#allowed-values-for-array-types).
The usefulness could however be debated, and semantic check could be time consuming

```
DeliveryList:
  datatype: DeliveryInfo[]
  type: attribute
  allowed: [{'Munich','BMW'},{'Feuerbach','Bosch'}]
  description: List of deliveries
```

**Proposal: It shall for now not be allowed to use allowed for signals of struct type! (But allowed to use it for items)**
