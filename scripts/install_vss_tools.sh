#!/bin/sh
#
# Change this script to specify which version of vss-tools to install.
# It must be a version compatible with the VSS version.
# See https://github.com/COVESA/vss-tools for vss-tools information
#
# To be able to run the script you must have a python/pip environment
#  where pip is allowed, for instance a virtual python environment
# , see https://docs.python.org/3/library/venv.html
#
# ************ MASTER *************''
# For master (ongoing development) we typically rely on latest master of vss-tools
#
# pip install --upgrade git+https://github.com/COVESA/vss-tools@master

# Examples for other scenarios below
#
# ************ MAINTENANCE **********
# For development in maintenance branches we could either refer to a fixed version of vss-tools
# or refer to a maintenance branch of vss-tools
# pip install --upgrade git+https://github.com/COVESA/vss-tools@4.X
#
#
# ************* RELEASE CANDIDATES AND OTHER PRE-RELEASES ***************
# For VSS release candidates we want to link to specified released VSS-tools version.
# Either a released version or a pre-release, referenced with "--pre"
# See https://pypi.org/project/vss-tools/
#
pip install --upgrade --pre vss-tools==5.0
#
#
# *********************** RELEASES ***************************
# For releases we should link to specific released pypi version.
#
# pip install --upgrade vss-tools==5.1
