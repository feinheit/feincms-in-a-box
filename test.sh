#!/bin/sh
set -v
rm -rf build/example_com
# TODO "Nice!' name" fails in npm/bower
./generate.py --charge example.com "Nice name"
cd build/example_com
yes | fab local.setup
fab check.test
