---
title: "Value Restrictions"
date: 2019-08-04T12:37:12+02:00
weight: 50
---

## Specifying allowed values
Optionally it is possible to define an array of `allowed` values, which will restrict the usage of the data entry in the implementation of the specification.
It is expected, that any value not mentioned in the array is considered an error and the implementation of the specification shall react accordingly.
The datatype of the array elements is the `datatype` defined for the data entry itself.
For `attributes` it is possible to optionally set a default value.

```YAML
SteeringWheel.Position:
  datatype: string
  type: attribute
  default: 'FRONT_LEFT'
  allowed: ['FRONT_LEFT', 'FRONT_RIGHT']
  description: Position of the steering wheel on the left or right side of the vehicle.

```

If `allowed` is set, `min` or `max` cannot be defined.

The `allowed` element is an array of values, all of which must be specified
in a list.  Only values can be assigned to the data entry, which are
specified in this list.

The `datatype` specifier gives the datatype of the individual elements of the `allowed`
list. In general `allowed:` is valid for all datatypes, including integer- and float-based datatypes, unless otherwise specified.

## Recommendation on String values

String values used for `default` and `allowed` statements may contain characters from the printable subset of the Unicode character set.
If using [COVESA VSS-tools](https://github.com/COVESA/vss-tools) it is recommended to use single quotes (`'`) around values as tooling otherwise might handle literals like `OFF` as boolean values with unexpected result.
It is recommended not to specify a dedicated value corresponding to "unknown" or "undefined" unless there is a relevant use-case for that particular signal.
The background is that a signal with an array of allowed values shall be handled just as any other signal.
If e.g. the value of current speed or vehicle weight is unknown, then the vehicle shall not publish the corresponding signal.
Similarly, for the example above, if the steering wheel position is unknown then
`SteeringWheel.Position` shall not be published.

## Allowed values for array datatypes

The `allowed` keyword can also be used for signals of array datatype. In that case, `allowed` specifies the only valid values for array elements.
The actual value of the signal is expected to contain a subset of the values specified in `allowed`.

Example:

```YAML
DogBreeds:
  datatype: string[]
  type: attribute
  allowed: ['AKITA', 'BOXER', 'DACHSHUND', 'PAPILLON', 'PUG', 'VIZSLA']
  description: Brief list of dog breeds.
```

Examples of valid arrays:

```
  [] # Empty array
  ['BOXER']
  ['PAPILLON', 'VIZSLA', 'BOXER', 'AKITA', 'DACHSHUND']
  ['PUG', 'PUG'] # duplication is allowed
```


Example of an invalid array:

```
  ['PAPILLON', 'VIZSLA', 'LOBSTER'] # LOBSTER is not in the allowed value list
```

## Allowed for struct datatypes

Please see [struct]({{< ref "data_types_struct#allowed-values" >}} ) documentation.
