# Building and Using the VSS Standard Catalog

As a VSS user you have two options - either your project directly consumes the source files (`*.vspec`) in this repository,
or you first convert it to some other format using [VSS Tools](https://github.com/COVESA/vss-tools).

## Using the VSS source files

If you intend to write your own VSS parser there are two files that you need to use as input.
The root source file for the VSS standard catalog is [VehicleSignalSpecification.vspec](spec/VehicleSignalSpecification.vspec).
It include all other `*.vspec` files in this repository (except overlays/profiles).
Your parser may also be interested in using the [units.yaml](spec/units.yaml) file that list all units defined by the
standard catalog documentation.

## Using VSS-Tools

Before writing your own parser it could be an idea to check if a suitable parser already has been created as part of
[VSS-Tools](https://github.com/COVESA/vss-tools). This repository use some of the tools in VSS-Tools during Continuous
Integration, and we also provide generated artifacts (CSV, Franca IDL, Graphql, DDS IDL, JSON, Yaml) for each
[release](https://github.com/COVESA/vehicle_signal_specification/releases).
The sections below provide some guidance on how to use VSS-Tools to convert the VSS standard catalog.
Before creating a Pull Requst towards this repository it is recommended that you verify that your modified catalog
can be used successfully with tools used in continuous integration.

For detailed information on development environment and usage see [VSS-Tools](https://github.com/COVESA/vss-tools).

### Set up you development environment

You are free to use whatever development environment you want, but tools in [VSS-tools](https://github.com/COVESA/vss-tools)
have typically been tested only on Linux, and in continuous integration "ubuntu-latest" is used for testing.

For development a typical workflow to set up the development environment is as follows:

1. Clone the [VSS repository](https://github.com/COVESA/vehicle_signal_specification
2. Get all submodules (`git submodule update --init`)
3. Follow instructions in [VSS-tools](https://github.com/COVESA/vss-tools/blob/master/README.md) to install dependencies
4. Verify that your development environment is fully functional by running `make` from your `vehicle_signal_specification` folder.

### Generating artifacts

If you want to generate VSS artifacts (JSON, CSV, ...) similar to what is included in
[VSS-releases](https://github.com/COVESA/vehicle_signal_specification/releases) you can do that with `make`.
Check the [Makefile](Makefile) for available commands.

An example to generate CSV from the *.vspec files in your current branch is:

```
user@debian:~/vehicle_signal_specification$ make csv
./vss-tools/vspec2csv.py -I ./spec --uuid -u ./spec/units.yaml ./spec/VehicleSignalSpecification.vspec vss_rel_$(cat VERSION).csv
INFO     Output to csv format
INFO     Known extended attributes:
INFO     Added 56 units from ./spec/units.yaml
INFO     Loading vspec from ./spec/VehicleSignalSpecification.vspec...
INFO     Calling exporter...
INFO     Generating CSV output...
INFO     All done.
user@debian:~/vehicle_signal_specification$ ls *.csv
vss_rel_4.1-dev.csv
```

### Make sure that your changes pass CI checks

Continuous Integration (CI) checks are defined in the [workflows](.github/workflows) folder.
They consist of the following areas

#### Signoff
All commits must be signed-off, see [CONTRIBUTING.md](CONTRIBUTING.md)

#### Build checks
Make sure that `make travis-targets` succeeds. It is even better if all targets succeed (`make all`).

#### Pre-commit checks
The repository has [configuration file](.pre-commit-config.yaml) with pre-commits hooks.
It executes a number of checks that typically must pass for a new Pull Request to be accepted and merged.
You must manually configure pre-commit to use the provided hooks by running `pre-commit install` from the
respository top folder.

```bash
~/vehicle_signal_specification$: pip install pre-commit
~/vehicle_signal_specification$: pre-commit install
```
