"""setup.py file."""
import os
from setuptools import setup

def read(fname):
    with open("README.md") as f:
        return f.read()

setup(
    name = "napalm_aruba505",
    version = "0.0.5",
    author = "David Johnnes",
    author_email = "david.johnnes@gmail.com",
    description = ("Napaml Aruba driver for ArubaOs Wi-Fi devices '505' "),
    license = "BSD",
    keywords = "napalm drive",
    url="https://github.com/napalm-automation/napalm-arubaOS",
    packages=['napalm_aruba505'],
    long_description=read('README.md'),
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
)