#!/usr/bin/env python3 

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

from os import getenv
version = "0.1"
for e in ['CI_COMMIT_REF_NAME','CI_JOB_ID']:
    v = getenv(e,False)
    if v:
        version = str(v)
    
import unittest
def test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='test_*.py')
    return test_suite

pkgs = setuptools.find_packages()

setuptools.setup(
    name="pyhepdata",
    version=version,
    author="Christian Holm Christensen",
    author_email="cholmcc@gmail.com",
    description="I/O, validation, plotting, etc. of HEPData submission",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cholmcc/hepdata",
    packages=pkgs,
    # include_package_data=True,
    license='GPLv3+',
    platforms='any',
    package_data={'hepdata.names':['data/*.yaml']},    
    test_suite='setup.test_suite',
    scripts=['examples/hepdata_plot.py'],
    install_requires=[
        'pyyaml',
        'jsonschema',
        'matplotlib',
        'hepdata_validator'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Development Status :: 4 - Beta",
    ],
)
