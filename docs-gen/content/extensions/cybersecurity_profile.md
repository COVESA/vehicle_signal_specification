---
title: "Cybersecurity Profile"
weight: 10
---

This profile can be used to specify how VSS signals can be extended to include cybersecurity attibutes.

## Mapping Syntax

The syntax for definition of a signal with cybersecurty attributes (in an overlay) is specified below.

```yaml
<VSS Signal name>:
  type: <VSS type>
  datatype: <VSS datatype>
  cybersecurity:
    [authentication: {true|false}]
    [encryption: {true|false}]
    [integrity_check: {true|false}]
    [impact_profiles: {[{motion|privacy|regulation|safety|operational}]}]
```
- Set `authentication` attribute to true if you need to ensure serialized data is being exchanged between trusted entities or prevent unauthorized access to serialized data during transmission. Sample implementation mechanisms are public-key infrastructure, token based authentication etc.
- Set `encryption` attribute to true to protect the confidentiality of serialized data or to ensure that even if serialized data is intercepted, it cannot be easily understood or misused. Sample implementation mechanisms are symmetric (e.g AES), asymetric (e.g RSA) or end-to-end encryption.
- Set `integrity_check` attribute to detect and prevent unauthorized alterations to serialized data or to maintain the accuracy and reliability of data as it is transmitted or stored. Sample implementation mechanisms are checksums, counters, hash based, message authentication codes etc
- `impact_profiles` attribute indicate set of impact profiles that assess potential consequences of security issues. Possible values include:
  - `motion`: Impact on vehicle movement or control systems.
  - `privacy`: Impact on the privacy of individuals and data protection.
  - `regulation`: Impact related to regulatory compliance and legal issues.
  - `safety`: Impact on personal safety and potential physical harm.
  - `operational`: Impact on system functionality and service availability.

### Example
```yaml
Vehicle.Body.Mirrors.DriverSide.Tilt:
  datatype: int8
  type: actuator
  cybersecurity:
    authentication: false
    encryption: false
    integrity: true
    impact_profiles: [operational]
```
