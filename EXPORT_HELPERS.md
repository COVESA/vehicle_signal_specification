## Proposal / Discussion Draft: Consistent & Documented Export Formats

Goal of this proposal is to produce consistent and conformant formatted exports of the VSS via
the VSS-TOOLS or other potential 3rd-party implementations, resulting in a high degree of stability and
interoperability between implementations using a particular format (such as IDL).

This consistency and stability can ease the creation of interoperable examples and reference implementations for a given format.  
This draft focuses on IDL, but is intended to also maximize interoperability within other export formats.

To enable this capability, the following changes are proposed:

- Create a document to describe the recommended formatting and structure of the resulting exported (IDL or other) files.
- Modify the exporters in VSS-TOOLS to conform to the above document.
- Utilize the `arraysize` and `stringsizemax` to set the dimensions of the exported array/sequence/string types.
- Introduce 3 new keywords to the VSS: `memberof`, `membergroup`, `isogroup`, used as:
    - To have a `branch` entity create a namespace in the export (named for itself), add:
        - `memberof: namespace`
    - To create named group containers in the export for elements, add to the branch entry:
        - `membergroup <list of names>` to create containers that may also be referenced in the parent of this branch.
        - `isogroup <list of names>` to create containers that will not be referenced in the parent of this branch.
    - To assign `membergroup` struct names to be referenced in a parent struct:
        - `memberof: <list of parent struct names to insert reference into>`
    - To assign VSS elements to specific named group containers in the export, add to element entry:
        - `memberof: <list of group containers>`

## Effect on IDL Export
Implementing the above keywords into the VSS -- to enforce the guidance of the above reference document -- 
should have no effect on existing exporters in VSS-TOOLS, however a modified IDL exporter could use this new
information to consistently produce IDL that conforms to the above document.

Examples of this export guidance on IDL includes:  

### Namespaces
In IDL, namespaces are expressed with a `module { ... }` container around the affected definitions.
A sensible approach to namespacing in VSS would be to use containers for the major sections of
the specification, such as: `ADAS`, `Body`, `Cabin`, `Chassis`, `OBD`, and `Powertrain`, all residing
within a top-level container for `Vehicle`.   The resulting IDL would look like:
```
  module Vehicle {
    module Cabin {
      (struct and enum definitions for Cabin descendants)
    };
    module Chassis {
      (struct and enum definitions for Chassis descendants)
    };
  };
```
Note that only the `branch` entries that have this keyword will receive a namespace for their descendent types.
All `branch` entries beneath them will be implemented as `struct`.

### Creating structs from VSS elements
Using the new keywords to define and assign elements to structs, the VSS can be tailored to match the intended usage
patterns of the underlying signals, assinging them to one or more structs.  

Some signals should 'obviously' be grouped together, such as `Vehicle.AngularVelocity`, `Vehicle.CurrentLocation`, etc..,
```
Vehicle.AngularVelocity
  float Roll sensor
  float Pitch sensor
  float Yaw sensor
```
This should result in structs that match this most likely usage pattern:
```
  struct AngularVelocity {
    float Roll;
    float Pitch;
    float Yaw;
  };
```

Other signals are not as clear in their implied grouping, such as the signals directly under `Vehicle`:
```
  string StartTime attribute
  int16 RoofLoad attribute
  float CargoVolume attribute
  int16 EmissionsCO2 attribute
  uint16 CurbWeight attribute
  uint16 GrossWeight attribute
  uint16 MaxTowWeight attribute
  uint16 MaxTowBallWeight attribute
  uint16 Length attribute
  uint16 Height attribute
  uint16 Width attribute
  string LowVoltageSystemState sensor
  float Speed sensor
  float TravelledDistance sensor
  float TraveledDistance sensor
  float TraveledDistanceSinceStart sensor
  float TripDuration sensor
  boolean IsBrokenDown sensor
  boolean IsMoving sensor
  float AverageSpeed sensor
  uint16 CurrentOverallWeight sensor
  float TripMeterReading actuator
  uint8 PowerOptimizeLevel actuator
```
Even if split into separate structs for `attribute`, `sensor`, and `actuator`, using this "implied-by-proximity"
grouping might not represent the actual usage pattern of each VSS member.

However, if each VSS member could be assigned to a named struct, then the expected usage patterns for all signals
could be mapped and made part of the VSS specification itself.   This could result in data type (struct) definitions
such as:
```
  struct VehicleAttributes {
    string StartTime;
    int16 RoofLoad;
    float CargoVolume;
    int16 EmissionsCO2;
    uint16 CurbWeight;
    uint16 GrossWeight;
    uint16 MaxTowWeight;
    uint16 MaxTowBallWeight;
    uint16 Length;
    uint16 Height;
    uint16 Width;
  };
  struct Vehicle_Sensor_customName_whatever {
    string LowVoltageSystemState;
    float Speed;
    float TravelledDistance;
    float TraveledDistance;
    float TraveledDistanceSinceStart;
    float TripDuration;
    boolean IsBrokenDown;
    boolean IsMoving;
    float AverageSpeed;
    uint16 CurrentOverallWeight;
  };
```
To handle both cases above, the `memberof` and `membergroup`/`isogroup` keywords are used on the member elements and their 
containing branch definitions:
```
AngularVelocity:
  type: branch
  description: Spatial rotation. Axis definitions according to ISO 8855.
  memberof: VehicleTop
  membergroup: VehicleAngularVelocity

AngularVelocity.Roll:
  datatype: float
  type: sensor
  unit: degrees/s
  description: Vehicle rotation rate along X (longitudinal).
  memberof: VehicleAngularVelocity

AngularVelocity.Pitch:
  datatype: float
  type: sensor
  unit: degrees/s
  description: Vehicle rotation rate along Y (lateral).
  memberof: VehicleAngularVelocity

AngularVelocity.Yaw:
  datatype: float
  type: sensor
  unit: degrees/s
  description: Vehicle rotation rate along Z (vertical).
  memberof: VehicleAngularVelocity
```
Note that this enables branches to create multiple struct definitions, and signals to be assigned to multiple struct defintions.


### Including Descendent Structs in Parent Structs
The VSS structure in some places implies that a struct might be included in its parent struct, 
such as how `Vehicle.Powertrain.TractionBattery` might want to include its `Temperature` and `StateOfCharge` 
descendant structs -- but there is no directive in the VSS to enforce this grouping.

The added keywords could enforce the inclusion of references to descendant types within a parent,
enabling data structures such as:
```
  module Vehicle {
    module Powertrain {
      struct TractionBattery_Temperature {
        (temperature members)
      };
      struct TractionBattery_StateOfCharge {
        (stateOfCharge members)
      };
      struct TractionBattery_Sensors {
        (sensor member elements of TractionBattery)
        TractionBattery_Temperature Temperature;
        TractionBattery_StateOfCharge StateOfCharge;
      };
    };
  };
```

## Other export rules to be defined in document
The behaviors of format-specific features that do not require assistance in the VSS will be defined
in the controlling document for each format (IDL, etc.).  For the IDL example, this might include:

- How to interpret VSS `instances`, as they can translate nicely to DDS keyed topics with an enumerated key value, or to a non-keyed topic that uses content filtering.
- How to interpret VSS `allowed` values; as enums, or string values.
- How to ensure `enum` members do not have namespace collisions with other enum members, including when used with `C` programming language.


## Rationale
This change seeks to enable VSS to take the most advantage of the capabilities of the exported-to technology.
In this first example, the target is IDL and DDS.  
DDS (Data Description Service) is a (very) data-centric communications framework that uses IDL as its primary type definition language.
DDS has a large number of tunable features / QoS / security / capabilities that enable it to work in extremely challenging environments
where TCP/UDP alone cannot, all while decoupling the applications from these transport-level troubles.

Systems based on DDS do well by having a defined set of data types, from which many applications can be created and will be
assured of interoperability by using common data type definitions.   This approach has been very successful in the ROS
(Robot Operating System) ecosystem, which uses a common set of data types and a data-centric communications framework (DDS)
to ensure interoperability between independently-created applications.

This is why it's so important when expressing the VSS in IDL that the resulting data type (struct) definitions:
- represent the usage patterns of the member signals (signals are grouped together per their use)
- retain a stable and consistent definition (to ensure long-term interoperability)

In short, this proposal seeks to enable the VSS to be more concisely defined at the implementation end.

(Looking forward to a lively discussion :) 