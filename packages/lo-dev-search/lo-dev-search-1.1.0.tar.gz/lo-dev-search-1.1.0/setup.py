#!/usr/bin/env python
import pathlib
from setuptools import setup, find_packages
# from scriptforge_stubs import __version__
PKG_NAME = 'lo-dev-search'
VERSION = "1.1.0"

# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
with open(HERE / "README.md") as fh:
    README = fh.read()

setup(
    name=PKG_NAME,
    version=VERSION,
    package_data={"": ["*.json", "*.sqlite"]},
    python_requires='>=3.7.0',
    url="https://github.com/Amourspirit/python_lo_dev_search",
    packages=find_packages(),
    author=":Barry-Thomas-Paul: Moss",
    author_email='bigbytetech@gmail.com',
    license="mit",
    keywords=['libreoffice', 'openoffice' 'search', 'searchengine', 'uno', 'ooouno', 'pyuno'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Office/Business",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points = {
        'console_scripts': [
            'lodoc=lo_dev_search.cli.lodoc:main',
            'loguide=lo_dev_search.cli.loguide:main',
            'loapi=lo_dev_search.cli.loapi:main',
        ]
    },
    description="LibreOffice Developer Search Engine",
    long_description_content_type="text/markdown",
    long_description=README
)