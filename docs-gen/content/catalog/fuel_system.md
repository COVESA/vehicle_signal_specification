---
title: "Fuel System Representation"
date: 2019-08-04T12:46:30+02:00
weight: 5
---

## Introduction

A vehicle may have one or more fuel tanks for combustion engines.
The fuel tanks are logically divided into fuel systems.
If two tanks typically are used independently of each other they are considered to be part of different fuel systems.
If two tanks typically are used at the same time or needs to be used in parallel they are considered belonging to the same fuel system.

Tank data include capacity and current level, but consumption metrics are present on fuel system level only, and can be presented mass-based or volume-based.

This gives three typical fuel system setups for vehicles with 1-2 fuel tanks, shown as examples below.
The signal `Vehicle.Powertrain.FuelSystemType` can be used to indicate the setup.


### Single Fuel Vehicles

One tank of one fuel source used by the engine.
* Model as one logical fuel system with one fuel source.
*	The fuel source has its own tank, level sensor, and supply path.
*	The system has a single fuel consumption metric (for engine operation)

### Dual-Fuel Heavy-Duty Vehicles (Diesel + NG)

One tank of diesel, one tank of compressed/liquefied natural gas, both delivered simultaneously to the engine. The two fuels are mixed in the engine to produce combustion.
*	Model as one logical fuel system with two fuel sources.
*	Each source has its own tank, level sensors, and supply path.
*	The system has a single combined fuel consumption metric (for engine operation) but still tracks each tank individually.

### Bi-Fuel Vehicles (Gasoline + NG)
Gasoline tank + NG tank, but only one fuel type is used at a time. Unlike dual-fuel HD engines, fuels are not mixed in the engine; vehicle switches between them (separate fuel systems and delivery)
*	Model as two independent fuel systems.
*	Each fuel source has its own tank, sensors, and supply path
*	Each fuel system has its own consumption metrics.


A good article explaining dual fuel systems in HD vehicles (https://ultimatecelldistributors.co.uk/insights/dual-fuel-technology/).

## Usage in VSS standard Catalog

The VSS standard catalog is based on the assumption that a vehicle has a single fuel system with a single tank.
The fuel in the tank is measured in liters.
The setup in the default catalog is specified by `Powertrain/Powertrain.vspec`.
It include tank specific data on the same level as the fuel system, but include two different files to simplify customization.

```
FuelSystem:
  type: branch
  description: Fuel system data.
#include VolumeFuelSystem.vspec FuelSystem
# Tank integrated by default, not added to a separate branch
#include FuelSystem/VolumeTank.vspec FuelSystem
```

Taking tank absolute level as example, this results in a single signal:

```
Vehicle.Powertrain.FuelSystem.AbsoluteLevel,sensor,float,,l
```

## Extending for more advanced use-cases.

If using VSS for a vehicle with a gas fuel system, multiple fuel systems or multiple fuel tanks it is recommended to use an overlay to customize that catalog.
An example overlay exists in [overlays/extensions/multi_fuel_system_example.vspec](https://github.com/COVESA/vehicle_signal_specification/blob/master/overlays/extensions/multi_fuel_system_example.vspec).
That overlay can be used like this:

```bash
vspec export csv -u ./spec/units.yaml --strict -l overlays/extensions/multi_fuel_system_example.vspec -I spec -s ./spec/VehicleSignalSpecification.vspec -o vss_multi_fuel.csv
```

When using an overlay it is recommended to delete the standard path and after add your customized definition into a separate path

```
Vehicle.Powertrain.FuelSystem:
  type: branch
  delete: true
```

All examples below can be found combined in the example overlay.

Alternatively if using your own fork/branch you can update [Powertrain.vspec](https://github.com/COVESA/vehicle_signal_specification/blob/master/spec/Powertrain/Powertrain.vspec) directly.

### Fuel system with weight based fuel

If you measure fuel by weight (kilograms) rather than volume you could use the overlay to delete the default branch and instead add a gas branch,
using the "mass" versions of the files reporting capacity and consumption based on kilograms rather than liters

```
Vehicle.Powertrain.FuelSystem:
  type: branch
  delete: true

Vehicle.Powertrain.GasFuelSystem:
  type: branch
  description: Fuel system data.
#include Powertrain/MassFuelSystem.vspec Vehicle.Powertrain.GasFuelSystem
# Tank integrated, not using separate branch
#include Powertrain/FuelSystem/MassTank.vspec Vehicle.Powertrain.GasFuelSystem
```

For absolute level, this results in this signal

```
Vehicle.Powertrain.GasFuelSystem.AbsoluteLevel,sensor,float,,kg
```

### Fuel system with two volume based tanks

In this case we represent the tanks on different sub-branches.
It is assumed that general consumption/economy metrics are still relevant, so the fuel system is represented by `VolumeFuelSystem.vspec`.

```
Vehicle.Powertrain.MultiFuelSystem1:
  type: branch
  description: Fuel system data.
#include Powertrain/VolumeFuelSystem.vspec Vehicle.Powertrain.MultiFuelSystem1

Vehicle.Powertrain.MultiFuelSystem1.Tank1:
  type: branch
  description: Fuel tank data.
#include Powertrain/FuelSystem/VolumeTank.vspec Vehicle.Powertrain.MultiFuelSystem1.Tank1
Vehicle.Powertrain.MultiFuelSystem1.Tank2:
  type: branch
  description: Fuel tank data.
#include Powertrain/FuelSystem/VolumeTank.vspec Vehicle.Powertrain.MultiFuelSystem1.Tank2
```

For absolute level, this results in two signals

```
Vehicle.Powertrain.MultiFuelSystem1.Tank1.AbsoluteLevel,sensor,float,,l
Vehicle.Powertrain.MultiFuelSystem1.Tank2.AbsoluteLevel,sensor,float,,l
```

### Fuel system with one volume based and one weight based tank.

In this case we represent the tanks on different sub-branches.
It is assumed that general consumption/economy metrics is not relevant, so the fuel system is represented by `FuelSystem.vspec`.

```
Vehicle.Powertrain.MultiFuelSystem2:
  type: branch
  description: Fuel system data.
#include Powertrain/FuelSystem.vspec Vehicle.Powertrain.MultiFuelSystem2
# Tank integrated, not using separate branch

Vehicle.Powertrain.MultiFuelSystem2.GasTank:
  type: branch
  description: Fuel tank data.
#include Powertrain/FuelSystem/MassTank.vspec Vehicle.Powertrain.MultiFuelSystem2.GasTank
Vehicle.Powertrain.MultiFuelSystem2.DieselTank:
  type: branch
  description: Fuel tank data.
#include Powertrain/FuelSystem/VolumeTank.vspec Vehicle.Powertrain.MultiFuelSystem2.DieselTank
```

For absolute level, this results in two signals

```
Vehicle.Powertrain.MultiFuelSystem2.GasTank.AbsoluteLevel,sensor,float,,kg
Vehicle.Powertrain.MultiFuelSystem2.DieselTank.AbsoluteLevel,sensor,float,,l
```

### Naming Recommendations

It is up to the user to decide on names on the fuel system and tank branches. The VSS project does not provide any recommendation, but the names must follow VSS branch naming rules
Some possible naming patterns include:

* Numeric suffix, e.g. `FuelSystem1`, `FuelSystem1`, `Tank1`, `Tank2`
* Logical naming, e.g. `Primary`, `Secondary`, `Diesel`, `Gas`
* Location, e.g. `Front`, `Rear, `Left`
