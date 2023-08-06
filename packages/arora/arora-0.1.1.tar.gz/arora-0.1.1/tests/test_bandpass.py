import unittest
from random import random

import numpy as np

from arora import bandpass


class TestBandpass(unittest.TestCase):

    def test_bandpass(self):
        r = 1000
        inp = [random() for _ in range(r)]
        lower = 99
        upper = 1
        fs = 200
        out = bandpass(inp, lower, upper, fs, 5)
        self.assertEqual(len(out), r)
        self.assertEqual(type(out), np.ndarray)


if __name__ == '__main__':
    unittest.main()
