#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

requirements = ["Click>=7.0", "pygame"]
dev_requirements = [
    "pip",
    "bump2version",
    "wheel",
    "watchdog",
    "twine",
]  # TODO: could be split into dev and publishing requirements
test_requirements = ["pytest>=3", "pytest", "tox", "coverage", "flake8"]


docs_requirements = ["sphinx"]

extras = {
    "dev": dev_requirements,
    "test": test_requirements,
    "docs": docs_requirements,
}

setup(
    author="Georg Jäger",
    author_email="georg.jaeger@informatik.tu-freiberg.de",
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
    description="An endless jumping game to develop AI agents for",
    entry_points={
        "console_scripts": [
            "bouncai=bouncai.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n",
    include_package_data=True,
    keywords="bouncai",
    name="bouncai",
    packages=find_packages(include=["bouncai", "bouncai.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    extras_require=extras,
    url="https://github.com/gjaeger1/bouncai",
    version="0.1.0",
    zip_safe=False,
)
