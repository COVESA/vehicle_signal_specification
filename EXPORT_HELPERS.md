## Proposal / Discussion Draft: Consistent & Documented Export Formats

Goal of this proposal is to get consistent and conformant formatted exports of the VSS,
from VSS-TOOLS or other potential 3rd-party implementations, resulting in a high degree of
interoperability between implementations using a particular format (such as IDL), and to
ease the creation of interoperable examples and reference implementations for a given format.
This draft focuses on IDL, but is intended to also maximize interoperability within other export formats.

To enable this capability, the following changes are proposed:

- Create a document to describe the recommended formatting and structure of the resulting exported (IDL or other) files.
- Modify the exporters in VSS-TOOLS to conform to the above document.
- Utilize the `arraysize` and `stringsizemax` to set the dimensions of the exported array/sequence/string types.
- Introduce 3 new keywords to the VSS: `memberof`, `membergroup`, `isogroup` to be used as:
    - To have a `branch` entity create a namespace in the export (named for itself), add:
        - `memberof: namespace`
    - To create named group containers in the export for elements, add to the branch entry:
        - `membergroup <list of names>` to create containers that may be referenced in the parent of this branch.
        - `isogroup <list of names>` to create containers that will not be referenced in the parent of this branch.
    - To assign VSS elements to specific named group containers in the export, add to element entry:
        - `memberof: <list of group containers>`

## Effect on IDL Export
Implementing the above keywords into the VSS -- to enforce the guidance of the above reference document -- 
should have no effect on existing exporters in VSS-TOOLS, however a modified IDL exporter could use this new
information to consistently produce IDL that conforms to the above document.

Examples of this export guidance on IDL includes:  

**Namespaces**  
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

**Creating structs from VSS elements**  
Using the new keywords to define and assign elements to structs, the VSS can be tailored to match the intended usage
patterns of the underlying signals.  For example:

Some signals should 'obviously' be grouped together, such as `Vehicle.AngularVelocity`, `Vehicle.CurrentLocation`, etc..,
resulting in structs that match this most likely usage pattern:
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

**Including Descendent Structs in Parent Structs**
The VSS structure in some places implies that a struct might be included in its parent struct, 
such as how `Vehicle.Powertrain.TractionBattery` might want to include its `Temperature` and `StateOfCharge` 
descendant structs -- but there is no guidance in the VSS to support this grouping.

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
This change seeks to enable VSS to take the most advantage of the capabilities of IDL and DDS.
DDS (Data Description Service) is a (very) data-centric communications framework that uses IDL as its primary type definition language.
Systems built on DDS can take advantage of the features that are built-in to the DDS standard, thereby avoiding the need to create 
these features -- DDS handles it.  Some capabilities (in brief):

- **Content Filtering**: Subscribers to data topics can designate a filtering specification on the data elements within that topic, such as only allowing temperature readings if they are above 90C.  This filtering spec can be automatically moved to the *publisher* of that data, wherein it won't put data on the network if it doesn't meet the filter spec for the subscriber.

- **Keyed Topics**: a data type definition (struct) can have one or more members designated as a `key`; This key 
value will uniquely identify the source of the data, enabling many sources to share the same data topic 
without identity contention.

- **Transport Independence**: system design is decoupled from the underlying transport, meaning that the application software need not change if the application uses TCP, UDP, Shared Memory, Serial, Radio, Backplane, etc.   Secure or insecure transports, reliable or not.

- **A long list of capabilities** -- time-based filtering, persistence, liveliness, security, reliability, redundancy, batching, type extensibility, and many more capabilities are part of the open/published standard of DDS, from which more than 12 implementations have been created.

Systems based on DDS do well by having a defined set of data types, from which many applications can be created and will be
assured of interoperability by using common data type definitions.   This approach has been very successful in the ROS
(Robot Operating System) ecosystem, which uses a common set of data types and a data-centric communications framework (DDS)
to ensure interoperability between independently-created applications.

This is why it's so important when expressing the VSS in IDL through a stable set of data type definitions, that they represent
the most common usage patterns (groupings) for those signals.

(Looking forward to a lively discussion :) 