#!/bin/bash -e

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

version=$(python -c 'import eziface; eziface.version()')

echo "Deploying version $version"

# git related commands
git tag -s -m "Version $version" v$version
python2 setup.py sdist

git push origin master # only push master branch
git push --tags origin

rm -rf build/ dist/

