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
This module provides a generator that yields events from a *Jasmine* test run.
"""

import json
import logging
import os
import pkg_resources
import subprocess

from . import node


log = logging.getLogger(__name__)


#: The name of the runner *JavaScript*
RUNNER_NAME = 'runner.js'


def jasmine(project_dir, *files, **options):
    """Generates events from a test run.

    Each event is a ``dict`` and has the keys ``event``, which is the event
    type, and ``data``, which is data associated with the event.

    The event names correspond to the *Jasmine* reporter callback methods, and
    the data to their data argument. Please see ``./runner.js`` and the
    *Jasmine* documentation and source code for more information.

    :param str project_dir: The base project directory. This can be set to
        either the base directory of the project, or the actual path to the
        spec files. If set to the project directory, ``options`` must contain
        the value ``'spec_dir'``, which is the relative path to the spec files.

    :param [str] files: The spec files. These paths must be relative to
        ``project_dir`` and, if specified, ``options['spec_dir']``.

    :param options: Any configuration options passed to *Jasmine*. This value
        is sent to ``Jasmine.loadConfig``.
    """
    # spec_dir must be set
    if 'spec_dir' not in options:
        options['spec_dir'] = '.'

    p = node.run(
        ['-e', RUNNER_DATA, project_dir, json.dumps(options)] + list(files),
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE)

    try:
        for line in p.stdout:
            try:
                yield json.loads(line.strip().decode('ascii'))
            except ValueError:
                log.exception(
                    'Invalid output from %s: %s',
                    RUNNER_NAME,
                    line.strip())
                continue
    finally:
        p.stdin.close()
        p.stdout.close()


def _get_runner_from_filesystem():
    with open(os.path.join(os.path.dirname(__file__), RUNNER_NAME), 'r') as f:
        return f.read()


def _get_runner_from_pkgresources():
    return pkg_resources.resource_stream(
        __name__.rsplit('.', 1)[0], RUNNER_NAME).read()


def _get_runner():
    try:
        return _get_runner_from_filesystem()
    except IOError:
        return _get_runner_from_pkgresources()


try:
    RUNNER_DATA = _get_runner()
except:
    raise ImportError('failed to load Jasmine runner')
