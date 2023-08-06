#!/bin/bash

# clirail: command line interface to iRail
# Copyright © 2019 Midgard
# License: GPLv3+

cd $(dirname "$0")/..

rm -rf ./build/ ./clirail.egg-info/ ./dist/ ./__pycache__/ ./clirail/__pycache__/
