# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the MIT License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import re
import ast
from setuptools import find_packages, setup

classes = """
    License :: OSI Approved :: BSD License
    Topic :: Scientific/Engineering
    Topic :: Scientific/Engineering :: Bio-Informatics
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3 :: Only
    Operating System :: Unix
    Operating System :: POSIX
    Operating System :: MacOS :: MacOS X
"""

classifiers = [s.strip() for s in classes.split('\n') if s]

description = (
    "Help a user parse and select (and label) papers searched on Web Of "
    "Science based on their abstracts."
)

with open("README.md") as f:
    long_description = f.read()

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("Xpress_parse/__init__.py", "rb") as f:
    hit = _version_re.search(f.read().decode("utf-8")).group(1)
    version = str(ast.literal_eval(hit))

standalone = [
    'Xpress=Xpress_parse.scripts._standalone_xpress_parse:standalone_xpress'
]

setup(
    name="Xpress_parse",
    version=version,
    license="BSD",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Franck Lejzerowicz",
    author_email="franck.lejzerowicz@gmail.com",
    maintainer="Franck Lejzerowicz",
    maintainer_email="franck.lejzerowicz@gmail.com",
    url="https://github.com/FranckLejzerowicz/Xpress_parse",
    packages=find_packages(),
    install_requires=["click", "pandas", "numpy"],
    classifiers=classifiers,
    entry_points={'console_scripts': standalone},
    python_requires='>=3.6'
)
