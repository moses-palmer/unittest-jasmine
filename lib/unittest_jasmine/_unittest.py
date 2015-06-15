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
This module provides classes to integrate with ``unittest``.
"""

import unittest

from . import data, tb


class TestItem(object):
    """The base class for all *Jasmine* test items.
    """
    def __init__(self):
        object.__init__(self)
        self._parent = self

    def __str__(self):
        return '.'.join(reversed([i.id for i in self.ancestors]))

    @property
    def ancestors(self):
        """The parent suites, not including the top level suite"""
        i = self
        while i._parent is not i:
            yield i
            i = i._parent

    @property
    def topsuite(self):
        """The top level suite"""
        result = self
        while result._parent != result:
            result = result._parent
        return result

    @property
    def jasmine(self):
        """The jasmine runner used by this suite collection"""
        return getattr(self.topsuite, '_jasmine', None)

    @jasmine.setter
    def jasmine(self, jasmine):
        self.topsuite._jasmine = jasmine


class Test(TestItem, data.JasmineSpec, unittest.TestCase):
    #: This must be set, but we do not support calling it
    runTest = None

    def __init__(self, id, name, description):
        TestItem.__init__(self)
        data.JasmineSpec.__init__(self, id, name, description)
        unittest.TestCase.__init__(self)

    @property
    def data(self):
        """The ``data`` part of the result"""
        return self.result.get('data', {})

    def _add_failures(self, result):
        """Adds all failures from the test run to a test result.

        The failures are taken from :attr:`result`.

        :param unittest.TestResult result: The test result to which to add the
            failures.
        """
        for failure in self.data['failedExpectations']:
            result.addFailure(
                self,
                err=(
                    AssertionError,
                    AssertionError(failure['message']),
                    tb.Traceback.from_stack(failure['stack'])))

    def run(self, result=None):
        # Make sure we have a result to run with; this is copied from the
        # unittest implementation
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        result.startTest(self)

        try:
            self.setUp()
            try:
                with self.running(self.jasmine):
                    pass
            finally:
                self.tearDown()

            # Get the test result; if the test passed, we just add success
            if self.data['status'] == 'passed':
                result.addSuccess(self)
            else:
                self._add_failures(result)

        finally:
            result.stopTest(self)

    def shortDescription(self):
        return self.name


class Suite(TestItem, data.JasmineSuite, unittest.TestSuite):
    def __init__(self, children, id, name, description):
        TestItem.__init__(self)
        data.JasmineSuite.__init__(self, children, id, name, description)
        unittest.TestSuite.__init__(self, self.children)

        for child in children:
            child._parent = self

    def setUp(self):
        """Called before the suite is started.

        Despite the naming convention used, this is not a standard *unittest*
        method; it is added for consistency with :meth:`Test.setUp`.

        By default, this method does nothing; add a replacement if necessary.
        """
        pass

    def tearDown(self):
        """Called when the suite has completed.

        Despite the naming convention used, this is not a standard *unittest*
        method; it is added for consistency with :meth:`Test.tearDown`.

        By default, this method does nothing; add a replacement if necessary.
        """
        pass

    def run(self, result, debug=False):
        self.setUp()

        try:
            # If this is the top level suite, run the suite outside of the
            # context manager, since it is just a container suite
            if self.topsuite is self:
                return super(Suite, self).run(result, debug)

            with self.running(self.jasmine):
                return super(Suite, self).run(result, debug)

        finally:
            self.tearDown()
