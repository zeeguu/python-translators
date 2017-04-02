#!/usr/bin/env python
# -*- coding: utf8 -*-

import setuptools


setuptools.setup(
    name="translators",
    version="0.1",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    author="The Jager",
    author_email="...",
    description="...",
    keywords="...",
    install_requires=(
        "google-api-python-client",
        "configobj",
        "requests")
)