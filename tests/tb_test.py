import os
import traceback
import unittest

import unittest_jasmine


class TracebackTest(unittest.TestCase):
    def test_tb(self):
        """Asserts that a correct traceback is generated"""
        path = os.path.join(os.path.dirname(__file__), 'res', 'test-runner.js')
        expected = ' '.join("""
            File "{0}", line 7, in Object.<anonymous>
                func();
            File "{0}", line 5, in func
                expect(2).toEqual(1);""".format(path).split())
        tb = unittest_jasmine.tb.Traceback.from_stack("""
            Error: Expected 2 to equal 1.
                at stack (.../jasmine-core/jasmine.js:1482:17)
                at buildExpectationResult (.../jasmine-core/jasmine.js:1452:14)
                at Expectation.toEqual (.../jasmine-core/jasmine.js:1406:12)
                at func ({0}:5:23)
                at Object.<anonymous> ({0}:7:9)
                at attemptSync (.../jasmine-core/jasmine.js:1789:24)
                at QueueRunner.run (.../jasmine.js:1777:9)""".format(path))
        self.assertEqual(
            expected,
            ' '.join(' '.join(traceback.format_tb(tb)).split()))
