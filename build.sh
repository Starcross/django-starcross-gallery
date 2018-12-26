#!/bin/bash
shopt -s extglob
rm -rf django-starcross-gallery
mkdir django-starcross-gallery
mkdir django-starcross-gallery/gallery
cp -r !(LICENSE|MANIFEST.in|README.rst|setup.py|django-starcross-gallery|build.sh|migrations) django-starcross-gallery/gallery
cp LICENSE MANIFEST.in README.rst setup.py django-starcross-gallery
pushd django-starcross-gallery
python setup.py sdist
popd


