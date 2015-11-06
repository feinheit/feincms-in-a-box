#!/bin/sh
set -e
set -v
rm -rf build/example_com
# TODO "Nice!' name" fails in npm/bower
./generate.py --charge --server deploy@example.tld example.com "Nice name" --python ${TRAVIS_PYTHON_VERSION:-python2}
ls . *
cd build/example_com
yes | fab local.setup
fab check.test
