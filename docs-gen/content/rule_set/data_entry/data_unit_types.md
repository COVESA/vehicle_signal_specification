---
title: "Data Unit Types"
date: 2019-08-04T12:36:12+02:00
weight: 2
---
A signal can optionally specify a unit of measurement from the following set.
This list composed with definition according to International Units (SI) and few automotive specific units: [Specification](https://www.iso.org/standard/30669.html), [Wikipedia](https://en.wikipedia.org/wiki/International_System_of_Units)


Unit type     | Domain                          | Description
:-------------|:--------------------------------|:-------------
mm            | Distance                        | Distance measured in millimeters
cm            | Distance                        | Distance measured in centimeters
m             | Distance                        | Distance measured in meters
km            | Distance                        | Distance measured in kilometers
inch          | Distance                        | Distance measured in inches
km/h          | Speed                           | Speed measured in kilometers per hours
m/s           | Speed                           | Speed measured in meters per second
m/s^2         | Acceleration                    | Acceleration measured in meters per second squared
cm/s^2        | Acceleration                    | Acceleration measured in centimeters per second squared
ml            | Volume                          | Volume measured in milliliters
l             | Volume                          | Volume measured in liters
cm^3          | Volume                          | Volume measured in cubic centimeters
celsius       | Temperature                     | Temperature measured in degree celsius
degrees       | Angle                           | Angle measured in degrees
degrees/s     | Angular Speed                   | Angular speed measured in degrees per second
W             | Power                           | Power measured in watts
kW            | Power                           | Power measured in kilowatts
PS            | Power                           | Power measured in horsepower
kWh           | Energy Consumption              | Energy consumption measured in kilowatt hours
g             | Weight                          | Mass measured in grams
kg            | Weight                          | Mass measured in kilograms
lbs           | Weight                          | Mass measured in pounds
V             | Electric Potential              | Electric potential measured in volts
A             | Electric Current                | Electric current measured in amperes
Ah            | Electric Charge                 | Electric charge measured in ampere hours
ms            | Time                            | Time measured in milliseconds
s             | Time                            | Time measured in seconds
min           | Time                            | Time measured in minutes
h             | Time                            | Time measured in hours
day           | Time                            | Time measured in days
weeks         | Time                            | Time measured in weeks
months        | Time                            | Time measured in months
years         | Time                            | Time measured in years
UNIX Timestamp| Time                            | Unix time is a system for describing a point in time. It is the number of seconds that have elapsed since the Unix epoch, excluding leap seconds.
mbar          | Pressure                        | Pressure measured in millibars
Pa            | Pressure                        | Pressure measured in pascal
kPa           | Pressure                        | Pressure measured in kilopascal
stars         | Rating                          | Rating measured in stars
g/s           | Mass per time                   | Mass per time measured in grams per second
g/km          | Mass per distance               | Mass per distance measured in grams per kilometers
kWh/100km     | Energy Consumption per distance | Energy consumption per distance measured in kilowatt hours per 100 kilometers
ml/100km      | Volume per distance             | Volume per distance measured in milliliters per 100 kilometers
l/100km       | Volume per distance             | Volume per distance measured in liters per 100 kilometers
l/h           | Flow                            | Flow measured in liters per hour
mpg           | Distance per Volume             | Distance per volume measured in miles per gallon
N             | Force                           | Force measured in newton
Nm            | Torque                          | Torque measured in newton meters
rpm           | Rotational Speed                | Rotational speed measured in revolutions per minute
Hz            | Frequency                       | Frequency measured in hertz
ratio         | Relation                        | Relation measured as ratio
percent       | Relation                        | Relation measured in percent
... | ... | ...

VSS tooling use the list specified in [config.yaml](https://github.com/COVESA/vss-tools/blob/master/vspec/config.yaml) to validate that only supported types are used in the signal specification.
