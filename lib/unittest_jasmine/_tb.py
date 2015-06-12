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
This module contains classes for mocking tracebacks.
"""

import linecache
import itertools
import re


class Code(object):
    """A mock code object used in tracebacks.
    """
    def __init__(self, co_filename, co_name):
        linecache.updatecache(co_filename, None)
        self.co_filename = co_filename
        self.co_name = co_name


class Frame(object):
    """A mock frame object used in tracebacks.
    """
    def __init__(self, f_code):
        self.f_code = f_code
        self.f_globals = {}


class Traceback(object):
    """A mock traceback.
    """
    #: The regular expression used to parse a stack entry
    STACK_RE = re.compile(
        r'\s*at\s+([a-zA-Z_][a-zA-Z0-9_.<>]*)\s+\((.*?):([0-9]+):([0-9]+)\)')

    def __init__(self, frames, line_nums):
        self._frames = frames
        self._line_nums = line_nums
        self.tb_frame = self._frames[0]
        self.tb_lineno = self._line_nums[0]

    @property
    def tb_next(self):
        if len(self._frames) > 1:
            return Traceback(self._frames[1:], self._line_nums[1:])

    @classmethod
    def _frames(self, stack):
        """Yields all frames and line numbers from a *Jasmine* stack as the
        tuple ``(frame, line)``.

        :param str stack: The stack text.
        """
        for m in self.STACK_RE.finditer(stack):
            co_name, co_filename, line = m.group(1), m.group(2), m.group(3)

            yield (Frame(Code(co_filename, co_name)), int(line))

    @classmethod
    def _is_user_test(self, frame):
        """Determines whether a stack frame is from inside of a user test case.

        :param Frame frame: The frame to check.

        :return: whether the frame is from a user test case
        """
        # TODO: Determine this in a better way
        return 'jasmine-core' not in frame.f_code.co_filename

    @classmethod
    def from_stack(self, stack):
        """Generates a mock traceback from a *Jasmine* stack trace string.

        This method takes a string on the form:

            Error: Expected 2 to equal 1.
                at stack (.../jasmine-core/jasmine.js:1482:17)
                at buildExpectationResult (.../jasmine-core/jasmine.js:1452:14)
                at Expectation.toEqual (.../jasmine-core/jasmine.js:1406:12)
                at func (.../test.js:5:23)
                at Object.<anonymous> (.../test.js:7:9)
                at attemptSync (.../jasmine-core/jasmine.js:1789:24)
                at QueueRunner.run (.../jasmine.js:1777:9)

        and return an object which, when passed to :func:`traceback.print_tb`,
        will be represented as:

            File ".../test-runner.js", line 7, in Object.<anonymous>
                func();
            File ".../test-runner.js", line 5, in func
                expect(2).toEqual(1);

        :param str stack: The *Jasmine* stack description string.

        :return: a mock
        """
        return self(*zip(*reversed(list(
            itertools.takewhile(
                lambda fl: self._is_user_test(fl[0]),
                itertools.dropwhile(
                    lambda fl: not self._is_user_test(fl[0]),
                    self._frames(stack)))))))
