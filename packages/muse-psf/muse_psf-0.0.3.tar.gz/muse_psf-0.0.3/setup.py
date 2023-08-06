#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 19:47:38 2022

@author: vegam
"""

from setuptools import setup, find_packages
import codecs
import os
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
VERSION = '0.0.3'
DESCRIPTION = 'muse_psf'
# Setting up
setup(
    name="muse_psf",
    version=VERSION,
    author="m-vegap (Macarena Vega)",
    author_email="<m.vega.pallauta@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['numpy', 'astropy', 'photutils'],
    url="https://github.com/m-vegap/muse-psf",
    keywords='python adaptative optics muse psf',
    license='MIT',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
