---
title: "Data Formats"
date: 2024-08-29T12:36:12+02:00
weight: 25
---

## Data Formats

For some data it is necessary to specify the format.
An example are dates.
Let's say we specify a leaf e.g. `Vehicle.ProductionDate` and give it
the datatype `string`. How would a consumer know what to expect in this string?
It could be ISO8601, it could be a unix-timestamp or it could be something totally different.
To provide that info, a `format` field can be used.

A complete definition of a `ProductionDate` field could then look like this:

```yaml
Vehicle.ProductionDate:
    description: The production date of the car
    datatype: string
    format: iso8601
```

All formats being used have to be specified in format definition files.

## Format definitions file

It has the following format:

```yaml
unix-time:
  description: Unix Timestamp
  allowed-datatypes: ['uint32','uint64','int64']
```

Both fields are required:
- `description`: Should specify how the format is specified
- `allowed-datatypes`: Datatypes allowed when using this format. The consistency will be enforced by `vss-tools`

Please note that you can either specify `unit` or `format`.


## Supported Data Formats in VSS Standard Catalog

The catalog defines common formats in the `formats.yaml` file similar to how units are handled. `vss-tools` provides an interface to pass one or more format files.
Like with unit files, `formats.yaml` will be loaded if it is present on the level
of the given entry point `vspec` file.
