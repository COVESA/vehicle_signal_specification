#
# Makefile to generate specifications
#

.PHONY: clean all travis_targets json franca yaml csv ddsidl tests binary protobuf ttl graphql ocf c install overlays

all: clean json franca yaml csv ddsidl binary tests protobuf graphql overlays ttl

# All mandatory targets that shall be built and pass on each pull request for
# vehicle-signal-specification or vss-tools
travis_targets: clean json franca yaml binary csv graphql ddsidl overlays tests tar


# Additional targets that shall be built by travis, but where it is not mandatory
# that the builds shall pass.
# This is typically intended for less maintainted tools that are allowed to break
# from time to time
# Can be run from e.g. travis with "make -k travis_optional || true" to continue
# even if errors occur and not do not halt travis build if errors occur
travis_optional: clean protobuf ttl

DESTDIR?=/usr/local
TOOLSDIR?=./vss-tools

json:
	${TOOLSDIR}/vspec2json.py -I ./spec --uuid -u ./spec/units.yaml ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).json

franca:
	${TOOLSDIR}/vspec2franca.py -v $$(cat VERSION)  -I ./spec --uuid -u ./spec/units.yaml ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).fidl

yaml:
	${TOOLSDIR}/vspec2yaml.py -I ./spec --uuid -u ./spec/units.yaml ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).yaml

csv:
	${TOOLSDIR}/vspec2csv.py -I ./spec --uuid -u ./spec/units.yaml ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).csv

ddsidl:
	${TOOLSDIR}/vspec2ddsidl.py -I ./spec --uuid -u ./spec/units.yaml ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).idl

# Verifies that supported overlay combinations are syntactically correct.
overlays:
	${TOOLSDIR}/vspec2json.py -I ./spec --uuid -u ./spec/units.yaml -o overlays/profiles/motorbike.vspec ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION)_motorbike.json
	${TOOLSDIR}/vspec2json.py -I ./spec --uuid -u ./spec/units.yaml -o overlays/extensions/dual_wiper_systems.vspec ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION)_dualwiper.json

tests:
	PYTHONPATH=${TOOLSDIR} pytest

binary:
	gcc -shared -o ${TOOLSDIR}/binary/binarytool.so -fPIC ${TOOLSDIR}/binary/binarytool.c
	${TOOLSDIR}/vspec2binary.py --uuid -u ./spec/units.yaml ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).binary

protobuf:
	${TOOLSDIR}/vspec2protobuf.py  -I ./spec -u ./spec/units.yaml ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).proto

graphql:
	${TOOLSDIR}/vspec2graphql.py -I ./spec --uuid -u ./spec/units.yaml ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).graphql.ts

ttl:
	${TOOLSDIR}/contrib/vspec2ttl/vspec2ttl.py -I ./spec -u ./spec/units.yaml ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).ttl

# Include all offically supported outputs (i.e. those created by travis_targets).
# Exception is binary as it might be target specific and library anyway needs to be rebuilt.
# As of today all artifacts generated for release shall include UUID if supported.
# Note: From VSS 3.1 individual files are uploaded instead of tar file, but this command kept for now anyway
tar:
	tar -czvf vss_rel_$$(cat VERSION).tar.gz vss_rel_$$(cat VERSION).json vss_rel_$$(cat VERSION).fidl vss_rel_$$(cat VERSION).yaml \
	vss_rel_$$(cat VERSION).csv vss_rel_$$(cat VERSION).graphql.ts vss_rel_$$(cat VERSION).idl

clean:
	rm -f vss_rel_*

install:
	git submodule init
	git submodule update
	(cd ${TOOLSDIR}/; python3 setup.py install --install-scripts=${DESTDIR}/bin)
	install -d ${DESTDIR}/share/vss
	(cd spec; cp -r * ${DESTDIR}/share/vss)
