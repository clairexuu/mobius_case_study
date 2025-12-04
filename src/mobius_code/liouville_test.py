import ctypes
import os
import unittest


dldlib = ctypes.CDLL(os.path.abspath('liouville.so'))
dldliouville = dldlib.liouville
dldliouville.argtypes = [ctypes.c_longlong]


class TestLiouville(unittest.TestCase):
    def test_liouville_small(self):
        self.assertEqual(dldliouville(0), 0)

        self.assertEqual(dldliouville(1), 1)

        self.assertEqual(dldliouville(2), -1)
        self.assertEqual(dldliouville(3), -1)
        self.assertEqual(dldliouville(5), -1)
        self.assertEqual(dldliouville(7), -1)

        self.assertEqual(dldliouville(4), 1)
        self.assertEqual(dldliouville(9), 1)
        self.assertEqual(dldliouville(6), 1)
        self.assertEqual(dldliouville(10), 1)

        self.assertEqual(dldliouville(8), -1)
        self.assertEqual(dldliouville(12), -1)

    def test_liouville_large(self):
        self.assertEqual(dldliouville(7*11*13), -1)
        self.assertEqual(dldliouville(2*3*5*7*11), -1)
        self.assertEqual(dldliouville(2*3*5*7*11*11), 1)
        self.assertEqual(dldliouville(2*3*5*7*11*13), 1)
