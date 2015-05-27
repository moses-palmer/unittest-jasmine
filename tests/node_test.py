import subprocess
import unittest

import unittest_jasmine


class NodeTest(unittest.TestCase):
    def test_node_available(self):
        """Tests that node is available"""
        self.assertIsNotNone(unittest_jasmine.node.BINARY)

    def test_node_invocation(self):
        """Tests that node can be called"""
        stdout, stderr = unittest_jasmine.node.run(
            ['--eval', 'var a = "Hello"; console.log(a + " World")'],
            stdout=subprocess.PIPE).communicate()
        self.assertEqual(
            'Hello World',
            stdout.strip())
