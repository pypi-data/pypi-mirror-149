#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import setuptools

import alpy

setuptools.setup(
    name="alpy",
    version=alpy.__version__,
    description="Library for testing network virtual appliances using Docker",
    url="https://gitlab.com/abogdanenko/alpy",
    packages=["alpy"],
    install_requires=["docker", "pexpect", "qmp"],
    author="Alexey Bogdanenko",
    author_email="alexey@bogdanenko.com",
    long_description=Path("README.rst").read_text(encoding="ascii"),
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
)
