#!/usr/bin/env zsh
set -e
MODULE=km3astro

if [ $# -eq 0 ]
  then
    echo "No version number supplied"
    exit 1
fi

export VERSION=$1

git checkout master
git pull

vim CHANGELOG.rst
git add CHANGELOG.rst
git commit -m "Bump changelog"

echo "__version__ = '${VERSION}'" > $MODULE/__init__.py
git add $MODULE/__init__.py

git commit -m "Bump version number"

git tag -a $VERSION

rm -rf dist/*
python setup.py sdist
twine upload dist/*

git push
git push --tags
