---
title: "VSS Winnie the Pooh Extension Profile"
date: 2023-05-18T13:29:46+0000
weight: 2
---

*This is just an example on how we could define extension profiles within documentation.*
*To be removed as soon as we have a "real" extension profile!*

This is a profile to associate signals to Winnie the Pooh characters

## Syntax

```yaml
<VSS Signal name>:
  type: <VSS type>
  datatype: <VSS datatype>
  pooh: {"pooh"|"piglet"|"owl"|"tigger"|"kanga"|"eeyore"|"roo"}
```

## Example

```yaml
Vehicle.Body.Mirrors.DriverSide.Tilt:
  datatype: int8
  type: actuator
  pooh: tigger
  ```
