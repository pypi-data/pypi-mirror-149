import os
import re

import pkg_resources
import setuptools

from lwdia.settings import *

long_description = open("README.md", "r", encoding="utf-8").read()

setuptools.setup(
    name=app_name,
    version=app_version,
    author=app_author,
    author_email=app_author_email,
    maintainer=app_maintainer,
    maintainer_email=app_maintainer_email,
    description=app_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=app_url,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "lwdia=lwdia:spend",
        ]
    },
    python_requires=">=3.6",
    install_requires=get_requirements_product(),
    include_package_data=True,
)
