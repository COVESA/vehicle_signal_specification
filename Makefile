.PHONY: clean all preprocessing test

all: preprocessing yaml

TOOLSDIR ?= ./vss-tools
VSS_VERSION ?= 0.0
COMMON_ARGS = -u ./spec/units.yaml --strict -e metadata
COMMON_VSPEC_ARG = -s ./spec/VehicleSignalSpecification.vspec
BUILD_SCRIPT := tools/gomplate/src/generate.py
TEST_DIR := tools/gomplate/test

VERBOSE ?= 0
ifeq ($(VERBOSE),1)
	VFLAG = -v
else
	VFLAG =
endif

ifeq ($(OS),Windows_NT)
	PYTHON := python
	SHELL := powershell.exe
    	SHELLFLAGS := -NoProfile -Command
        RM_DIR = if (Test-Path "$(1)") { Remove-Item -Recurse -Force "$(1)" }
        RM_DIR_CONTENT = if (Test-Path "$(1)") { Remove-Item -Path "$(1)/*" -Recurse -Force }
else
	PYTHON := $(shell command -v python3 2>/dev/null || command -v python 2>/dev/null)
        RM_DIR = rm -rf "$(1)"
        RM_DIR_CONTENT = rm -rf "$(1)"/*
endif

preprocessing:
## clean the generated output before building
	$(call RM_DIR_CONTENT,spec)
	$(PYTHON) $(BUILD_SCRIPT) $(VFLAG)

yaml:
	vspec export yaml $(COMMON_ARGS) $(COMMON_VSPEC_ARG) -o spec/vss.yaml

test:
	$(PYTHON) -m pytest $(TEST_DIR) -v

## clean : Remove generated output
clean:
	$(call RM_DIR_CONTENT,spec)
	$(call RM_DIR,.pytest_cache)
	$(call RM_DIR,.tools)
	$(call RM_DIR,tools/gomplate/src/__pycache__)
	$(call RM_DIR,tools/gomplate/test/__pycache__)
