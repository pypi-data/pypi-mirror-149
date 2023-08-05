#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import pathlib
import pkg_resources

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

with open("VERSION") as version_file:
    version = version_file.read().strip()

with pathlib.Path("requirements/prod.txt").open() as requirements_txt:
    install_requirements = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]

with pathlib.Path("requirements/test.txt").open() as requirements_txt:
    test_requirements = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    author="Paul Armstrong",
    author_email="parmstrong@gitlab.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Simple python API wrapper for interacting with Tiingo endpoints",
    install_requires=install_requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="tiingo_news_api",
    name="tiingo_news_api",
    packages=find_packages(include=["tiingo_news_api", "tiingo_news_api.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://gitlab.com/paul_armstrong/tiingo_news_api",
    version=version,
    zip_safe=False,
)
