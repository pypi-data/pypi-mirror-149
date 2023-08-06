#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 Tong LI <tongli.bioinfo@protonmail.com>
#
# Distributed under terms of the BSD-3 license.

"""

"""
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="feature-based-registration-BioinfoTongLI",
    version="2.0.1",
    description="Feature-spot-based image registration for fluorescence microscopy images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=["Vasyl Vaskivskyi", "Tong LI"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        #'Topic :: segmentation :: Microscope',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="microscope registration DAPI fluorescence microscopy slide-imaging",
    packages=find_packages(),
    python_requires=">=3.0.*",
    install_requires=["numpy", "tifffile", "opencv-contrib-python", "dask", "pandas", "scikit-learn", "scikit-image"],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={  # Optional
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    # },
    project_urls={  # Optional
       'Bug Reports': 'https://github.com/BayraktarLab/feature_reg/issues',
       # 'Say Thanks!': 'http://saythanks.io/to/example',
       'Source': 'https://github.com/BayraktarLab/feature_reg/',
    }
)
