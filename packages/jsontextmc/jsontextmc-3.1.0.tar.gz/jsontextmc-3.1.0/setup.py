#!/usr/bin/env python3
# coding=utf-8
import setuptools

from jsontextmc import __version__

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsontextmc",
    version=__version__,
    author="whoatemybutter",
    author_email="\"whoatemybutter\" <4616947-whoatemybutter@users.noreply.gitlab.com>",
    description="Tool to translate old Minecraft formatting codes to the modern JSON format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/whoatemybutter/jsontextmc",
    packages=setuptools.find_packages(),
    license="GPL version 3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Localization",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
        "Topic :: Games/Entertainment :: Simulation",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Indexing"
    ],
    python_requires='>=3.9',
)
