#!/usr/bin/env python3
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scheduletask",
    version="1.1.0",
    author="Shinwaffle",
    author_email="shinwaffle@gmail.com",
    description="Create google calendar events from the command line",
    long_description="I'm gonna add a longer description later",
    long_description_content_type="text/markdown",
    url="https://github.com/shinwaffle/scheduletask",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_s= ["scheduletask"],
    entry_points = {
        "console_scripts": ['scheduletask = scheduletask.scheduletask:main']
    },
    python_requires=">=3.6",
)