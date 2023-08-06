#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.core import setup


def readme():
    with open("README-pypi.rst") as f:
        return f.read()


setup(
    name="minimalKB",
    version="9.9.9",
    license="BSD",
    description="A RDFlib-backed minimalistic knowledge based for robotic application",
    long_description=readme(),
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
    ],
    author="Séverin Lemaignan",
    author_email="severin.lemaignan@pal-robotics.com",
    url="https://github.com/severin-lemaignan/minimalkb",
    scripts=["bin/minimalkb"],
)
