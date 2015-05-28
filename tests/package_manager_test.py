import contextlib
import unittest

import unittest_jasmine


@unittest_jasmine.package_manager.register
class Interceptor(object):
    #: Whether this class should intercept package manager calls
    _COUNT = 0

    #: A counter that is incremented each time :meth:`install_dependencies` is
    #: called and set to ``0`` when :meth:`active` is called
    _CALL_COUNT = 0

    @classmethod
    @contextlib.contextmanager
    def active(self):
        """A context manager to run a code block with this class active as a
        package manager.
        """
        self._COUNT += 1
        self._CALL_COUNT = 0
        try:
            yield
        finally:
            self._COUNT -= 1

    @classmethod
    def was_called(self):
        """Returns whether :meth:`install_dependencies` has been called.
        """
        return self._CALL_COUNT > 0

    def __init__(self):
        if not self._COUNT:
            raise RuntimeError()

    def install_dependencies(self):
        Interceptor._CALL_COUNT += 1


class PackageManagerTest(unittest.TestCase):
    def test_no_manager(self):
        """Tests that NotImplementedError is raised when no manager handles
        request"""
        backup = unittest_jasmine.package_manager.PACKAGE_MANAGERS
        unittest_jasmine.package_manager.PACKAGE_MANAGERS = []
        try:
            with self.assertRaises(NotImplementedError):
                unittest_jasmine.package_manager.install_dependencies()
        finally:
            unittest_jasmine.package_manager.PACKAGE_MANAGERS = backup

    def test_install_dependencies(self):
        """Tests that a manager is called"""
        with Interceptor.active():
            self.assertIsInstance(
                unittest_jasmine.package_manager.install_dependencies(),
                Interceptor)
        self.assertTrue(
            Interceptor.was_called())

    def test_npm(self):
        """Tests that the npm manager works"""
        self.assertIsInstance(
            unittest_jasmine.package_manager.install_dependencies(),
            unittest_jasmine.package_manager.NPM)
