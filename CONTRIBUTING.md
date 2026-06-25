# Introduction to ACEA namespace Contribution
The `acea-namespace` branch is managed/maintained by the ACEA TaskForce Heavy Duty Electronic Interface: Onboard API expert group. All contribution to this branch is driven by the ACEA expert group.

## Creating a Pull Request towards VSS ACEA namespace
This is the typical workflow for preparing a pull request. A GitHub account is required.

1. Create a fork of the VSS repository.

    **NOTE:** You need to fork all branches from the COVESA VSS repo, the ACEA VSS tree is sitting on the `acea-namespace` branch.

2. Clone the forked repository into your local development environment.

    **NOTE:** Git by default will clone the master branch, you need to clone the `acea-namespace` branch

    ```console
    git clone -b acea-namespace --single-branch <repository-url>
    ```

3. Set up your local development environment and [install pre-commit checks](BUILD.md#pre-commit-checks), see BUILD.md for some guidance.
5. Introduce the wanted changes or extensions in your local development environment, see guidelines below. If you want change/extend ACEA VSS-signals, it is the *.vspec3 files in the templates folder that needs to be updated.
6. Verify that your changes fulfill Continuous Integration requirements, see BUILD.md for some guidance.
7. Create a commit and upload to your own fork.
8. In the GitHub UI, create a Pull Request from your fork to the `acea-namespace` branch of the VSS repository. The PR title shall always start with `acea-namespace: `
9. Validate that automatic build checks for the PR succeed.

## Guidelines and Recommendations
This section includes general guidelines and recommendations for anyone interested in contributing to VSS `acea-namespace`.

Every contribution (commit) must carry the following sign-off line with your real name and email address:

```console
Signed-off-by: Firstname Lastname <you@example.com>
```

If using git command line you can add a sign-off by using the -s argument when creating a commit.

For certain files it is requested that a copyright and license statement is added as file header. This currently applies to the following file types:

VSS template files (*.vspec3)

VSS source files (*.vspec)

```console
# Copyright (c) {year} Contributors to COVESA
#
# This program and the accompanying materials are made available under the
# terms of the Mozilla Public License 2.0 which is available at
# https://www.mozilla.org/en-US/MPL/2.0/
#
# SPDX-License-Identifier: MPL-2.0
```

Where {year} is the year the file was originally created. No need to update or append new years or a range of years later.
