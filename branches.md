# COVESA VSS Handling

*Note: This file is not intended to be merged; it shall rather be integrated in the wiki*
*Currently added as PR to simplify discussion/review*

## Branches

Branch type | Example | Purpose | Stability | Lifetime
------------|---------|---------|-----------|---------
default     | `master` | Default branch for new features/signals that will be included in next major release | Generally not thoroughly tested | Forever
Development branch for minor release    | `4.X` | Branch for new features/signals that will be included in next major release. Backward incompatible changes not accepted. | Generally not thoroughly tested | Created when the corresponding major release has been tagged/released. E.g. when `v5.0` is tagged we create a `5.X` branch. May be deleted when the corresponding major version has reached end-of-support
Release branches  | `release/4.0`, `release/4.1` | Branch for preparing a release and handling patches (if any) for a release. | Supposed to be thoroughly tested as soon as the corresponding tag has been created. After that only low-risk (patch) changes are accepted. | Created as part of the release process, when preparing for the first release candidate. Shall never be deleted

## Example work-flow

* New signal added to `master`, i.e. it will be included in next major release (5.0)
* As it as a change that does not affect backward compatibility it will also be included in the next minor release (if any) for supported versions. A maintainer will at latest during preparation for 4.2 cherry-pick the commit to the `4.X` branch
* When 5.0 release is being prepared a branch `release/5.0` is created from `master` at "feature freeze". Normal release preparations like updating CHANGELOG, versions and testing is performed. By using a separate branch for release preparations there is no need to "lock" the master branch for new features during the release preparation/stabilization period.
* When maintainer has performed all required steps a tag `v5.0rc0` is created and published and a release is created.
* If needed additional release candidates are created
* At earliest 2 weeks after the release candidate is created latest commit on `release/5.0` is tagged as `v5.0`
* At this time a branch `5.X` is created (from `v5.0`), for future minor releases based on 5.0 (like 5.1, 5.2)
* Fixes (if any) in the `release/5.0` branch is merged back to `master`.
* If a patch is needed (like 5.0.1) work for that can be performed within `release/5.0` branch.
* 6 months after the release the release candidate tags may be deleted


## Tags

Tag Type | Example | Purpose | Lifetime
------------|---------|---------|-------------------
Release    | `v5.0`, `v5.0.1` | Points to a specific release. Shall never be changed as soon as communicated. `vX.Y` is a short notation for `vX.Y.0`, i.e. even if `v5.0.1` is released the tag `v5.0` tag shall still point to the `v5.0.0` release and not `v5.0.1`. | Shall never be deleted as soon as "communicated"
Release Candidate   | `v5.0rc0` | Release candidate for a specific release. Shall never be changed as soon as communicated. Typically not created for path releases | May be deleted 6 months after release.
