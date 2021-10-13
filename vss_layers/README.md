# VSS-Layers

VSS layers is an extension mechanism that has been implicitly included since
the VSS development started, and now more formally defined.

Even before the concept had a name it was in practice implemented in the
initial tools because they behaved like layers in the following ways:

1. Overriding definitions was possible with subsequent re-definition of
   the same signal

2. It was possible to add custom metadata fields to each signal, in
   addition to the VSS "core" model metadata ("name", "type", "datatype",
   "description", and in recent editions "instances", "deprecation" etc.)

Later on, tools were written to warn about unknown metadata as a quality
measure, but this needs to be adjusted when layers are used.

There is one main way to add a metadata relationship in the plain VSS
(meta)model.  In the VSSo (ontology) environment there may also be additional
ways.


Example how to list new metadata below a signal definition:

VSS core model metadata:
```
Motor.CoolantTemperature:
  datatype: int16
  type: sensor
  unit: celsius
  description: Motor coolant temperature (if applicable).
```

### Removal of nodes

Various ideas:

Removal example, using empty value = removal
```
Motor.CoolantTemperature:
  datatype: int16
  type:              <- removes "type:" entirely (*if* we allow type to be removed)
  unit: celsius
  description: Motor coolant temperature (if applicable).
```

Removal example, using no meta-data = remove signal
```
Motor.CoolantTemperature:  <- removed because meta-data is empty

Vehicle.Powertrain.Transmission.Speed:
  datatype: int32          <- modified
```

Removal example, requires all signals to be named in "deployment file" otherwise they are not included
(in a code generator for example):

"deployment file"
```
Motor.CoolantTemperature:   <- signal mentioned, therefore included
   deployment_stuff: foo
```

### Tool invocation

Example with flags to define if it's a (m)odel or (R)emoval file:
```
 $ mytool -m vss_rel_2.yaml -m privacy_layer.yaml -m deployment_info.yaml -R stuff_to_remove.yaml
```
... in this case nodes listed in stuff_to_remove.yaml gets removed.


Example with flags to define if it's a (m)odel or (I)nclusion file:
```
 $ mytool -m vss_rel_2.yaml -m privacy_layer.yaml -m deployment_info.yaml -I deployment_whitelist.yaml
```
... in this case any node NOT listed in deployment_whitelist.yaml gets removed (not used in output).

Proposal: "Allow" tools to include equivalent of -R and -I flags, one or the
other or both, depending on need.

Also support a manifest file instead of listing on command line
```
 $ mytool -f filelist.txt
```

filelist.txt example 1:
```
 vss_rel_2.2
 +vss_privacy_info
 +deployment
 -removed_signals
```

filelist.txt example 2:
```
 basemodel: vss_rel_2.2
 layer: vss_privacy_info
 modification: ...
 deployment: mydepl.yaml
```

filelist.txt example 3:
```
 model: vss_rel_2.2
 model: vss_privacy_info
 model: ...
 Removal: mydepl.yaml
```


TODO:
- Define how to modify instances


Example of layered additional metadata:
```
Motor.CoolantTemperature:
  my_unique_concept: true
```

### A note about signal names and paths

The VSS is defined by a hierarchy of sub-trees each defined in their own file.

An example file (ElectricMotor.vspec) may include:

```
Motor.CoolantTemperature
  ...
  ...
```

but since this information is in the file ElectricMotor.vspec, and
that file was included at the location of Vehicle.Powertrain.ElectricMotor,
the above shortened definition actually spells out the following full-path
signal:

`Vehicle.Powertrain.ElectricMotor.Motor.CoolantTemperature`


This principle for file-inclusions and namespacing applies to VSS-layers in
the same way as the core VSS.  For full details, refer to the VSS
documentation. Note however, that later examples in this text will use the
full path for clarity.  E.g.: `Vehicle.Chassis.Wheel.Brake.Fluidlevel`

## Usage of VSS-layers

VSS-layers is a fully generic extension mechanism that is likely to find new
uses over time, but some of the primary drivers are:

1. The general separation of a "deployment model" that is not included in the core definition.
1. Defining supplementary layers that deal with, for example, data classification.
1. Ability for companies to tie VSS into existing software and processes that needs additional concepts or information

Some of these usages may lead to agreed-upon layers used by the whole industry, a.k.a. standard layers.
Others will be system, product, or company specific.

### Deployment model

This concept, also provided by Franca IDL, is very powerful as it
ensures that the basic interface definition (in this case the VSS signals) is
not encumbered by details that are unique to a particular usage of the
information.

A Deployment Model keeps the information necessary to realize the
described interface in a particular environment, platform, or even programming
language.  Anything that is not related to the interface (data) description
itself, but rather to how it is used, should be separated into a deployment
model outside of the main definition file.

This makes the data or interface definition more reusable because the same
definition can be used in many different environments and situations.

As an example, in a local request, the name of the data or function might be
enough to address it.  When the same definition is to be used in a distributed
system, the data access or function invocation may need some kind of
address of the location to find this particular item.  In some environments,
this could be a logical Node name it belongs to, or an IP-address in
another environment, or a numeric service ID in another.  A particular
protocol may offer data requests to be synchronous or asynchronous, or cached
or on-demand.  While that is a feature and is likely part of the request sent
via the protocol, it may be that some data items can support only one or the
other, and that must then be defined for each data item.

Whatever they may be, such details are deployment-specific and should be
layered on top of the core model and catalog, not included in it.

### Data classification

An example of information that would be applicable only in some situations is
to classify data into privacy sensitivity categories. Other classification
reasons can be envisioned as well.

Noteworthy for this example, and likely many others:

1. What falls into each privacy category differs depending on country
 jurisdiction, and perhaps sometimes on the usage situation.  The way data is
 classified might differ between car brands.
1. The same vehicle model may be sold in different markets and the same
   product would then need different definitions on the individual level.

The nature of local privacy laws (and likely many other examples) shows that
such information cannot be defined as part of the common model or catalog --
it simply differs too often between usage situations.  Sometimes it is
required to view the system's data model with different layer configurations
even within a single implementation.  Therefore, a layered approach is needed
in the creation of a standard data model and data catalog.

The fact that this may differ even on instances of vehicles of the same make
shows that the ability to add/remove layers dynamically might be needed in the
technology stack implementation.  Another consideration is for layers to be
individually updated during software updates.

### Access control

A frequent augmentation of the data model information is definition of access
permission rules.  These boil down to specific signals that a specific actor
is allowed or not allowed to access.  Once again, this differs depending on
the situation and should be defined as a separate layer.

## General definition of VSS-layers

The layer concept definition should impose very little restrictions.
Conventions and particular tools may introduce their own restrictions
for certain usage, at a later time.

The layer concept itself is able to do all of the following:

1. Modify existing metadata and ultimately redefine any signal (i.e. change
   its metadata) compared to a previous definition for example the definition
   in the standard catalog.
1. Add new signals. It can be done in the private/ branch as recommended but the
   mechanism allows adding them anywhere.
1. Add new metadata, or relationships to new concepts for the purpose of
   creating deployment-models, bindings to existing technology, classification
   and many other things.
1. Remove signals from the final data model (SYNTAX TO BE DEFINED)

VSS-layers can also define new concepts as described in the following
scenarios:

## Tool support

VSS Layer general concept shall be supported in vss-tools, wherever it is
applicable.

VSS processing tools shall generally support any number of input layers of the
supported type, and if nothing else is documented then tools shall process the
layers in the given order (later layers redefine or override earlier layers).
Tools may optionally provide information (warning or other logs) when
information is redefined.


