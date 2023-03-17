# Proposal to add Suggested Lengths for String Signals in the VSS

This document covers a concept proposal to add to the VSS .vspec files an additional keyword 
(`stringsize:` or similar) to assist the code generators (in vss-tools) in setting an appropriate
default size for strings.

This new keyword would be added to the .vspec files for all `datatype: string` elements (approx. 85 places),
and would also affect the arrays-of-strings (`datatype: string[]`, approx 6 places) to set a
correctly-sized default boundary length on these string members.

A few additional questions have been added below as well, for discussion in VSS meetings.


## Rationale

When creating software for a system with safety, security, or resource constraints, the use of 
unbounded variables is strongly discouraged.   Unless extra steps are taken to limit their size,
they can act as a vector for instability and exploitation.

In practice, the signals in the VSS will never require unbounded lengths.  Some string signals
in the VSS include the length in its `description:` field, but this information is not available for 
every `string` signal.  Specifying the `stringlength`, and the `arraysize` of VSS elements can help
create more concise implementations of the VSS, and reduce the burden on users.


## Proposed Implementation

The proposed implementation would add in the .vspec files a new key:value pair (herein called `stringlength:`) 
to set the string length of any signal with a `string` or `string[]` datatype.  
When used with arrays-of-strings (`string[]`), this keyword sets the max length of the strings in the array, while
the existing `arraysize` keyword sets the number of strings in the array.


## Examples from VSS

An example implementation might look like:
```
VehicleIdentification.VIN:
  datatype: string
  stringlength: 17
  type: attribute
  description: 17-character Vehicle Identification Number (VIN) as defined by ISO 3779.
```

An array-of-strings example might be:
```
DTCList:
  datatype: string[]
  stringlength: 6
  arraysize: 20
  type: sensor
  description: List of currently active DTCs formatted according OBD II (SAE-J2012DA_201812) standard ([P|C|B|U]XXXXX )
```
In this example, `stringlength` was estimated from the text in `description`, and `arraysize` was set to 
a value (20) based on an unqualified guess of what a reasonable number of DTCs should be.

In some instances, the string length and array dimensions are implied by the use of `allowed` elements, 
and do not need to be explicity stated:
```
SmartphoneProjection.SupportedMode:
  datatype: string[]
  type: attribute
  allowed: [ 'ANDROID_AUTO', 'APPLE_CARPLAY', 'MIRROR_LINK', 'OTHER' ]
  description: Supportable list for projection.
```
In this case, if this were to be implemented as an array-of-strings the `arraysize` can be obtained from the 
length of the `allowed` list, and the `stringlength` can be found from the length of the longest string in
the `allowed` list.   The `stringlength` concern does not apply if this is implemented as an array of `enum`
(integer) values created from the `allowed` list.  (see question below about 'Allowed Values')


## Questions Raised in Writing this Proposal

### Allowed Values: Is there a recommendation or enforcement on how this should be implemented in code?

In the VSPEC files, most `string` members are used to hold `allowed:` values, contained in a list of strings.
This list could be implemented in code as an `enum`, or as a verbatim array of strings, or using an order-preserving
container such as: `sequence` / `vector` / `list` of strings.  In each case, the index/enumeration would be 
the same (enum 0 == index 0, etc.).  Is there any guidance on this?   
(this is a potential place for improving the Wiki documentation.)

### Should this be used to specify fixed sizes, or an allowed range (min:max) of sizes for the element?

Open for discussion.

### Should this accommodate NULL-termination on strings, or be sized exact?

Open for discussion.

### Can `arraysize` be implemented on the arrays in the VSPEC files?

For example:
```
SeatPosCount:
  datatype: uint8[]
  type: attribute
  default: [2, 3]
  description: Number of seats across each row from the front to the rear.
  comment: Default value corresponds to two seats in front row and 3 seats in second row.
```

A default value is used here and it *implies* the dimension of the array, but it also could be
misread as "this array has a default size of 2x3 elements".  This seems like a good place to be explicit in the
array dimensions, by including the `arraysize` keyword and value.
Apologies if this has been implemented in a *development* branch of the VSS.


## Impact to Existing Uses

With limited testing, this new keyword appears to be ignored by the parser in VSS-TOOLS, so it should
be safe to add without breaking compatibility.   Should this be implemented in VSS, then it should
also be supported in VSS-TOOLS, for use in the generators that are capable of setting variable sizes.
