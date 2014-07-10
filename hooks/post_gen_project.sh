#!/bin/sh

# Ensure files end with a newline.
# Also see https://github.com/audreyr/cookiecutter/pull/183
find . -type f -print0|xargs -0 sed -i '' -e '$a\'

git init
git add -A
git commit -m "Initial commit"
fab setup
