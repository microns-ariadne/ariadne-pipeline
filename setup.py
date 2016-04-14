#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" distribute- and pip-enabled setup.py for ariadne-pipeline """

#from distribute_setup import use_setuptools
#use_setuptools()
from setuptools import setup, Extension, find_packages
import os
import sys

plugins=os.listdir("plugins/")
newpllist=[]

for p in plugins:
    newpllist.append("plugins/%s" % p)

setup(
    name='ariadne-pipeline',
    version='1.0a12',
    description="Run, and manage machine learning pipelines.",
    scripts=['scripts/ariadne', 'ariadne/ariadne_cli.py', 'ariadne/shell2pipe.py', 'scripts/ariadne-download.sh'],
    include_package_data=True,
    install_requires=['h5py', 'nose', 'luigi'],
    packages=['ariadne', 'plugins', 'examples'],#find_packages(exclude=['tests', 'scripts', 'bin', 'plugins']),
    #data_files=[('plugins', )], # Allow plugins to be copied verbatim.
    package_data={"plugins":["*.list"]},
    )
