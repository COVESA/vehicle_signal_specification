#
# Makefile to generate specifications
#

.PHONY: clean all travis_targets json franca yaml csv ddsidl tests binary protobuf ttl graphql ocf c install

all: clean json franca yaml csv ddsidl binary tests protobuf graphql

# All mandatory targets that shall be built and pass on each pull request for
# vehicle-signal-specification or vss-tools
travis_targets: clean json franca yaml binary csv graphql ddsidl tests tar


# Additional targets that shall be built by travis, but where it is not mandatory
# that the builds shall pass.
# This is typically intended for less maintainted tools that are allowed to break
# from time to time
# Can be run from e.g. travis with "make -k travis_optional || true" to continue
# even if errors occur and not do not halt travis build if errors occur
travis_optional: clean c ocf protobuf ttl

DESTDIR?=/usr/local
TOOLSDIR?=./vss-tools

json:
	${TOOLSDIR}/vspec2json.py -I ./spec ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).json

franca:
	${TOOLSDIR}/vspec2franca.py -v $$(cat VERSION)  -I ./spec ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).fidl

yaml:
	${TOOLSDIR}/vspec2yaml.py -I ./spec ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).yaml

csv:
	${TOOLSDIR}/vspec2csv.py -I ./spec ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).csv

ddsidl:
	${TOOLSDIR}/vspec2ddsidl.py -I ./spec ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).idl

tests:
	PYTHONPATH=${TOOLSDIR} pytest

binary:
	gcc -shared -o ${TOOLSDIR}/binary/binarytool.so -fPIC ${TOOLSDIR}/binary/binarytool.c
	${TOOLSDIR}/vspec2binary.py ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).binary

protobuf:
	${TOOLSDIR}/contrib/vspec2protobuf.py  -I ./spec ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).proto

graphql:
	${TOOLSDIR}/vspec2graphql.py -I ./spec ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).graphql.ts

ocf:
	${TOOLSDIR}/contrib/ocf/vspec2ocf.py -I ./spec ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).ocf.json

ttl:
	${TOOLSDIR}/contrib/vspec2ttl/vspec2ttl.py -I ./spec ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).ttl

c:
	(cd ${TOOLSDIR}/contrib/vspec2c/; make )
	PYTHONPATH=${TOOLSDIR} ${TOOLSDIR}/contrib/vspec2c.py -I ./spec ./spec/VehicleSignalSpecification.vspec vss_rel_$$(cat VERSION).h vss_rel_$$(cat VERSION)_macro.h

# Include all offically supported outputs (i.e. those created by travis_targets)
# Exception is binary as it might be target specific and library anyway needs to be rebuilt
tar:
	tar -czvf vss_rel_$$(cat VERSION).tar.gz vss_rel_$$(cat VERSION).json vss_rel_$$(cat VERSION).fidl vss_rel_$$(cat VERSION).yaml \
	vss_rel_$$(cat VERSION).csv vss_rel_$$(cat VERSION).graphql.ts vss_rel_$$(cat VERSION).idl

clean:
	rm -f vss_rel_*
	(cd ${TOOLSDIR}/contrib/vspec2c/; make clean)

install:
	git submodule init
	git submodule update
	(cd ${TOOLSDIR}/; python3 setup.py install --install-scripts=${DESTDIR}/bin)
	$(MAKE) DESTDIR=${DESTDIR} -C ${TOOLSDIR}/vspec2c install
	install -d ${DESTDIR}/share/vss
	(cd spec; cp -r * ${DESTDIR}/share/vss)
