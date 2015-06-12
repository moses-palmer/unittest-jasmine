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

import itertools
import re


class Code(object):
    """A mock code object used in tracebacks.
    """
    def __init__(self, co_filename, co_name):
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
