#!/bin/bash

# clirail: command line interface to iRail
# Copyright © 2019 Midgard
# License: GPLv3+

cd $(dirname "$0")/..

# Create virtualenv
python3 -m virtualenv venv/

# Install dependencies
venv/bin/pip install -e .
