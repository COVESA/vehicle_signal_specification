#
# Makefile to generate specifications
#

.PHONY: clean all mandatory_targets json franca yaml csv ddsidl tests binary protobuf ttl graphql ocf c overlays id jsonschema

all: clean mandatory_targets optional_targets

# All mandatory targets that shall be built and pass on each pull request for
# vehicle-signal-specification or vss-tools
mandatory_targets: clean json json-noexpand franca yaml binary csv graphql ddsidl id jsonschema apigear samm overlays

# Additional targets that shall be built by travis, but where it is not mandatory
# that the builds shall pass.
# This is typically intended for less maintainted tools that are allowed to break
# from time to time
# Can be run from e.g. travis with "make -k optional_targets || true" to continue
# even if errors occur and not do not halt travis build if errors occur
optional_targets: clean protobuf ttl

TOOLSDIR?=./vss-tools
VSS_VERSION ?= 0.0
COMMON_ARGS=-u ./spec/units.yaml --strict
COMMON_VSPEC_ARG=-s ./spec/VehicleSignalSpecification.vspec

json:
	vspec export json ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.json

json-noexpand:
	vspec export json ${COMMON_ARGS} --no-expand ${COMMON_VSPEC_ARG} -o vss_noexpand.json

jsonschema:
	vspec export jsonschema ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.jsonschema

franca:
	vspec export franca --franca-vss-version $(VSS_VERSION) ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.fidl

yaml:
	vspec export yaml ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.yaml

csv:
	vspec export csv ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.csv

ddsidl:
	vspec export ddsidl ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.idl

# Verifies that supported overlay combinations are syntactically correct.
overlays:
	vspec export json ${COMMON_ARGS} -l overlays/profiles/motorbike.vspec ${COMMON_VSPEC_ARG} -o vss_motorbike.json
	vspec export json ${COMMON_ARGS} -l overlays/extensions/dual_wiper_systems.vspec ${COMMON_VSPEC_ARG} -o vss_dualwiper.json
	vspec export json ${COMMON_ARGS} -l overlays/extensions/OBD.vspec ${COMMON_VSPEC_ARG} -o vss_obd.json

binary:
	vspec export binary ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.binary

protobuf:
	vspec export protobuf ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.proto

graphql:
	vspec export graphql ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.graphql.ts

apigear:
	vspec export apigear ${COMMON_ARGS} ${COMMON_VSPEC_ARG} --output-dir apigear
	cd apigear && tar -czvf ../vss_apigear.tar.gz * && cd ..

samm:
	vspec export samm ${COMMON_ARGS} ${COMMON_VSPEC_ARG} --target-folder samm
	cd samm && tar -czvf ../vss_samm.tar.gz * && cd ..

# vspec2ttl does not use common generator framework
ttl:
	${TOOLSDIR}/contrib/vspec2ttl/vspec2ttl.py -u ./spec/units.yaml ./spec/VehicleSignalSpecification.vspec vss.ttl

id:
	vspec export id ${COMMON_ARGS} ${COMMON_VSPEC_ARG} -o vss.vspec

clean:
	rm -f vss.*
	rm -rf apigear
	rm -rf samm
