#!/bin/bash -e

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

version=$(python -c 'import pyiface; pyiface.version()')

echo "Deploying version $version"

# git related commands
git tag -s -m "Version $version" v$version
python2 setup.py sdist

git add .
git commit -a

git push origin master # only push master branch

rm -rf build/ dist/

