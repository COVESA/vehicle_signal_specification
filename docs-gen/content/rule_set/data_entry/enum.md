---
title: "Enums"
date: 2019-08-04T12:37:12+02:00
weight: 45
---



## Specifying a signal as an enum

VSS has introduced `enum` as an alternative to [allowed values](/vehicle_signal_specification/rule_set/data_entry/allowed/).
In VSS allowed values have typically been used to restrict values for string signals, and most exporters and downstream projects have treated it as a string value.
With enum the base type is an integer type and exporters and downstream projects are free to decide on how they want to use the symbolic names,
like if they want to expose the symbolic names in APIs or generated assets, or if they just ignore the symbolic names.

It is however expected that VSS implementations has mechanisms to assure that only values matching the specified enums can be used for the related signals.

## Basic syntax

Enum delcarations can be used for `actuator`, `sensor`, `attribute` and for structs in `property`.
The base type must be an integer type, which means that e.g. `string` cannot be used as base type.
In the enum field a dict of string keys and integer values shall be given be given.
The values must fit the defined datatype. In the example below it means that values 0-255 can be used.

```yaml
Dogbreed:
  type: attribute
  description: Foo
  datatype: uint8
  enum:
    'AKITA': 0
    'BOXER': 1
  default: 0
```


* Keys must match the pattern `[A-Z][A-Z_0-9]*`
* Values are not allowed to be reused, E.g. a definition like `'A':1, 'B':1, 'C':2` is not allowed.
* If `enum` is set then `allowed`, `pattern`, `min` or `max` cannot be defined.
* If `default` is used the numeric value shall be used.

### Recommendations

If using [COVESA VSS-tools](https://github.com/COVESA/vss-tools) it is recommended to use single quotes (`'`) around keys as tooling otherwise might handle literals like `OFF` as boolean values with unexpected result.
It is recommended not to specify a dedicated values corresponding to "unknown" or "undefined" unless there is a relevant use-case for that particular signal.
The background is that a signal using enum shall be handled just as any other signal.
If e.g. the value of current speed or vehicle weight is unknown, then the vehicle shall not publish the corresponding signal.
Similarly, for the example above, if the dog breed is unknown then
`Dogbreed` shall not be published.

## Enum for array datatypes

The `enum` keyword can also be used for signals of array datatype. In that case, `enum` specifies the valid values for array elements.
The `default` statement (if present) defines the default array. In the example below the default array is `[AKITA, CHOW_CHOW]`.

Example:

```yaml
DogBreeds:
  type: attribute
  description: Bar
  datatype: uint8[]
  enum:
    'AKITA': 0
    'BOXER': 1
    'CHOW_CHOW': 2
    'DACHSHUND': 3
  default:
    - 0
    - 2
```
