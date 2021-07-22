---
title: "Enumerated Data Entries"
date: 2019-08-04T12:37:12+02:00
weight: 5
---


A data entry can optionally be enumerated, allowing it to be assigned a
value from a specified set of values. An examples of a signal using enum is
given below:


```YAML
  
Charging.ChargePlugType:
  datatype: string
  type: attribute
  default: ccs
  enum: [ 'type 1', 'type 2', 'ccs', 'chademo' ]
  description: Type of charge plug available on the vehicle (CSS includes Type2).
```

An enumerated signal entry has no ```min```, ```max```, or ```unit```
element.

The ```enum``` element is an array of values, all of which must be specified
in the enum list.  This signal can only be assigned one of the values
specified in the enum list.

VSS supports enums for both integer datatypes as well as strings.
The ```datatype``` specifier gives the type of the individual elements of the enum
list.
