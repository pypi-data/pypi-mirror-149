#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os 
from setuptools import setup, find_packages


def get_long_description():
    """
    Return the README.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f"{dir_path}/README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="fast-micro",
    python_requires=">=3.6",
    version="0.0.13",
    url="https://github.com/patrickfnielsen/fast-micro",
    description="Opinionated FastAPI microservice setup to provide correlation, camelCase models, and struct logging",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Patrick Falk Nielsen",
    author_email="patrick@6k.io",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "fastapi",
        "requests",
        "structlog",
        "starlette-context"
    ],
    keywords=[
        "fastapi",
        "tracing",
        "correlation"
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    zip_safe=False,
)