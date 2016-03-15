#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" distribute- and pip-enabled setup.py for ariadne-pipeline """

from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup, Extension, find_packages
import os
import sys

setup(
    name='ariadne-pipeline',
    version='dev',
    scripts=['scripts/ariadne', 'scripts/ariadne-download.sh'],
    include_package_data=True,
    packages=find_packages(exclude=['tests', 'scripts']),
    )