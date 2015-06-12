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
This module tries to determine the command used to launch ``node`` on the
current system.

Since node.js picked an already used binary name, we must check whether
``node`` is *node.js* or *node - Amateur Packet Radio Node program*. The latter
is the case on some *Debian* based systems.

If no suitable executable is found, ``ImportError`` is raised.
"""

import subprocess


def run(command, *args, **kwargs):
    """Calls ``node`` using :class:`subprocess.Popen` with the arguments given.

    This function makes sure to set the first argument to the command to invoke
    ``node``.

    This function is simply a thin wrapper around the
    :class:`~subprocess.Popen` constructor, and ``*args`` and ``**kwargs`` are
    simply passed on. It returns the value returned by the constructor.
    """
    return subprocess.Popen([BINARY] + command, *args, **kwargs)


def _locate_node():
    """Determines the command to use to invoke ``node``.

    :return: the command to use, or ``None`` if ``node`` is not installed

    :rtype: str or None
    """
    # Since node.js picked an already used binary name, we must check whether
    # `node` is node.js or node - Amateur Packet Radio Node program
    for node in ('node', 'nodejs'):
        try:
            node_output = subprocess.check_output([
                node, '--eval', 'console.log("%s")' % __name__])
            if node_output.strip().decode('ascii') == __name__:
                return node
        except OSError:
            pass

BINARY = _locate_node()
if BINARY is None:
    raise ImportError('node is not available')
