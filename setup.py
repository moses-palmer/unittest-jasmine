#!/usr/bin/env python
# coding: utf8

import os
import setuptools


#: The name of the package on PyPi
PYPI_PACKAGE_NAME = 'unittest-jasmine'

#: The name of the main Python package
MAIN_PACKAGE_NAME = 'unittest_jasmine'

#: The package URL
PACKAGE_URL = 'https://github.com/moses-palmer/unittest-jasmine'

#: The author email
AUTHOR_EMAIL = 'moses.palmer@gmail.com'

#: The runtime requirements
RUNTIME_PACKAGES = []

#: Additional requirements used during setup
SETUP_PACKAGES = []


# Read globals from ._info without loading it
INFO = {}
with open(os.path.join(
        os.path.dirname(__file__),
        'lib',
        MAIN_PACKAGE_NAME,
        '_info.py')) as f:
    for line in f:
        try:
            name, value = (i.strip() for i in line.split('='))
            if name.startswith('__') and name.endswith('__'):
                INFO[name[2:-2]] = eval(value)
        except ValueError:
            pass


# Load the read me
try:
    with open(os.path.join(
            os.path.dirname(__file__),
            'README.rst')) as f:
        README = f.read()
except IOError:
    README = ''


# Load the release notes
try:
    with open(os.path.join(
            os.path.dirname(__file__),
            'CHANGES.rst')) as f:
        CHANGES = f.read()
except IOError:
    CHANGES = ''


setuptools.setup(
    name=PYPI_PACKAGE_NAME,
    version='.'.join(str(i) for i in INFO['version']),
    description='A unittest test loader for Jasmine tests',
    long_description=README + '\n\n' + CHANGES,

    install_requires=RUNTIME_PACKAGES,
    setup_requires=RUNTIME_PACKAGES + SETUP_PACKAGES,

    author=INFO['author'],
    author_email=AUTHOR_EMAIL,

    url=PACKAGE_URL,

    packages=setuptools.find_packages(
        os.path.join(
            os.path.dirname(__file__),
            'lib')),
    package_dir={'': 'lib'},
    zip_safe=True,

    test_suite='tests',

    license='GPLv3',
    classifiers=[])
