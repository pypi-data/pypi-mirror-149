# -*- coding: utf-8 -*-
# Create Time: 2022/2/13 11:11
# Author: nzj
# Function：
from setuptools import find_packages, setup


def read_long_description_from_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

setup(
    name="dbc-parse",
    version="1.0.11",
    packages=find_packages(include=["dbc_parse"]),
    description="Database Parse",
    long_description=read_long_description_from_readme(),
    long_description_content_type="text/markdown",
    author="nzj",
    author_email="nzjwoaini9@gmail.com",
    keywords=["database"],
    package_data={
        # Include anything in the data directory
        "openstef_dbc": ["data/*", "*.license"]
    },
    python_requires=">=3.9.0",
    classifiers=[
        r"Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        r"License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
