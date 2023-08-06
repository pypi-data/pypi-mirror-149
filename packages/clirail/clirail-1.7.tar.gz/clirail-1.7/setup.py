#!/usr/bin/env python3

import setuptools


with open("README.md", "r") as fh:
	long_description = fh.read()


setuptools.setup(
	name="clirail",
	version="1.7",
	author="Midgard",
	author_email=None,
	description="Command line application for the iRail API",
	long_description=long_description,
	long_description_content_type="text/markdown",
	scripts=["bin/clirail"],

	url="https://framagit.org/Midgard/clirail",
	project_urls={
		"Source": "https://framagit.org/Midgard/clirail",
		"Change log": "https://framagit.org/Midgard/clirail/-/blob/master/CHANGELOG.md",
		"Bug tracker": "https://framagit.org/Midgard/clirail/-/issues",
	},

	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"License :: OSI Approved :: ISC License (ISCL)",
		"Operating System :: OS Independent",
		"Natural Language :: English",
		"Natural Language :: Dutch",
		"Environment :: Console",
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: End Users/Desktop",
		"Topic :: Utilities",
	],

	packages=setuptools.find_packages(),
	python_requires=">=3.6",
	install_requires=[
		"requests",
		"python-dateutil",
	],
)
