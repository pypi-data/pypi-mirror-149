# -*- coding: utf-8 -*-
"""
Created on Sat May  8 14:37:04 2021

"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pkglogger", # Replace with your own username
    version="0.0.16.0",
    author="Avik Das",
    author_email="avik_das_2017@cba.isb.edu",
    description="This package help you to keep logs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "pkglogger"},
    packages=setuptools.find_packages(where="pkglogger"),
    python_requires=">=2.0",
)