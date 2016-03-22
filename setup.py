#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" distribute- and pip-enabled setup.py for ariadne-pipeline """

#from distribute_setup import use_setuptools
#use_setuptools()
from setuptools import setup, Extension, find_packages
import os
import sys

setup(
    name='ariadne-pipeline',
    version='1.0a8',
    description="Run, and manage machine learning pipelines.",
    scripts=['ariadne/ariadne.py', 'scripts/ariadne', 'ariadne/shell2pipe.py', 'scripts/ariadne-download.sh'],
    include_package_data=True,
    install_requires=['h5py', 'nose', 'luigi'],
    packages=find_packages(exclude=['tests', 'scripts', 'bin']),
    )
