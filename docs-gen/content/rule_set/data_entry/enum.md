---
title: "Defined Value restrictions"
date: 2019-08-04T12:37:12+02:00
weight: 5
---

Optionally it is possible to define an array of `allowed`, which will restrict the usage of the data entry in the implementation of the specification.
It is expected, that any value not mentioned in the array is considered an error and the implementation of the specification shall react accordingly.
The datatype of the array elements is the `datatype` defined for the data entry itself.
For `attributes` it is possible to set optionally a default value.

```YAML
  
Charging.ChargePlugType:
  datatype: string
  type: attribute
  default: ccs
  allowed: [ 'type 1', 'type 2', 'ccs', 'chademo' ]
  description: Type of charge plug available on the vehicle (CSS includes Type2).
```

If `allowed` is set, ```min```, ```max```, or ```unit``` cannot be defined.

The ```allowed``` element is an array of values, all of which must be specified
in a list.  Only values can be assigned to the data entry, which are
specified in this list.

The ```datatype``` specifier gives the type of the individual elements of the `allowed`
list.
