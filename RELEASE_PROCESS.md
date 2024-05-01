**Copyright (c) 2016 Contributors to COVESA**<br />

All files and artifacts in this repository are licensed under the
provisions of the license provided by the LICENSE file in this repository.

# RELEASE PROCESS
This document describes the process for creating a new version of the
signal specification.

The process, driven by COVESA with significant input from the W3C Automotive WG, is aimed at being lightweight and carried
out in public, giving both COVESA members and non-members a say in the
creation of a new version.

![Release Process](pics/vss_release_process.png)

In git, the ```master``` branch is used as an integration branch
accepting pull requests with new and modified vpsec files from
contributors.

Pull requests [PR] are **always** initiated from a **fork** and not through
a feature branch in the main repository. PRs are reviewed, discussed and merged
through the public GitHub repository.
A PR is merged earliest after one week to give a fair chance of reviewing.

Each release is incrementally numbered, starting with 1.

A release is tagged in git with the tag:

    v[m.n]

where [m.n] is the release number.

Detailed instructions on how releases are created can be found in the
[Release Instructions and Checklist](https://github.com/COVESA/vehicle_signal_specification/wiki/Release-Instructions-and-Checklist).
