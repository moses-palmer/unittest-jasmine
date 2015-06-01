import os
import types
import unittest

import unittest_jasmine

from . import _res as res


class RunnerTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RunnerTest, self).__init__(*args, **kwargs)
        unittest_jasmine.package_manager.install_dependencies()

    def subdict(self, source, template):
        """Returns a copy of ``source`` where only the keys from ``template``
        are present.

        This method copies values recursively, including lists.

        :param dict source: The source dictionary.

        :param dict template: The dictionary containing the keys of interest.

        :return: a dictionary containing at most keys from template
        """
        def value(s, t):
            if isinstance(s, types.ListType):
                return [self.subdict(v1, v2) for v1, v2 in zip(s, t)]
            elif isinstance(s, types.DictType):
                return self.subdict(s, t)
            else:
                return s

        return dict(
            ((k, value(source[k], template[k])))
            for k in source
            if k in template)

    def test_runner_output(self):
        """Tests that the runner provides the expected output"""
        output = list(res.output())
        expected_output = list(res.TEST_OUTPUT)

        self.assertEqual(
            len(expected_output),
            len(output))

        for actual, expected in zip(output, expected_output):
            self.assertEqual(
                expected,
                self.subdict(actual, expected))

    def test_runner_output_coffee_script(self):
        """Tests that the runner provides the expected output for a Coffee
        Script test suite"""
        output = list(res.output(
            helpers=[os.path.join('res', 'coffee-script-activate.js')]))
        expected_output = list(res.TEST_OUTPUT)

        self.assertEqual(
            len(expected_output),
            len(output))

        for actual, expected in zip(output, expected_output):
            self.assertEqual(
                expected,
                self.subdict(actual, expected))
