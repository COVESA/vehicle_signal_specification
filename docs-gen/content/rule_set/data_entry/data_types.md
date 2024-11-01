---
title: "Datatypes"
date: 2019-08-04T11:11:48+02:00
weight: 10
---

In VSS each [data entry](/vehicle_signal_specification/rule_set/data_entry/) (except branches and structs) must specify a ```datatype```.
It can be a primitive type, an array of a primitive type or a struct type.

This is the default datatype for the given entry.
The VSS project typically selects datatype (and unit) so that values are easily understandable by humans,
can cover a reasonable range and supports reasonable precision.
An example is given below where `Vehicle.Speed` has been assigned the datatype `float` and the unit `km/h`.

```
Vehicle.Speed:
  datatype: float
  type: sensor
  unit: km/h
  description: Vehicle speed.
```

The meaning of this is that unless otherwise specified (by an API), the value is supposed to be given as a decimal number with km/h as unit.
An example from [VISS](https://github.com/COVESA/vehicle-information-service-specification) is given below, showing how the speed 123.45 km/h is returned As `"123.45"`.

```
HTTP/1.1 200 OK
            Content-Type: application/json; charset=utf-8
	    ...
            {
              “data”:{“path”:”Vehicle.Speed”,
                      “dp”:{“value”:”123.45”, “ts”:”2020-04-15T13:37:00Z”}
                     }
            }
```

Another example is the [Kuksa Client](https://github.com/eclipse-kuksa/kuksa-python-sdk) where values are to be given in the unit and datatype specified by VSS.

```
Test Client> setValue Vehicle.Speed 43.2
2024-10-18 16:12:54,307 INFO kuksa_client.grpc.aio: Using v2
OK

Test Client> getValue Vehicle.Speed
{
    "path": "Vehicle.Speed",
    "value": {
        "value": 43.20000076293945,
        "timestamp": "2024-10-18T14:12:54.314814+00:00"
    }
}
```

It is *not* mandatory for an implementation, protocol or an API to use the datatype and unit specified by the COVESA VSS catalog.
A VSS entity can in a customized or extended VSS catalog, be annotated with information specifying that the data entry shall be transmitted or stored using a different datatype, possibly involving scaling and offset. An API may in addition or as replacement to the default datatype and offset allow the entity to be read or written using alternative representations or alternative units.

It is however recommended that the default method to read or write a dataentry shall be based on the datatype and unit definined in the standard VSS catalog for signals definied in the standard VSS catalog, as there otherwise is a risk that the client and the server interpret the value differently.


## Supported datatypes

Name       | Datatype                   | Min  | Max
:----------|:---------------------------|:-----|:---
uint8      | unsigned 8-bit integer     | 0    | 255
int8       | signed 8-bit integer       | -128 | 127
uint16     | unsigned 16-bit integer    |  0   | 65535
int16      | signed 16-bit integer      | -32768 | 32767
uint32     | unsigned 32-bit integer    | 0 | 4294967295
int32      | signed 32-bit integer      | -2147483648 | 2147483647
uint64     | unsigned 64-bit integer    | 0    | 2^64 - 1
int64      | signed 64-bit integer      | -2^63 | 2^63 - 1
boolean    | boolean value              | 0/false | 1/true
float      | IEEE 754-2008 binary32 floating point number | -3.40e 38 | 3.40e 38
double     | IEEE 754-2008 binary64 floating point number | -1.80e 308 | 1.80e 308
string     | character string (unicode)          | n/a  | n/a

## Strings

Strings in VSS supports the unicode character set. Actual encoding like UTF-8 or UTF-16 is not
specified by VSS, that is to up to the Protocol/API/SDK implementing VSS support to decide.

## Arrays

Besides the datatypes described above, VSS supports as well the concept of
`arrays`, as a *collection of elements based on the data entry
definition*, wherein it's specified. By default the size of the array is undefined.
By the optional keyword `arraysize` the size of the array can be specified.
The following syntax shall be used to declare an array:

```yaml
# Array of datatype uint32, by default size of the array is undefined
datatype: uint32[]
# Optional: specified number of elements in the array
arraysize: 5
```

An example for the usage of `arrays` is `Vehicle.OBD.DTCList` which contains a list
of Diagnostic Trouble Codes (DTCs) present in a vehicle.

## Structs

VSS struct support is further described on [this page](/vehicle_signal_specification/rule_set/data_entry/data_types_struct/).

## Data Streams

Data Entries, which describe sensors offering binary streams
(e.g. cameras), are not supported directly by VSS with a
dedicated datatype. Instead, they are described through the
meta data about the sensor itself and how to retrieve the
corresponding data stream.

A camera can be a good example of it. The Data Entry for the camera
and the corresponding video stream could look like:

```yaml
Camera:
  type: branch
  description: Information about the camera and how to connect to the video stream

Camera.IsActive:
  type: actuator
  datatype: boolean
  description: If the camera is active, the client is able to retrieve the video stream

Camera.URI:
  type: sensor
  datatype: string
  description: URI for retrieving the video stream, with information on how to access the stream (e.g. protocol,  data format, encoding, etc.)

```

In this example, it shows the usage of meta data about
the status of the sensor. The camera can be set to active through
the same data entry (`actuator`). A dynamic data entry (`sensor`)
is used for the URI of the video stream. Information on how to access
the stream is expected.
