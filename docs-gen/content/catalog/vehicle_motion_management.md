---
title: "Vehicle Motion Management"
date: 2019-08-04T12:46:30+02:00
weight: 7
---

## Introduction

In modern vehicles multiple electronic controlled systems are interacting to realize the overall vehicle motion in all physical directions.
Typically, the driver gives input e.g. using the steering wheel and the accelerator and brake pedals, but additional vehicle functions may have also requests towards the motion actuators.
One example is that a traction control system may want to limit the performance due to slippery road conditions or that the emergency braking system requests braking.

A number of signals have been added to VSS related to powertrain (eAxle), steering, suspension and braking.
These signals may be used to define actuator interfaces to support a highly flexible functional deployment on different electronic control units.
Vehicle motion functions like driver brake request, cooperative regenerative braking and traction control system may request target values for longitudinal control on vehicle, axle and wheel level.
Therefore, generic interface signals for the braking systems are introduced which support an arbitration of the requested target values by minimum and maximum values.
The signal definitions for powertrain and steering are based on state-of-the art interfaces which are widely used in the automotive industry.
VSS does not specify the implementation of the interface signals and the arbitration cascade, but possible examples are given below.


## Definitions and Assumptions

If nothing else is specified, the following definitions and assumptions apply


* The specified data types are chosen based on state-of-the art interfaces for vehicle internal communication between chassis ECUs.
  All datatypes int/uint may represent decimal numbers, therefore additional computational methods could be specified in upcoming VSS releases.

* Main guiding units for vehicle motion brake control:
  * Vehicle level: Force requests
  * Axle level: Torque requests
  * Wheel level: Torque requests, omega limits (wheel-spin velocity according to ISO 8855)

  Brake forces on vehicle level are defined by the sum of all wheel forces that control the vehicle along the driving path.
  Brake torques on axle level are defined as the sum of torques on all wheels on that axle.
  Brake torques and omega limits on wheel level are defined for each individual wheel of the vehicle.

* Signal orientation brake system:
  Requests are positive in desired path direction of the vehicle.
  The desired path direction is defined by the intended driving selection (P,R,D,N).
  This means that a positive value indicates acceleration, a negative value deceleration with respect to the intended driving selection.
* Omega limits for brake system defined as relative to actual driving direction. This means that omega is never negative.
* Torque and Force distribution signals (between front/rear axle or left/right wheel) are based on the assumption that all wheels/axles exercise torque in the same direction, i.e. a single axle/wheel cannot fulfil more than 100% of the total request.

* Signal orientation steering system:
  Requests are defined according to ISO 8855.
  For steering related signals, a positive request on the front axle unless otherwise stated yields to steer the vehicle to the left.

* Signal orientation eAxle system:
  Requests are defined according to ISO 8855.
  This means that a positive torque yields to a force in vehicle forward direction and a negative torque yields to a force in backward direction.
  Omega limits for eAxle system defined according. Positive sign for rotation in forward direction, negative sign for rotation in backward direction.
  So the sign of current omega of a eAxle indicated the current driving direction.

* Signal orientation suspension system:
  Requests are defined according to ISO 8855.
  This means that a positive damping force is pointing upwards and a negative force is pointing downwards.
  A positive roll torque indicates a torque that tends to depress the right-hand side of the vehicle and lift the left-hand side.

* All signals are defined in an automotive safety context, i.e. ISO 26262 has to be considered while using specified signals in vehicle applications.

-----------------------

## Sensors vs. Actuators

The type `actuator` is selected to define that the signal may be used as a "request" by vehicle systems/services towards the actuator.
The type `sensor` is selected for signals that are processed by the actuator and may be used as actuator feedback towards the requesting vehicle systems/services.

## Braking System
The defined braking signals are the main signals for interacting between vehicle motion features and the braking system including the arbitration of longitudinal vehicle requests.
The interface signals are specified on vehicle-, axle- and wheel-level and the arbitration concept supports a flexible integration of vehicle motion features on different ECUs.
The arbitration of multiple vehicle motion features can result in a sophisticated arbitration logic to ensure the vehicle stability and driver safety, which is not part of VSS signal catalogue.
However, the specified vehicle signals shall support different arbitration logics.
The following section shows some hypothetical examples for arbitration.

### Example 1 - vehicle force requests (`Vehicle.MotionManagement.Brake.VehicleForceMaximum`)
Driver request via brake pedal -2000N.
Advanced driving assistance system for automated emergency brake has a request of -3000N.
As a result, a vehicle force of -3000N would be applied, to ensure maximum deceleration.

## Example 2 distribution request (`Vehicle.MotionManagement.Brake.VehicleForceDistributionFrontMinimum`/ `Maximum`)

Vehicle force request of -3000N of example 1.

A vehicle energy function requests a AxlePercentRangeDistributionFrontMaximum of 100% to be most energy efficient.
The vehicle stability function could limit this distribution of 20% < x < 80% due to the current driving situation.
As a result, only 80% axle distribution would be arbitrated, e.g. -600N force (braking) on rear axle and -2400N force (braking) on front axle.


## Powertrain System (Electrical Axle)

A vehicle may have an arbitrary number of electrical axles. Rotational speed and torque for an electrical axle refer to the axle coming out of the electrical axle unit.
There may be a transmission/gearbox between the electrical axle and the actual wheels served by the electrical axle.

There are two operation modes of an eAxle: torque control or speed control.

### Torque Control
A torque request (e.g. 50Nm) is realized by the eAxle. In addition, limit for the rotational speed can be defined, e.g. -5000 rpm ... +5000 rpm. These limits are useful to avoid too high wheelspin when the vehicle is on a slippery road. This mode is used most of the time, when the eAxle is active.

### Speed Control
A rotational speed request (e.g., 1000rpm) is realized by the eAxle. This mode is useful for low speed till standstill, because so the vehicle can be controlled easier to a standstill, especially on a rough road.

## Steering System

The defined steering signals are the main signals for interacting between vehicle motion features and the steering system on the front axle and are widely used in automotive industry.
These signals are specified in a generic way to support various steering systems like electric power steering as well as Steer-by-Wire. Therefore, not all signals must necessarily be available/applicable.
The signal specification supports requests on steering wheel (torque and angle) and the steering rack position which is linked to the steered wheels of the vehicle.
As an alternative to steering rack position it is possible to use steer angle (single track model).
The signal requests are further divided in "offset" and "target" signals, where an offset value is used additive to the functionality of the steering system and a "target" value is used as absolute external set-point for steering actuation.
The different requests are controlled by dedicated "mode" signals for enabling and disabling the steering requests.

Examples: Driving in a left curve and applying external requests to steering system.
Based on the stationary driving without external request (config 1) the principle effects of the different steering interface signals are explained for each interface signal exlusively (config 2...6).
Depending on the concrete use case a combination of parallel requested interface signals is applicable.

Config                                                                   | Current.SteeringWheelTorque (Torque Applied by Driver) | Current.SteeringWheelAngle  | Current.RackPositionFrontAxle  | Result/Comment
-------------------------------------------------------------------------|--------------------------------------------------------|-----------------------------|--------------------------------|----
`1`: Regular turn - No external request                                  | 3 Nm                                                   | 20 degree                   | 4 mm                           | "Steering support" (e.g. power steering) require driver to apply 3 Nm to continue turning with same radius.
`2`. Lane Assist Intervention - `SteeringWheelTorqueOffsetTarget = 2 Nm` | 5 Nm*                                                  | 20 degree                   | 4 mm                           | Driver torque needs to be increased to continue turning with same radius
`3`. Torque Target Changed - `SteeringWheelTorqueTarget = 2 Nm`          | 2 Nm*                                                  | 20 degree                   | 4 mm                           | Required driver torque set to 2 Nm (e.g. external steering feel for steer by wire), offset ignored.
`4`. Autonomuos Driving - `SteeringWheelAngleTarget = 0 deg`             | ---**                                                  | 0 degree                    | 4 mm                           | Steering wheel set to 0 deg (e.g. automated driving with steer by wire and fixed steering wheel)
`5`. Stability intervention - `RackPositionOffsetFrontAxleTarget = 3 mm` | 3 Nm                                                   | 20 degree                   | 7 mm                           | Rack position increased by 3mm (e.g. vehicle stability intervention with steer by wire)
`6`. Autonomuous Driving - `RackPositionFrontAxleTarget = 3 mm`          | ---**                                                  | 0 degree                    | 3 mm                           | Rack position set to 3 mm (e.g. automated driving), offset ignored

`*` Assumption is that driver is holding the steering wheel at the same position as without external request

`**` Steering wheel torque depending on driver input. Target request may be ignored if driver is applying torque (driver override).
