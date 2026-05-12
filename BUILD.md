# Building and Using the ACEA-VSS Catalog

As a user you have two options - either your project directly consumes the source files (`*.vspec`) generated in this repository, see [Generate VSPEC files](#generate-vspec-files),
or you convert it to some other format using [VSS-tools](https://github.com/COVESA/vss-tools/), see [Generate artifacts using VSS tools](#generate-artifacts-using-vss-tools).

## Set up your development environment

You are free to use whatever development environment you want. For development a typical workflow to set up the development environment is as follows:

1. Clone the branch acea-namespace in [VSS repository](https://github.com/COVESA/vehicle_signal_specification)

```console
user@debian:~$ git clone --branch acea-namespace https://github.com/COVESA/vehicle_signal_specification
```

2. Get all submodules

```console
user@debian:~/vehicle_signal_specification$ git submodule update --init
```

3. Follow the instructions in [VSS-tools](https://github.com/COVESA/vss-tools/blob/master/README.md) to prepare an environment suitable for vss-tools
4. Install the needed dependencies: python v3.10.6 and Make
5. Verify that your development environment is fully functional by running `make` from your `vehicle_signal_specification` folder.

## Download the pre-built tree

You can download the acea-vss pre-built artifact from [Github Actions](https://github.com/COVESA/vehicle_signal_specification/actions?query=branch%3Aacea-namespace), the workflow runs everytime there is a new commit on the `acea-namespace` branch.

## Build the ACEA-VSS tree

You can build the default tree by running the `make` command on the root repository, alternatively you can run the python script directly as follow:

```console
user@debian:~/vehicle_signal_specification$ python tools/gomplate/src/generate.py
user@debian:~/vehicle_signal_specification$ vspec export yaml -u ./generated/units.yaml --strict -e metadata -s ./generated/VehicleSignalSpecification.vspec -o generated/vss.yaml
```

## Enable Verbose logging

By default, the build runs in quiet mode — only warnings and errors are shown.

To enable verbose logging (debug + info messages), pass VERBOSE=1 to `make`:

```console
user@debian:~/vehicle_signal_specification$ make VERBOSE=1
```

## Generate VSPEC files

The sections below provide some guidance on how to use the tools provided in this repo to convert the ACEA tree into VSS catalog. See [set up your development environment](#set-up-your-development-environment)

The ACEA specification defined under the folder spec/ are templated using [Gomplate](https://github.com/hairyhenderson/gomplate), you can generate the VSPEC files according to the VSS catalog by running the below command, the output will be under folder generated/:

```console
user@debian:~/vehicle_signal_specification$ make preprocessing
```

Note: the python script under tools/ will install Gomplate tool if it cannot be found in your environment.

## Generate artifacts using VSS tools

The sections below provide some guidance on how to use the tools provided in this repo to convert ACEA specification and generate artifacts using VSS tools. See [set up your development environment](#set-up-your-development-environment)

### Generate Tree in YAML format

If you want to generate the artifact in YAML format, you can do that with `make yaml`.
Check the [Makefile](Makefile) for available commands.

An example to generate yaml from the *.vspec3 files under the folder spec/:

```console
user@debian:~/vehicle_signal_specification$ make yaml
/usr/bin/python3 tools/gomplate/src/generate.py
vspec export yaml -u ./generated/units.yaml --strict -e metadata -s ./generated/VehicleSignalSpecification.vspec -o generated/vss.yaml
[11:13:37] INFO     User defined extra attributes: ('metadata',)
           INFO     Loaded 'VSSQuantity', file=/home/foobar/vehicle_signal_specification/generated/quantities.yaml, elements=30
           INFO     Loaded 'VSSUnit', file=/home/foobar/vehicle_signal_specification/generated/units.yaml, elements=69
           INFO     VSpecs loaded, amount=36
[11:13:38] INFO     Generating YAML output...
user@debian:~/vehicle_signal_specification$ ls generated/vss.yaml
generated/vss.yaml
```

### Generate Tree in other format

If you want to generate the artifact in other formats supported by the [VSS-tools](https://github.com/COVESA/vss-tools/) (JSON, CSV, ...), you have two options, either:

### Add support for other format in the Makefile

Similarly to the YAML target in the [Makefile](Makefile), other VSS-tools supported format can be extended and added to the Makefile directly, for example:

```
binary:
	vspec export binary ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o generated/vss.binary
```

### Run the VSS-tools on the generated VSPEC files

Before you run the VSS tools, first you need to generate the VPSEC files from the ACEA templated files, you can do that by following instruction in section [Generate VSPEC files](#generate-vspec-files)

An example to generate csv from the *.vspec3 files under the folder spec/:

```
user@debian:~/vehicle_signal_specification$ make preprocessing
/usr/bin/python3 tools/gomplate/src/generate.py
user@debian:~/vehicle_signal_specification$ vspec export csv -u ./generated/units.yaml --strict -e metadata -s ./generated/VehicleSignalSpecification.vspec -o generated/vss.csv
[11:25:42] INFO     User defined extra attributes: ('metadata',)
           INFO     Loaded 'VSSQuantity', file=/home/a398755/playground/acea/repo/vehicle_signal_specification/generated/quantities.yaml, elements=30
           INFO     Loaded 'VSSUnit', file=/home/a398755/playground/acea/repo/vehicle_signal_specification/generated/units.yaml, elements=69
           INFO     VSpecs loaded, amount=36
           INFO     Generating CSV output...
```

## Make sure that your changes pass CI checks

Continuous Integration (CI) checks are defined in the [workflows](.github/workflows) folder.

### Signoff

All commits must be signed-off and carry the following sign-off line with your real name and email address:

`Signed-off-by: Firstname Lastname <you@example.com>`

### Pre-commit checks

The repository has [configuration file](.pre-commit-config.yaml) with pre-commits hooks.
It executes a number of checks that typically must pass for a new Pull Request to be accepted and merged.
You must manually configure pre-commit to use the provided hooks by running `pre-commit install` from the
repository top folder.

```console
user@debian:~/vehicle_signal_specification$: pip install pre-commit
user@debian:~/vehicle_signal_specification$: pre-commit install
```
