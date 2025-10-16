#
# Makefile to generate specifications
#

.PHONY: clean all mandatory_targets json franca yaml csv ddsidl tests binary protobuf ttl graphql ocf c overlays id jsonschema

all: clean mandatory_targets optional_targets

# All mandatory targets that shall be built and pass on each pull request for
# vehicle-signal-specification or vss-tools
mandatory_targets: clean apigear binary csv ddsidl franca go graphql id json json-noexpand jsonschema overlays plantuml samm yaml

# Additional targets that shall be built by travis, but where it is not mandatory
# that the builds shall pass.
# This is typically intended for less maintainted tools that are allowed to break
# from time to time
# Can be run from e.g. travis with "make -k optional_targets || true" to continue
# even if errors occur and not do not halt travis build if errors occur
optional_targets: clean protobuf

TOOLSDIR?=./vss-tools
VSS_VERSION ?= 0.0
COMMON_ARGS=-u ./spec/units.yaml --strict
COMMON_VSPEC_ARG=-s ./spec/VehicleSignalSpecification.vspec


# Exporters

apigear:
	vspec export apigear ${COMMON_ARGS} ${COMMON_VSPEC_ARG} --output-dir apigear
	cd apigear && tar -czvf ../vss_apigear.tar.gz * && cd ..

binary:
	vspec export binary ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.binary

csv:
	vspec export csv ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.csv

ddsidl:
	vspec export ddsidl ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.idl

franca:
	vspec export franca --franca-vss-version $(VSS_VERSION) ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.fidl

go:
	vspec export go ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.go

graphql:
	vspec export graphql ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.graphql.ts

id:
	vspec export id ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.vspec

json:
	vspec export json ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.json

json-noexpand:
	vspec export json ${COMMON_ARGS} --no-expand ${COMMON_VSPEC_ARG} -o vss_noexpand.json

jsonschema:
	vspec export jsonschema ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.jsonschema

plantuml:
	vspec export plantuml ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.puml

protobuf:
	vspec export protobuf ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.proto

samm:
	vspec export samm ${COMMON_ARGS} ${COMMON_VSPEC_ARG} --target-folder samm
	cd samm && tar -czvf ../vss_samm.tar.gz * && cd ..

yaml:
	vspec export yaml ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.yaml

# Other

# Verifies that supported overlay combinations are syntactically correct.
overlays:
	vspec export json ${COMMON_ARGS} -l overlays/profiles/motorbike.vspec ${COMMON_VSPEC_ARG} -o vss_motorbike.json
	vspec export json ${COMMON_ARGS} -l overlays/extensions/dual_wiper_systems.vspec ${COMMON_VSPEC_ARG} -o vss_dualwiper.json
	vspec export json ${COMMON_ARGS} -l overlays/extensions/OBD.vspec ${COMMON_VSPEC_ARG} -o vss_obd.json

clean:
	rm -f vss.*
	rm -rf apigear
	rm -rf samm
