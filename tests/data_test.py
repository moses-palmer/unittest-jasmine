import types
import unittest

import unittest_jasmine

from . import _res as res

spec = unittest_jasmine.data.JasmineSpec
suite = unittest_jasmine.data.JasmineSuite


class JasmineDataTest(unittest.TestCase):
    def suite(self, spec=spec, suite=suite):
        return suite(
                [
                    suite(
                        [
                            spec(
                                'spec0',
                                'Spec 0',
                                'This is spec 0'),
                            spec(
                                'spec1',
                                'Spec 1',
                                'This is spec 1')],
                        'suite1',
                        'Suite 1',
                        'This is Suite 1'),
                    spec(
                        'spec2',
                        'Spec 2',
                        'This is spec 2')],
                'suite0',
                'Suite 0',
                'This is Suite 0')

    def test_parse(self):
        """Tests that parsing a dict returns the expected value"""
        self.assertEqual(
            self.suite(),
            unittest_jasmine.data.parse(res.SUITE_DEFINITION))

    def test_parse_invalid(self):
        """Tests that parsing an invalid dict raises ValueError"""
        with self.assertRaises(ValueError):
            unittest_jasmine.data.parse(dict(
                type='__invalid_type___',
                id='id',
                fullName='fullName',
                description='description'))

    def test_parse_missing(self):
        """Tests that parsing a dict with missing values raises KeyError"""
        with self.assertRaises(KeyError):
            unittest_jasmine.data.parse(dict(
                type='spec',
                fullName='fullName',
                description='description'))

    def test_parse_custom(self):
        """Tests that passing custom generator functions returns the expected
        value"""
        def test_spec(id, name, description, **kwargs):
            s = spec(id, name, description)
            s.kwargs = kwargs
            return s

        def test_suite(children, id, name, description, **kwargs):
            s = suite(children, id, name, description)
            s.kwargs = kwargs
            return s

        data = unittest_jasmine.data.parse(
            res.SUITE_DEFINITION,
            test_spec,
            test_suite,
            test=True,
            test_name='test')

        self.assertEqual(self.suite(), data)

        def visitor(i):
            self.assertTrue(i.kwargs['test'])
            self.assertEqual(
                'test',
                i.kwargs['test_name'])
            for c in getattr(i, 'children', []):
                visitor(c)
        visitor(data)

    def test_order(self):
        """Tests that the order of tests and suites correspond to the events
        returned by the runner"""
        output = res.output()
        tree = next(output)

        def expect(event, data_id):
            o = next(output)
            self.assertEqual(
                event,
                o['event'])
            self.assertEqual(
                data_id,
                o['data']['id'])

        def test_spec(id, name, description, **kwargs):
            def load(self):
                expect('specStarted', self.id)
                expect('specDone', self.id)
            s = spec(id, name, description)
            s.load = types.MethodType(load, s)
            return s

        def test_suite(children, id, name, description, **kwargs):
            def load(self):
                expect('suiteStarted', self.id)
                for child in children:
                    child.load()
                expect('suiteDone', self.id)
            s = suite(children, id, name, description)
            s.load = types.MethodType(load, s)
            return s

        # The top-level suite is not run
        for i in unittest_jasmine.data.parse(
                tree,
                test_spec,
                test_suite).children:
            i.load()
