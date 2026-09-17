---
title: "Energy Management"
date: 2019-08-04T12:46:30+02:00
weight: 7
---


## Introduction
The VSS energy management feature conditions the battery for fast charging at the end of the trip.
Energy savings are achieved by minimizing the time when the battery is at the required temperature.

## Logic
When the feature is enabled (EnergyManagement.IsEnabled) optimized values for the battery temperature setpoint, the coolant mass flow and the heater power are downloaded into the vehicle.
The values are the result of a predictive optimization that takes the current battery state and the route into account (Vehicle.Cabin.Infotainment.Navigation).
The expected GPS position is also downloaded to detect if the vehicle is still on the route.
If a deviation in the battery temperature is detected or if the vehicle has left the expected route a new optimization is triggered (EnergyManagement.IsRecalculationRequest).
When the vehicle has reached its destination the backend is notified (Navigation.Map.IsDestinationReached).

The data downloaded into the vehicle is in table format.
One table for setpoints and one for check timestamps.
They are represented as arrays in VSS.
The size for setpoints and check timestamps may be different.
All timestamps are relative to feature activation.


### SetPoint table

Hypothetic example of setpoint table:

Index | SetpointTimestamp | SetpointBatteryTemperature |SetpointHeaterPower | SetpointCoolantMassFlow
---|----|---|---|---
0 | 0 | 17.0 | 0 | 54
1 | 120 | 17.5 | 2 | 57
2-98 |...| ... | ... | ...
99 | 12000 | 35.3 | 5 | 60 |


### Target table

Hypothetic example of target table:

Index | TargetTimestamp | TargetLatitude | TargetLongitude
---|----|---|---
0 | 0 | 55.0 | 13.0
1 | 600 | 55.5 | 13.5
2-19 |...| ... | ...
20 | 12000 | 60.0 | 14.8
