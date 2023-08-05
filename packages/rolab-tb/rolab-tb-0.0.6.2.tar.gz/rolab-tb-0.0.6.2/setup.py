# SPDX-FileCopyrightText: 2022 Senne Van Baelen
#
# SPDX-License-Identifier: Apache-2.0

import setuptools

""" python package config """

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rolab-tb",
    version="0.0.6.2",
    author="Senne Van Baelen",
    author_email="senne.vanbaelen@kuleuven.be",
    description="Lightweight ROS-less API for Turtlebots, over a websocket bridge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="",
    # project_urls={
        # "Bug Tracker": "link-to-issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    include_package_data=True,
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'numpy',
        'websockets'
        ]
    )
