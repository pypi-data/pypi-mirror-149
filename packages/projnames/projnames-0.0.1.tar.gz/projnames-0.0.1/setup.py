#!/usr/bin/env python

import setuptools
import distutils.command.build
import distutils.command.sdist
import os

setuptools.setup(
    name='projnames',
    version='0.0.1',
    description='Projection name to/from epsg-code',
    long_description='Projection name to/from epsg-code using data from pyproj',
    long_description_content_type="text/markdown",
    author='Egil Moeller',
    author_email='em@emeraldgeo.no',
    url='https://github.com/EMeraldGeo/projnames',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'emeraldinterpret': ['*.json', "*.txt", "*/*.css", "*/*.yaml", "*/*.pvsm"]},
    entry_points={
        'console_scripts': [
            'projnames = projnames:cmd',
        ],
    },
)

