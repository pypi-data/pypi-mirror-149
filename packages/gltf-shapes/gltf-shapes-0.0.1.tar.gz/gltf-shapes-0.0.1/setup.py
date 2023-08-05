#!/usr/bin/env python

import setuptools
import os

setuptools.setup(
    name='gltf-shapes',
    version='0.0.1',
    description='Transform numpy arrays and pandas dataframes to 3d exports',
    long_description="""Transform numpy arrays and pandas dataframes to 3d exports using trimesh""",
    long_description_content_type="text/markdown",
    author='Egil Moeller',
    author_email='em@emeraldgeo.no',
    url='https://github.com/emerald-geomodelling/gltf-shapes',
    packages=setuptools.find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "trimesh"
    ],
)
