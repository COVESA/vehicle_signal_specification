# Introduction to VSS Contribution Process

The COVESA VSS project has public two GitHub repositories

- [Vehicle Signal Specification (VSS)](https://github.com/COVESA/vehicle_signal_specification), containing signal specifications and documentation.
- [VSS Tools](https://github.com/COVESA/vss-tools), containing tools for validating and transforming VSS specifications.

The examples below refer to the VSS repository, but the process is similar for the VSS-Tools repository.

There are two main methods to propose changes or extensions to VSS:

- If you have an idea or a question you can create an [issue](https://github.com/COVESA/vehicle_signal_specification/issues) in GitHub.
- If you already have prepared changes or extension that you think would be interesting for COVESA to include in VSS
  then you can create a [Pull Request (PR)](https://github.com/COVESA/vehicle_signal_specification/pulls).

All contributions must follow the [COVESA contribution guidelines](https://www.covesa.global/contribute).

The VSS project has regular meetings at Tuesdays 16.00 CET (see [COVESA VSS Wiki](https://wiki.covesa.global/display/WIK4/VSS+-+Vehicle+Signal+Specification)).
In the meetings Pull Requests and Issues are discussed, and if a Pull Request is acceptable the meeting will decide that it shall be merged.
Everyone interested is welcome to join the meetings.

## Creating a Pull Request towards VSS

This is the typical workflow for preparing a pull request. A Github account is required.

1. Create a personal or company fork of the [VSS repository](https://github.com/COVESA/vehicle_signal_specification)
   and/or [VSS-Tools repository](https://github.com/COVESA/vss-tools).
2. Clone the forked repository into your local development environment.
3. Create a local branch based on the VSS master branch to use for the proposed changes.
4. Introduce the wanted changes or extensions in your local development environment, see guidelines below.
   If you want change/extend VSS-signals, it is the *.vspec files in the [spec](https://github.com/COVESA/vehicle_signal_specification/tree/master/spec) folder that
   needs to be updated.
5. Run "make travis_targets" to verify that the changes are syntactically correct and does not introduce any side effects.
   This will verify that tools and test-cases in vss-tools repository accepts the changes.
6. Create a commit and upload to your own fork.
7. In the GitHub UI create a Pull Request from your fork to the master branch of [the VSS repository](https://github.com/COVESA/vehicle_signal_specification).
8. Validate that automatic build checks for the PR succeed.

## Handling of the created Pull Request

1. The PR creator shall follow up on any comments or questions received on the Pull Request.
2. The PR will be discussed at one of the next VSS weekly meetings. 
   It is preferable if the PR creator can participate and give a quick introduction on the rationale for the change.
3. Unless trivial, PRs shall typically be open for at least a week before merging is considered, to give time for comments.
4. If needed, the PR creator needs to refactor the PR to address received comments and remarks.
4. After a while, if all comments and concerns have been sorted out and no-one objects merging the PR the meeting will decide to merge the PR.
   It is not guaranteed that all PRs will be accepted. The VSS meeting may reject and close Pull Requests.
5. A VSS maintainer will perform the merge.

## Guidelines and Recommendations

This section includes general guidelines and recommendations for anyone interested in contributing to VSS.

### VSS Signals shall be generic

Signals added to standard VSS shall be generic, i.e. it shall be possible that other manufacturers can reuse the signal.
Manufacturer-specific signals shall preferably be part of private overlays, and not part of standard VSS.

### Logical path

VSS aims to put all signals in a logical path based on physical topology of the vehicle. 
As an example, signals related to wheels should typically reside under `Vehicle.Chassis.Axle`.
When proposing a new signal, reuse an existing path if a relevant path exists.

### Consider adding a new file if adding a large number of signals

VSS has no strict rules that every branch must have its own file,
but if a file becomes too big you can consider splitting it if feasible.

### Signals shall have a clear definition without ambiguities

It shall be possible to interpret a signal value by reading the signal description.
Describe if needed how the value shall be calculated/interpreted,
for example if it is based on a standard or if it is up to the manufacturer to select algorithm/method.

* Example: A signal Vehicle.Weight would be ambiguous unless you specify that it refers to e.g. gross weight or curb weight.
* Example: Specifying an allowed value `MODE_2` is ambiguous unless you also specify what `MODE_2` means, e.g. by referring to a standard.

### No duplicates

VSS generally avoids to have duplicates in the signal tree, i.e. signals with same purpose and description in different part of the tree.

### Use existing style

Try to reuse the same style as used for existing signals.
Only specify min/max-values if there is a logical reason to limit the range.
Boolean signals should start with `Is*`.
American English is preferred over British English.
Follow the style guide in the [documentation](https://covesa.github.io/vehicle_signal_specification/rule_set/basics/#style-guide).

### No scaling, SI-unit, natural datatype

VSS is not concerned with how signals are transmitted, and does not consider scaling/offset typically used in transport protocols.
VSS signals typically use the unit used by humans when talking about the value, but prefers SI-units when feasible,
see [documentation](https://covesa.github.io/vehicle_signal_specification/rule_set/data_entry/data_unit_types/) for all supported units.
If it is unlikely that someone is interested in decimals for this value, select a signed or unsigned integer type.
Select a size which with reasonable margins can cover all vehicles.
If it is likely that decimal values are needed select float or if relevant double.

### Avoid backward incompatible changes

VSS sometimes change or remove existing signals, but only if there is a good reason.
Merging can be delayed, as VSS may decide to wait with the change until the next major release is prepared.

### Getting Support

To avoid time consuming refactoring it could for bigger contributions be relevant to ask VSS if the wanted changes
seems to be reasonable and likely will be accepted by VSS. Create an [issue](https://github.com/COVESA/vehicle_signal_specification/issues)
and describe what you intend to do and ask for feedback. You can also create a draft pull request at an early stage and ask for comments.

