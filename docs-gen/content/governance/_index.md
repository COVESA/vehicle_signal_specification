---
title: Governance
weight: 15
chapter: false
---

# Governance

The Vehicle Signal Specification (VSS) project is an initiative by [COVESA](https://www.covesa.global/) to define a syntax and a catalog for vehicle signals.

The artifacts maintained by the VSS project consist of:

* Source code, documentation and releases in the [VSS github repository](https://github.com/COVESA/vehicle_signal_specification).
* Tools for parsing and converting VSS files in the [VSS-tools github repository](https://github.com/COVESA/vss-tools).

The VSS project has an informal structure with a chair and github maintainers appointed by COVESA.
Tasks for the chair includes hosting regular meeting to discuss incoming pull requests and issues, as well as roadmap and release planning.

## Contribution process

Anyone may propose changes to VSS. It is up to the VSS project to decide if the changes are feasible to include in VSS.
The VSS project does not have any developers or maintainers paid by COVESA.
Instead, the VSS project relies on voluntary contributions, typically from member organizations.
The maintainers are expected to review incoming pull requests.
All contributions must follow the [COVESA contribution guidelines](https://www.covesa.global/contribute).

In general, pull requests shall be opened for at least a week before being merged to give time for COVESA members to review the pull request and provide comments.
In case of larger changes or changes that affect backward compatibility pull requests are typically opened for a longer period, to allow for a through review.
Pull requests, unless trivial, are typically merged first after a decision at one of the regular VSS meetings, see link at [COVESA VSS wiki page](https://wiki.covesa.global/display/WIK4/VSS+-+Vehicle+Signal+Specification).
These rules concerns primarily normative content (see below), non-normative content may be updated without thorough reviews.

For more information and guides on how to contribute see [CONTRIBUTING.md](https://github.com/COVESA/vehicle_signal_specification/blob/master/CONTRIBUTING.md).

## Branches

VSS development is typically developed in the master branch only.
Each release is tagged and a maintenance branch is created (e.g. `release/3.0`) which could be used as target for pull requests intending to patch a release.

## Normative vs. non-normative content

The VSS repositories contain some artifacts that can be considered normative, i.e. an implementation claiming to "support" VSS shall:

* Support signals defined according to the rules in the VSS documentation
  ([source](https://github.com/COVESA/vehicle_signal_specification/tree/master/docs-gen), [generated](https://covesa.github.io/vehicle_signal_specification/))
* Support the signals currently defined in VSS.
    * The signals in source format (*.vspec files) can be found in [Github repository](https://github.com/COVESA/vehicle_signal_specification/tree/master/spec).
    * Derived formats supported by VSS project are included in each [release](https://github.com/COVESA/vehicle_signal_specification/releases), 
      originating from the tools in the [VSS-tools github repository](https://github.com/COVESA/vss-tools).

In addition to this the VSS repositores contain artifacts that currently are considered non-normative. This includes immature concepts and work-in progress. Non-normative content include:

* [VSS Github Wiki](https://github.com/COVESA/vehicle_signal_specification/wiki)
* [VSS Tools Wiki](https://github.com/COVESA/vss-tools/wiki)
* [Overlays and Profiles](https://github.com/COVESA/vehicle_signal_specification/tree/master/overlays)
* [Contributed tools](https://github.com/COVESA/vss-tools/tree/master/contrib)

The list of what is considered normative and non-normative is no static, it may change over time.

## Handling of backward compatibility

The VSS project aims to keep backward compatibility as far as feasible.
VSS is however an evolving syntax and catalog and there are still areas where changes are need to fit the need of users.
Changes that breaks backward compatibility are typically introduced only in major releases (e.g. `X.0`) and shall be documented in release notes.
This concerns changes to syntax and signals, but also to tools.

The VSS project has introduced a [deprecation concept](../rule_set/basics.md#deprecation-since-version-21).
If possible, when e.g. renaming or moving a signal or changing tools the old signal or parameter set shall be kept but marked as deprecated.
That allows the change to be introduced in a minor version (e.g. `X.Y`). The old signal shall be removed first in the next major release, or later if needed.

A history of past changes and planned changes that affects backward compatibility can be found in the [Changelog](https://github.com/COVESA/vehicle_signal_specification/blob/master/CHANGELOG.md).

## Release Process

The release process is further described in the [Github repository](https://github.com/COVESA/vehicle_signal_specification/blob/master/RELEASE_PROCESS.md).

