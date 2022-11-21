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

DeliveryList:
  datatype: DeliveryInfo
  type: sensor
  description: List of deliveries
```

For VSS 4.0 it is not necessary that vss-tools do semantic check, i.e. if someone would add an extra `f` by mistake like this:

```

DeliveryList:
  datatype: DeliveryInffo
  type: sensor
  description: List of deliveries
```

... then VSS-tools does not necessarily need to give an error (stretch goal to have semantic check that referred type exist).

## Name resolution

For now, two ways of referring to a type shall be considered correct:

### Reference to a struct definition within same branch

As the example above.

TBD: Or do we want a more flexible approach, i.e. if you specify "ABC" as datatype, that a tool shall search upwards in all parent branches?

I.e. If a signal `A.B.C.D` is defined with type `X`, then the following priority order shall apply:

* If `A.B.C.X` exists, then it will be used.
* Else if `A.B.X` exists, then it will be used.
* Else if `A.X` exists, then it will be used.

### Reference by absolute path

Reference by full path shall also be allowed. For now relative paths (e.g. `../Powertrain` shall not be supported).
But vss-tools does not need to resolve or verify that type reference is correct in VSS 4.0.

```

DeliveryList:
  datatype: Vehicle.Some.Branch.DeliveryInfo
  type: sensor
  description: List of deliveries
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

DeliveryList:
  datatype: DeliveryInfo
  type: sensor
  description: List of deliveries
```

TBD: Where shall the inner struct be defined? Shall it be allowed to define it within a struct as well, or does it need to be defined within a branch like above? If allowed to be defined within a struct, how do we want name resolution to work, only support exact (current) scope and absolute path, or a more flexible setup searching upwards.

I.e. shall the following alternative style (where the struct `OpenHours` is defined within `DeliveryInfo`) be allowed or even preferred?

```

DeliveryInfo:
  type: struct
  description: A struct type containing info for each delivery

DeliveryInfo.OpenHours:
  type: struct
  description: A struct type containing information on open hours
  
DeliveryInfo.OpenHours.Open:
  datatype: uint8
  type: item
  max: 24
  description: Time the address opens
  
DeliveryInfo.OpenHours.Close:
  datatype: uint8
  type: item
  max: 24
  description: Time the address close
  
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

DeliveryList:
  datatype: DeliveryInfo
  type: sensor
  description: List of deliveries
```

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

