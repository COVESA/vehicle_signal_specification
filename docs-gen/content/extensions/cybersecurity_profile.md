---
title: "Cybersecurity Profile"
weight: 10
---

This profile can be used to record the **cybersecurity needs** of a VSS signal in an overlay. It is informative and optional.
The goal is that someone who knows the use case, but is not a security specialist, can state what a signal needs.
VSS defines the keywords and their allowed values; example overlays show the syntax. VSS itself assigns no values to signals.

## Mapping Syntax

The syntax for a signal with cybersecurity attributes (in an overlay) is specified below.

```yaml
<VSS Signal name>:
  type: <VSS type>
  datatype: <VSS datatype>
  cybersecurity:
    [confidentiality: {required|not_required|not_assessed}]
    [integrity: {required|not_required|not_assessed}]
    [availability: {required|not_required|not_assessed}]
    [extensions:
      [privacy: {required|not_required|not_assessed}]
      [authenticity: {required|not_required|not_assessed}]
      [non_repudiation: {required|not_required|not_assessed}]
      [authorization: {required|not_required|not_assessed}]
      [access_control: {required|not_required|not_assessed}]
      [timeliness: {required|not_required|not_assessed}]]
    [impact_profiles: [{motion|privacy|regulation|safety|operational|financial}]]
    [sesip_sfrs: [<SESIP requirement id>]]
```

The attributes are enabled per tool run as an extended attribute, for example:

```bash
vspec export json -s spec/VehicleSignalSpecification.vspec \
  -l overlays/extensions/cybersecurity.vspec \
  -e cybersecurity -o vss_cybersecurity.json
```

## The taxonomy

Confidentiality, Integrity and Availability are the three roots. Every other property extends at least one root, so a
need can always be traced back to C, I or A.

```
            Confidentiality
             └─ privacy
   Integrity                 Availability
    ├─ authenticity           ├─ access_control
    ├─ non_repudiation        └─ timeliness
    └─ authorization ── also extends availability
```

Most extensions have one root. `authorization` has two: an unauthorized write or actuation breaks integrity, and
availability means usable on demand *by an authorized party*.

| Key | Extends | Meaning |
|-----|---------|---------|
| `confidentiality` | (root) | The value must not be disclosed to unauthorized parties. |
| `integrity` | (root) | Unauthorized modification of the value must be detectable. |
| `availability` | (root) | The value must remain accessible to authorized consumers when needed. |
| `privacy` | confidentiality | The value relates to an identifiable person. Privacy can be breached even when the value stays secret, for example by keeping it too long or linking it to a person. |
| `authenticity` | integrity | A consumer must be able to verify that the value comes from the expected source. |
| `non_repudiation` | integrity | The origin of a value or command must be provable afterwards. |
| `authorization` | integrity, availability | The rights to read, write or actuate the signal are granted only to permitted parties. |
| `access_control` | availability | Every access to the signal is checked against those rights where it happens. |
| `timeliness` | availability | The value must arrive within its deadline; a late value can be as harmful as a missing one. This is distinct from freshness, which protects against replay and belongs to integrity. |

- Every key takes one of `required`, `not_required` or `not_assessed`. `not_assessed` is not the same as
  `not_required`: it records that nobody has decided yet, so tools must not read it as "no protection needed".
- Extensions sit under an `extensions` block.
- Audit is not a property of its own. It is the evidence that the other properties hold, and it applies across all
  three roots.
- `impact_profiles` lists the kinds of harm a compromise could contribute to. It names categories only and is not an
  impact rating. Possible values:
  - `motion`: impact on vehicle movement or control systems.
  - `privacy`: impact on the privacy of individuals and data protection.
  - `regulation`: impact related to regulatory compliance and legal issues.
  - `safety`: impact on personal safety and potential physical harm.
  - `operational`: impact on system functionality and service availability.
  - `financial`: financial loss for the vehicle user or another stakeholder.

  `safety`, `financial`, `operational` and `privacy` are the damage-scenario impact categories of ISO/SAE 21434, so a
  risk assessment can take them over directly.
- `sesip_sfrs` (optional) names GlobalPlatform SESIP security functional requirements that a component handling the
  signal is expected to address, by the ids defined in `overlays/extensions/cybersecurity_sesip_mapping.yaml`. Leave it
  out to let tools derive the requirements from the properties (see below); state it when a use case already knows them.

## Why these properties

The three roots are the cybersecurity properties named by ISO/SAE 21434 (confidentiality, integrity, availability), and
`authenticity`, `authorization` and `non_repudiation` are the further properties commonly analysed alongside them. The
remaining extensions close gaps that come up when describing vehicle signals:

- `privacy`: a signal can be kept secret and still be misused, for example a location stored too long or linked to a
  driver. Data protection law treats this separately from confidentiality.
- `access_control`: `authorization` says who may use a signal; `access_control` says that every access is actually
  checked where it happens, for example at a gateway or a diagnostic interface.
- `timeliness`: for actuation and safety-relevant signals, a correct value that arrives too late is a failure of
  availability, and it needs different protection than a missing value.

Each extension sits under the root whose loss it describes, so a tool that only understands C, I and A can still read the
need correctly.

## Relation to GlobalPlatform SESIP

This profile is the vehicle-signal side of a path that continues in GlobalPlatform's SESIP (Security Evaluation
Standard for IoT Platforms, GP_FST_070):

```
use case → properties each signal needs (this profile)
         → SESIP requirements that address those properties (the mapping below)
         → SESIP profile and level, assurance (CAL / TAF)  ← per vehicle, from its risk assessment
         → component configuration, reviewed by a person   ← per vehicle
```

`overlays/extensions/cybersecurity_sesip_mapping.yaml` holds the mapping in machine-readable form: the SESIP requirement
ids and, per property, the requirements that typically address it.

| Property | SESIP requirements that typically address it |
|---|---|
| `confidentiality` | Secure Communication Support / Enforcement; Secure Confidential Storage; Secure Encrypted Storage; Cryptographic Operation; Cryptographic KeyStore |
| `privacy` | Secure Confidential Storage; Residual Information Purging; Field Return of Platform |
| `integrity` | Secure Communication Support / Enforcement; Secure Trusted Storage; Secure Initialization of Platform; Secure Update of Platform |
| `authenticity` | Verification of Platform Identity; Verification of Platform Instance Identity; Attestation of Platform Genuineness; Secure Communication Support |
| `non_repudiation` | Audit Log Generation and Storage; Cryptographic Operation |
| `authorization` | Authenticated Access Control; Privileged Access Control |
| `availability` | Secure Update of Platform; Isolation of Platform Parts |
| `access_control` | Authenticated Access Control; Isolation of Platform; Isolation of Application Parts |
| `timeliness` | No dedicated SESIP requirement; addressed at system level |

The mapping is informative. It selects no SESIP profile, sets no SESIP level and is not conformity evidence: which
requirements a component must meet, and at which level, follows from the vehicle's risk assessment.

## From use case to properties

Start from the use case, not from the signal. A storyline such as "a rental company unlocks the car for a verified
driver and bills the insurance per trip" names who acts on which data, under which conditions. The properties each
signal needs follow from that storyline, and the same signal can need different properties in a different use case.

## What these attributes are not

- **Not a rating.** They state what a signal needs, not how severe a compromise would be in a particular vehicle.
- **Not a control.** `integrity: required` says the value needs integrity protection. It does not say which mechanism
  provides it.
- **Not an assurance level.** How much assurance a property needs is determined later, from the use case and the risk
  assessment.
- **Not conformity evidence.** A filled overlay is an input to a risk assessment, never its result.

Which assurance level a need requires, which ECU sends and receives the signal, over which medium, whether that medium
can carry the protection, and how keys, freshness and message authentication are planned along the signal's path, all
depend on the vehicle's architecture and its risk assessment. They are intentionally not modelled in this profile.

## Earlier attributes

Earlier versions of this profile used boolean attributes. They remain valid; tools should read them as the
corresponding new keys, and when both are given the new key takes precedence. The earlier example wrote
`integrity: true`; read a boolean `integrity` as `integrity_check`. A string value of `integrity` is the new key.

| Earlier attribute | Read as |
|---|---|
| `encryption: true\|false` | `confidentiality: required\|not_required` |
| `integrity_check: true\|false` | `integrity: required\|not_required` |
| `authentication: true\|false` | `extensions.authenticity: required\|not_required` |

## Example

```yaml
Vehicle.Cabin.Door.Row1.DriverSide.IsLocked:
  datatype: boolean
  type: actuator
  cybersecurity:
    confidentiality: not_required
    integrity: required
    availability: required
    extensions:
      authenticity: required
      authorization: required
      access_control: required
      non_repudiation: not_assessed
    impact_profiles: [safety, financial]
    sesip_sfrs: [authenticated_access_control, secure_communication_support]
```

See `overlays/extensions/cybersecurity.vspec` for more examples. All example values are illustrative: they are not
recommendations, not ratings and not conformity evidence for any vehicle.
