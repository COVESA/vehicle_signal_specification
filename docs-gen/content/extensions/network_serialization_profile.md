---
title: "Network Serialization Profile"
weight: 20
---

This profile can be used to specify how VSS signals can be serialized on network as data signal.

## Mapping Syntax

The syntax for definition of a signal with network serialization data (in an overlay) is specified below.

```yaml
<VSS Signal name>:
  type: <VSS type>
  datatype: <VSS datatype>
  network_serialization:
    signal: <signal name in DBC or ARXML>
    [interval_ms: < data update interval in milliseconds>]
    [on_change: {true|false}]
    [endianness: {big_endian|little_endian}]
    [default: <default value or init value (physical) of the signal>]
    [length_bits: < length of signal in bits>]
    [transform: ...]
```

Specifying network signal name is mandatory. It may or maynot be same as VSS signal name but it must correspond to a signal defined in DBC or ARXML.

- The `interval_ms` value indicates the (minimum) interval between updates in milliseconds. A value of `1000` indicates that the VSS system wants at least 1000 milliseconds between each update.
- The `on_change` attribute specifies that the VSS signal only shall be sent if the value has changed.
- If both `interval_ms` and `on_change` are given it shall be considered as an AND-criteria. An update will be sent if the value has changed and the given interval has passed.
- If none of `interval_ms` and `on_change` are specified it corresponds to that the signal shall be sent as soon as value has changed, i.e. `on_change: true`.
- The `endianness` attribute shall be set to represent the order in which bytes are arraged.
- The `default` indicates the default value of signal in same units as min and max of VSS signal.
- The `length_bits` represents length of signal in bits. However, this could be auto-calculated if `transformation` transformation is provided.
- The `transform` entry can be used to specify math or representation of signal i.e conversion between physical to internal and/or textual represenation of signal values.
- If transform is not specified values will be transformed as is. This is applicable for signal representing enumerations.

#### Transformation
##### Math Transformation
A Math transformation can be defined by the `math` attribute.
It accepts [py-expression-eval](https://github.com/AxiaCore/py-expression-eval/) formulas as attribute.
It is expected that the "from" value is represented as `x`.

When evaluating what transformation is needed one must study both the network signal and the VSS signal. An example is given below for mirror tilt of left mirror.

**Network Signal**

The signal `VCLEFT_mirrorTiltYPosition` provides mirror tilt.

```
SG_ VCLEFT_mirrorTiltYPosition : 41|8@1+ (0.02,0) [0|5] "V"  Receiver
```
An introduction to DBC file syntax can be found [here](https://www.csselectronics.com/pages/can-dbc-file-database-intro).
The specification above shows that on CAN the tilt is represented as 0-5 Volts.
The value is sent with a scaling of 0.02 and uses 8 bits, i.e. 5 Volts is transmitted as 250,
but that information is not needed when using the profile,
as the transformation defined in the DBC is performed automatically when CAN frames are read.
For the input to the mapping you will need to consider just a value between 0 and 5 V in this example.
**VSS**
The corresponding signal in VSS uses -100 percent to +100 percent as range and int8 as datatype:
```
Vehicle.Body.Mirrors.DriverSide.Tilt:
  datatype: int8
  unit: percent
  min: -100
  max: 100
  type: actuator
  description: Mirror tilt as a percent. 0 = Center Position. 100 = Fully Upward Position. -100 = Fully Downward Position.
```
With an assumptions that 5 Volts corresponds to fully upward (+100%) and 0 Volts corresponds to
fully downward (-100%) then one could define mapping like in the example below.
```yaml
  Vehicle.Body.Mirrors.DriverSide.Tilt:
  datatype: int8
  type: actuator
  network_serialization:
    signal: VCLEFT_mirrorTiltYPosition
    interval_ms: 100
    transform:
      math: "floor((x*40)-100)"
```

I.e. 2 Volts corresponds to `(2*40)-100` = -20%.

##### Represenation Transformation
A representation transformation can be specified with the `representation` attribute.
It must consist of a list of `value`/`text` pairs like in the example below.
When a network signal value is received the feeder will look for a matching `value` value in the list,
and the corresponding `text` value will be sent to KUKSA.val.

```yaml
Vehicle.Powertrain.Transmission.CurrentGear:
  type: sensor
  datatype: int8
  network_serialization:
    signal: DI_gear
    transform:
       representation:
        - text: DI_GEAR_D
          value: 1
        - text: DI_GEAR_P
          value: 0
        - text: DI_GEAR_INVALID
          value: 0
        - text: DI_GEAR_R
          value: -1
```
Numerical values must be written without quotes.
For boolean signals `true` and `false` without quotes is recommended, as that is valid values in both Yaml and JSON.
If using Yaml (*.vspec) as source format quoting string values is optional.
Quotes may however be needed if the value otherwise could be misinterpreted as a [Yaml 1.1](https://yaml.org/type/bool.html)
literal. Typical examples are values like `yes` which is a considered as a synonym to `true`.
If using JSON all strings must be quoted.

**Example with math and representation attributes in transform**
```yaml
Vehicle.Body.Mirrors.DriverSide.Tilt:
datatype: int8
type: actuator
network_serialization:
  signal: VCLEFT_mirrorTiltYPosition
  interval_ms: 100
  transform:
    math: "floor((x*40)-100)"
    representation:
      - value: 255
        text: Invalid
      - value: 254
        text: ActuationFailed
```
