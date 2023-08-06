import unittest
from random import random

import numpy as np

from arora import low_pass_filter, high_pass_filter


class TestFiltering(unittest.TestCase):

    def test_low_pass_filter(self):
        r = 1000
        fs = 200
        cutoff = 99
        inp = [random() for _ in range(r)]
        out = low_pass_filter(inp, cutoff, fs)
        self.assertEqual(len(out), r)
        self.assertNotEqual(inp, list(out))
        self.assertEqual(type(out), np.ndarray)

    def test_high_pass_filter(self):
        r = 1000
        fs = 200
        cutoff = 50
        inp = [random() for _ in range(r)]
        out = high_pass_filter(inp, cutoff, fs)
        self.assertEqual(len(out), r)
        self.assertNotEqual(inp, list(out))
        self.assertEqual(type(out), np.ndarray)


if __name__ == '__main__':
    unittest.main()
