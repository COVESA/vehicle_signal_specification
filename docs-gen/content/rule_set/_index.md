---
title: Rule Set
weight: 20
chapter: true
---

# Rule Set

The `Rule Set` of a [domain taxonomy](/vehicle_signal_specification/introduction/taxonomy/) is used to describe how to write the data definition syntactically.

This chapter defines and describes the rule set for VSS.
Tools in the [vss-tools repository](https://github.com/COVESA/vss-tools) can be used to validate that a specification follows the rule set for VSS,
but those tools may have limitations and may not check all rules stated in this document.
In case of conflict, what is stated in the rule set in this documentation is considered to have precedence over tool implementations.

## Version handling

The source for the rule set is in [VSS Git repository](https://github.com/COVESA/vehicle_signal_specification/tree/master/docs-gen/content).
The online version of the rule set in the [generated VSS documentation](https://covesa.github.io/vehicle_signal_specification/)
is updated whenever a new commit is merged to the VSS master branch and does this not necessarily correspond to the rule set for the last release VSS version.

To highlight important changes to the VSS rule set two notations are used in the documen

* `since version X.Y` means that the concept/syntax was introduced in version X.Y. Older tools not supporting VSS version X.Y may not support this concept/syntax.
* `deprecated since version X.Y` means that the concept/syntax is no longer recommended from version X.Y onwards. The concept/syntax may be removed in the next major release.
