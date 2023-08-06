#!/bin/bash

set -e

cd $(dirname "$0")/..

if [ ! -t 0 ] ; then
	echo "release.sh should be run with a terminal attached to stdin" >&2
	exit 1
fi

source venv/bin/activate
pip install twine

git status

echo -n "Previous version:  v"
prev_version="$(./setup.py --version)"
echo "$prev_version"
read -p "Enter new version: v" version

tagid=v"$version"
if [ "$version" != "$prev_version" ]; then
	sed -i 's/version=".*"/version="'"$version"'"/' setup.py
	sed -i 's/## \[Unreleased\]/&\n\n## ['"$version"'] - '"$(date --utc +%Y-%m-%d)"'/' CHANGELOG.md
	echo; echo "Inspect CHANGELOG..."
	${EDITOR:-nano} CHANGELOG.md
	git add setup.py CHANGELOG.md
	git commit -m "Bump version to $version"

	echo "Creating git tag $tagid"
	git tag -s -m "Version $version" "$tagid"
else
	echo "Version already created; building wheel and uploading"
fi

./setup.py sdist bdist_wheel

read -p "Upload to Git and PyPI? (y/N) " confirm
if [ ! "$confirm" = y ]; then "Abort"; exit 1; fi

torsocks python3 -m twine upload dist/*-${version}*
git push origin "$tagid" master
