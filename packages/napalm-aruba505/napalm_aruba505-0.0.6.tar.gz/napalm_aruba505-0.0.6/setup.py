"""setup.py file."""
import os
from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name = "napalm_aruba505",
    version = "0.0.6",
    author = "David Johnnes",
    author_email = "david.johnnes@gmail.com",
    description = ("Napaml Aruba driver for ArubaOs Wi-Fi devices '505' "),
    license = "BSD",
    keywords = "napalm drive",
    url="https://github.com/napalm-automation/napalm-arubaOS",
    packages=['napalm_aruba505'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
)