#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.core import setup

setup(
    name="minimalKB",
    version="9.9.10",
    license="BSD",
    description="A RDFlib-backed minimalistic knowledge based for robotic application",
    long_description="""
    `minimalkb` has been superseeded by `KnowledgeCore`: https://pypi.org/project/KnowledgeCore/

Install `KnowledgeCore` instead of `minimalkb`: `pip install KnowledgeCore`""",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
    ],
    author="Séverin Lemaignan",
    author_email="severin.lemaignan@pal-robotics.com",
    url="https://github.com/severin-lemaignan/minimalkb",
    scripts=["bin/minimalkb"],
)
