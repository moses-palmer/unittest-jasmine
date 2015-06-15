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
This module handles installation of dependencies for *JavaScript*.

Currently, the only supported package manager is ``npm``.

To add other package managers, use the :func:`register` decorator on a class
with an argument-less constructor and which implements the
:meth:`~NPM.install_dependencies` method.
"""

import logging
import os
import subprocess


log = logging.getLogger(
        '.'.join((__name__, 'npm')))


PACKAGE_MANAGERS = []


def register(klass):
    """A decorator to register a class as a package manager.

    The class is added to the head of the list of package managers, so when
    calling, :func:`install_dependencies`, the package manager registered last
    will take precedence.

    :param type class: The class to register.
    """
    PACKAGE_MANAGERS.insert(0, klass)
    return klass


@register
class NPM(object):
    """A class to manage and detect ``npm``.
    """
    #: The command used to launch ``npm``
    COMMAND = 'npm'

    #: The files used by ``npm`` to specify dependencies
    DEPENDENCY_FILES = (
        'package.json',
        'npm-shrinkwrap.json')

    log = logging.getLogger(
        '.'.join((__name__, 'npm')))

    def __init__(self):
        if not any(
                os.path.isfile(dependency_file)
                for dependency_file in self.DEPENDENCY_FILES):
            self.log.warn('Not npm package directory: %s', os.getcwd())
            raise ValueError('invalid current working directory')

        try:
            output = subprocess.check_output(
                [self.COMMAND, '--version'],
                stderr=subprocess.STDOUT).strip().decode('ascii')
        except:
            self.log.exception('Failed to get npm version')
            raise

        try:
            self.version = tuple(int(p) for p in output.split('.'))
            self.log.debug('Using npm version %s', '.'.join(
                str(p) for p in self.version))
        except:
            self.log.exception('Failed to parse npm version %s', output)
            raise

    def install_dependencies(self):
        """Installs dependencies.

        This method will simply execute the command ``npm install`` using
        :func:`subprocess.check_call`. Any exceptions raised by that call will
        be re-raised.
        """
        self.log.info('Installing dependencies')
        try:
            subprocess.check_output(
                [self.COMMAND, 'install'],
                stderr=subprocess.STDOUT)
        except:
            self.log.exception('Failed to install packages using npm')
            raise


def install_dependencies():
    """Installs dependencies.

    This function will iterate over all installed package managers and try to
    use them to install dependencies. Once one is successful, no more will be
    called.

    :return: the package manager that serviced the request
    """
    for package_manager_class in PACKAGE_MANAGERS:
        try:
            package_manager = package_manager_class()
            package_manager.install_dependencies()
            return package_manager
        except:
            log.exception(
                'Package manager %s failed',
                package_manager_class.__name__)
