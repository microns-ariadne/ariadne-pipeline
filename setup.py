#!/usr/bin/env python
import os
from setuptools import setup, find_packages


VERSION = 0.1


README = open('README.md').read()


setup(
    name='ariadne-pipeline',
    version=VERSION,
    author='Daniel Kelleher',
    author_email='dkelleher@g.harvard.edu',
    url = 'https://github.com/microns-ariadne/ariadne-pipeline',
    description='Run, and manage machine learning pipelines.',
    long_description=README,
    install_requires=[
        'h5py>=2.6.0',
        'nose>=1.3.7',
        'luigi>=2.1.1',
        'cliff>=2.0.0',
        'requests>=2.10.0'
    ],
    packages=['ariadne', 'plugins', 'examples'],
    entry_points={
        'console_scripts': [
            'ariadne = ariadne.cli:main'
        ],
        'ariadne.clisub.base': [
            'dataset fetch = ariadne.dataset:FetchCommand',
        ]
    },
    zip_safe=False
)
