#!/bin/sh
set -v
ID=$RANDOM
# TODO "Nice!' name" fails in npm/bower
./generate.py --charge test-`echo $ID`.ch "Nice name"
cd build/test_`echo $ID`_ch
yes | fab local.setup
fab check.test
