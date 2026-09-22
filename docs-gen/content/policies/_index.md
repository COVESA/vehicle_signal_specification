---
title: VSS Design Policy
weight: 22
chapter: false
---


In addition to the rules for the VSS langage the VSS project has agreed on policies for the VSS standard catalog. When someone wants to add new signals to the VSS catalog it shall be verified that the contribution follows the policies for the VSS Standard catalog.

Legacy signals may exist that does not follow the policies. Those signals or the characteristics of those signals shall preferably be listed as exceptions in the corresponding policies. There it shall also preferably be stated if the signals better shall be refactored in the future or if they by some are excempted from the policy.

## License Header

For certain files it is requested that a copyright and license statement is added as file header.
This currently applies to the following file types:

* VSS source files (`*.vspec`)
* Python files (vss-tools, `*.py`)

Those files shall have copyright statement of the following form, inspired by the [Eclipse generic copyright header](https://www.eclipse.org/projects/handbook/#ip-copyright-headers).
Copyright/License-statement may also be added to other files if considered relevant.

```
# Copyright (c) {year} Contributors to COVESA
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License 2.0 which is available at
# https://www.mozilla.org/en-US/MPL/2.0/
#
# SPDX-License-Identifier: MPL-2.0

```
Where {year} is the year the file was originally created. No need to update or append new years or a range of years later.

## VSS Signals shall be generic

Signals added to standard VSS shall be generic, i.e. it shall be possible for other manufacturers to reuse the signal.
Manufacturer-specific signals shall preferably be part of private overlays and not part of standard VSS.

## Logical path

VSS aims to put all signals in a logical path based on physical topology of the vehicle.
As an example, signals related to wheels should typically reside under `Vehicle.Chassis.Axle`.
When proposing a new signal, reuse an existing path if a relevant path exists.


## Consider adding a new file if adding a large number of signals

VSS has no strict rules that every branch must have its own file,
but if a file becomes too big you can consider splitting it if feasible.

## Signals shall have a clear definition without ambiguities

It shall be possible to interpret a signal value by reading the signal description.
Describe if needed how the value shall be calculated/interpreted,
for example if it is based on a standard or if it is up to the manufacturer to select algorithm/method.

* Example: A signal Vehicle.Weight would be ambiguous unless you specify that it refers to gross weight or curb weight.
* Example: Specifying an allowed value `MODE_2` is ambiguous unless you also specify what `MODE_2` means, e.g. by referring to a standard.

## No duplicates

VSS generally avoids to have duplicates in the signal tree, i.e. signals with same purpose and description in different part of the tree.

## Use existing style

Try to reuse the same style as used for existing signals.
Only specify min/max-values if there is a logical reason to limit the range.
Boolean signals should start with `Is`, as in `IsOpen`.
American English is preferred over British English.
No trailing blanks.
Follow the style guide in the [documentation](https://covesa.github.io/vehicle_signal_specification/rule_set/basics/#style-guide).

## Unit and Datatype Policy

See [Unit and Datatype Policy](/vehicle_signal_specification/policies/unit_datatype) .

## Avoid backward incompatible changes

VSS sometimes change or remove existing signals, but only if there is a good reason.
Merging can be delayed, as VSS may decide to wait with the change until the next major release is prepared.
