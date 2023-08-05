# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2021-2022 Thorsten Simons (sw@snomis.eu)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Sos of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyrighftware without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copiet notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys
from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path
# this is to be able to get the version without importing *hcilib*,
# which would cause *pip install* to fail.
sys.path.insert(0, path.abspath('hcilib'))
from hcilib.version import Gvars

# Get the long description from the relevant file
with open(path.join(path.abspath(path.dirname(__file__)),
                    'DESCRIPTION.rst'),
          encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hcisle',
    version=str(Gvars.s_version),
    description=Gvars.Description,
    long_description=long_description,
    url='https://hcisle.readthedocs.org',
    author=Gvars.Author,
    author_email=Gvars.AuthorMail,
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Archiving',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    keywords='Hitachi Content Intelligence',
    packages=find_packages(exclude=[]),
    install_requires=[],
    entry_points={'console_scripts': ['hcisle = hcilib.__main__:main']}
)
