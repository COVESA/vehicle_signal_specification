# Introduction to VSS Contribution Process

The COVESA VSS project has two public GitHub repositories:

- [Vehicle Signal Specification (VSS)](https://github.com/COVESA/vehicle_signal_specification), containing signal specifications and documentation.
- [VSS Tools](https://github.com/COVESA/vss-tools), containing tools for validating and transforming VSS specifications.

The examples below refer to the VSS repository, but the process is similar for the VSS-Tools repository.

There are two main methods to propose changes or extensions to VSS:

- If you have an idea or a question you can create an [issue](https://github.com/COVESA/vehicle_signal_specification/issues) in GitHub.
- If you already have prepared changes or extension that you think would be interesting for COVESA to include in VSS
  then you can create a [Pull Request (PR)](https://github.com/COVESA/vehicle_signal_specification/pulls).

All contributions must follow the [COVESA contribution guidelines](https://covesa.global/contribute).

The VSS project has regular meetings on Tuesdays at 16.00 CET and CEST in the summer (see [COVESA VSS Wiki](https://wiki.covesa.global/display/WIK4/VSS+-+Vehicle+Signal+Specification)).
In the meetings Pull Requests (PRs) and Issues are discussed and, if a Pull Request is accepted, a decision to merge the PR will be made.
Everyone interested is welcome to join the meetings.

## Creating a Pull Request towards VSS

This is the typical workflow for preparing a pull request. A GitHub account is required.

1. Create a personal or company fork of the [VSS repository](https://github.com/COVESA/vehicle_signal_specification)
   and/or [VSS-Tools repository](https://github.com/COVESA/vss-tools).
2. Clone the forked repository into your local development environment.
3. Set up your local development environment, see [BUILD.md](BUILD.md) for some guidance.
4. Create a local branch based on the VSS master branch to use for the proposed changes.
5. Introduce the wanted changes or extensions in your local development environment, see guidelines below.
   If you want change/extend VSS-signals, it is the *.vspec files in the [spec](https://github.com/COVESA/vehicle_signal_specification/tree/master/spec) folder that
   needs to be updated.
6. Verify that your changes fulfill VSS Continuous Integration requirements, see [BUILD.md](BUILD.md) for some guidance.
7. Create a commit and upload to your own fork.
8. In the GitHub UI, create a Pull Request from your fork to the master branch of [the VSS repository](https://github.com/COVESA/vehicle_signal_specification).
9. Validate that automatic build checks for the PR succeed.

## Handling of the created Pull Request

1. The PR creator shall follow up on any comments or questions received on the Pull Request.
2. The PR will be discussed at one of the next VSS weekly meetings.
   It is preferable if the PR creator can participate and give a quick introduction on the rationale for the change.
3. Unless trivial, PRs shall typically be open for at least a week before merging is considered, to give time for comments.
4. If needed, the PR creator needs to refactor the PR to address received comments and remarks.
4. After a while, if all comments and concerns have been sorted out and no-one objects merging, a decision will be made in the meeting to merge the PR.
   It is not guaranteed that all PRs will be accepted. The VSS meeting may reject and close Pull Requests.
5. A VSS maintainer will perform the final merge.

## Guidelines and Recommendations

This section includes general guidelines and recommendations for anyone interested in contributing to VSS.

### All contributions must follow COVESA contribution guidelines

COVESA has defined [contribution guidelines](https://covesa.global/contribute).

Every contribution (commit) must carry the following sign-off line with your real name and email address:

`Signed-off-by: Firstname Lastname <you@example.com>`

By supplying this sign-off line, you indicate your acceptance of the COVESA Certificate of Origin.

If using git command line you can add a sign-off by using the `-s` argument when creating a commit.



### Getting Support

To avoid time consuming refactoring it could, for bigger contributions, be relevant to ask VSS if the wanted changes
seems to be reasonable and likely will be accepted by VSS. Create an [issue](https://github.com/COVESA/vehicle_signal_specification/issues)
and describe what you intend to do and ask for feedback. You can also create a draft pull request at an early stage and ask for comments.
