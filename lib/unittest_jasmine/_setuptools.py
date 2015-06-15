# coding=utf-8
# unittest-jasmine
# Copyright (C) 2015 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
"""
This module provides a *unittest* test loader that extends the scanning test
loader from *setuptools* and allows it to load *Jasmine* tests as well.
"""

import importlib
import json
import os
import re
import setuptools.command.test
import types

from . import data, package_manager, runner, unittest


def suite_setup(suite):
    """Called before every suite is run.

    Add an implementation of this to your own lifecycle module.

    :param unittest_jasmine.unittest.Suite suite: The suite that is about to
        start.
    """
    pass


def suite_teardown(suite):
    """Called after every suite has run.

    Add an implementation of this to your own lifecycle module.

    :param unittest_jasmine.unittest.Suite suite: The suite that has completed.
    """
    pass


def test_setup(test):
    """Called before every test is run.

    Add an implementation of this to your own lifecycle module.

    :param unittest_jasmine.unittest.Test test: The test that is about to
        start.
    """
    pass


def test_teardown(test):
    """Called after every test has run.

    Add an implementation of this to your own lifecycle module.

    :param unittest_jasmine.unittest.Test test: The test that has completed.
    """
    pass


class SetuptoolsLoader(setuptools.command.test.ScanningLoader):
    """A scanning test loader to use when running tests from
    :func:`setuptools.setup`.

    Set the ``test_loader`` parameter to ``'unittest_jasmine.setup:Loader'`` to
    use this loader.

    By default, this loader will, in addition to the tests loaded by
    :class:`setuptools.command.test.ScanningLoader`, load all files matching
    the pattern ``*spec.js`` in the *unittest* test package directory.

    This loader extends the interpretation of the ``test_suite`` parameter to
    :func:`setuptools.setup` as
    ``test_suite[|option1=value1[;option2=value2...]]``.

    Option values can be specified as *JSON* or a simple strings. An attempt to
    parse the value as *JSON* is always made, and if it fails, the option value
    is used as a string.

    Note that this handling of option strings will yield ``{'key': True}`` for
    ``'key=true'`` and ``{'key ': ' true'}`` for ``'key = true'``.

    If the test package does not contain any *unittest* tests, and the
    *setuptools* scanning loader is thus unable to find a test, or if the
    *Jasmine* tests are in a different directory, you must specify
    ``test_directory``. An example value is
    ``'test|test_directory=/home/user/src/project/test'``.

    If the spec files do not match the pattern above, or if you intend to run
    *CoffeeScript* specs, you must specify ``spec_regexp``. An example value is
    ``'test|spec_regexp=.*?\.(coffee|js)'``. Also note that in order to run
    *CoffeeScript* specs, you must add the call
    ``require("coffee-script/register")`` to one of the helper files.

    If you have any *Python* code to run before and after suites and tests are
    run, implement the functions :func:`suite_setup`, :func:`suite_teardown`,
    :func:`test_setup` and :func:`test_teardown` in a module and pass its name
    as the option ``lifecycle``. This is where to implement launching of for
    example the *Python* web server being tested.

    Any other option values will be passed to the *Jasmine* ``loadConfig``
    method.

    Of those options, the one most commonly used will be ``helpers``. This must
    be a list of strings, so it must be a *JSON* value. It is interpreted as a
    list of helper files, relative to ``test_directory``, that *Jasmine* will
    load before running the tests.
    """
    def _parse_option(self, option):
        """Parses an option string.

        The string is expected to be on the form ``'key=value'``. Whitespace is
        stripped from the start and end of the string.

        The value of ``key`` is used verbatim as the key name.

        The value of ``value`` is first passed to :func:`json.loads`. If this
        is successful, the parsed value is used in the return value, otherwise
        the actual string is used.

        :param str option: The option string to parse.

        :return: the tuple ``(key, value)``, suitable for creation of a
            ``dict``
        """
        key, value = option.strip().split('=')
        try:
            return (key, json.loads(value))
        except ValueError:
            return (key, value)

    def _parse_name(self, name):
        """Parses a test suite name into the actual test package name and
        options.

        :param str name: The name to parse.

        :return: the actual name and any options passed
        :rtype: (str, dict)
        """
        try:
            name, option_strings = name.split('|', 1)
        except ValueError:
            return (
                name,
                {})

        # Parse the options
        return (
            name,
            dict(
                self._parse_option(v)
                for v in option_strings.split(';')))

    def _guess_test_directory(self, name):
        """Guesses the test directory to use by trying to import ``name``.

        If the package cannot be imported, ``None`` is returned.

        :param str name: The test package name.

        :return: a path or ``None``
        :rtype: str or None
        """
        try:
            m = importlib.import_module(name)
            return os.path.dirname(m.__file__)
        except ImportError:
            return None

    def _apply_lifecycle(self, test_item, lifecycle):
        """Sets the setup and teardown methods of all test items recursively.

        :param test_item: The test item to modify. If this is a suite, this
            method is called recursively for all children.
        :type test_item: unittest_jasmine.unittest.Test or
            unittest_jasmine.unittest.Suite

        :param lifecycle: The module containing the event functions.
        """
        def add(target, source):
            setattr(
                test_item,
                target,
                types.MethodType(
                    getattr(
                        lifecycle, source, globals()[source]),
                    test_item,
                    test_item.__class__))
        if isinstance(test_item, unittest.Suite):
            add('setUp', 'suite_setup')
            add('tearDown', 'suite_teardown')
            for child in test_item.children:
                self._apply_lifecycle(child, lifecycle)
        elif isinstance(test_item, unittest.Test):
            add('setUp', 'test_setup')
            add('tearDown', 'test_teardown')

    def loadTestsFromNames(self, names, module=None):
        # Extract the package name and options from the names passed; names
        # will be a list with one item: the value of test_suite passed to
        # setuptools.setup
        name, options = self._parse_name(names[0])

        # First load the unittest tests
        tests = super(SetuptoolsLoader, self).loadTestsFromNames(
            [name] + names[1:],
            module)

        # Pop option values used by this method
        test_directory = options.pop(
            'test_directory',
            self._guess_test_directory(name))

        spec_regex = re.compile(options.pop(
            'spec_regex',
            r'.*?spec\.js'))

        lifecycle = importlib.import_module(options.pop(
            'lifecycle',
            __name__))

        # If we have a test directory, load the tests
        if test_directory:
            jasmine = runner.jasmine(
                test_directory,
                *(
                    f
                    for f in os.listdir(test_directory)
                    if spec_regex.match(f)),
                **options)

            # Read the full test tree and make sure it knows about Jasmine
            top_suite = data.parse(
                next(jasmine),
                spec=unittest.Test,
                suite=unittest.Suite)
            top_suite.jasmine = jasmine

            # Make sure setup and teardown functions are called; do not modify
            # the top suite, as user tests should not receive notifications
            # about it
            for suite in top_suite.children:
                self._apply_lifecycle(suite, lifecycle)

            # Make sure that dependencies are installed when the top suite is
            # run
            top_suite.setUp = types.MethodType(
                lambda self: package_manager.install_dependencies(),
                top_suite,
                top_suite.__class__)

            # Finally add the test suite
            tests.addTest(top_suite)

        return tests
