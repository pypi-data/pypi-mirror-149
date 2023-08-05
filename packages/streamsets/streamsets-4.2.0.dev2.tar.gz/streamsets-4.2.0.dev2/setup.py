#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2021 StreamSets, Inc.

"""The setup script."""

from setuptools import setup

requirements = [
    'dpath==1.4.2',
    'inflection',
    'PyYAML',
    'requests'
]

setup(
    name='streamsets',
    version='4.2.0.dev2',
    description='A Python SDK for StreamSets',
    author='StreamSets Inc.',
    packages=['streamsets.sdk'],
    include_package_data=True,
    install_requires=requirements,
    dependency_links=['https://github.com/streamsets/dpath-python/tarball/master#egg=dpath-1.4.2'],
    python_requires='>=3',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
