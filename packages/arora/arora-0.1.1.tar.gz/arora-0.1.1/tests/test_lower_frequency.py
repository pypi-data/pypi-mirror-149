import unittest
from random import random
from numpy import mean, median, ceil

from arora import lower_frequency


class MyTestCase(unittest.TestCase):

    def test_lower_min(self):
        r = 1000
        fs = 100
        inp = [round(random()*100, 1) for _ in range(r)]
        out = lower_frequency(inp, method='min', new_fs=fs)
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), r / fs)
        self.assertEqual(min(inp[0:fs]), out[0])
        self.assertEqual(min(inp[-fs:]), out[-1])

    def test_lower_max(self):
        r = 1000
        fs = 100
        inp = [round(random() * 100, 1) for _ in range(r)]
        out = lower_frequency(inp, method='max', new_fs=fs)
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), r / fs)
        self.assertEqual(max(inp[:fs]), out[0])
        self.assertEqual(max(inp[fs * 2:fs * 3]), out[2])

    def test_lower_mean(self):
        r = 1000
        fs = 100
        inp = [round(random() * 100, 1) for _ in range(r)]
        out = lower_frequency(inp, method='mean', new_fs=fs)
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), r / fs)
        self.assertEqual(mean(inp[fs * 2:fs * 3]), out[2])
        self.assertEqual(mean(inp[fs * 4:fs * 5]), out[4])

    def test_lower_median(self):
        r = 1000
        fs = 100
        inp = [round(random() * 100, 1) for _ in range(r)]
        out = lower_frequency(inp, method='median', new_fs=fs)
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), r / fs)
        self.assertEqual(median(inp[fs * 3:fs * 4]), out[3])
        self.assertEqual(median(inp[fs * 6:fs * 7]), out[6])

    def test_not_complete_list(self):
        r = 1000
        fs = 70
        inp = [round(random() * 100, 1) for _ in range(r)]
        out = lower_frequency(inp, method='min', new_fs=fs)
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), ceil(r / fs))
        cutoff = (r // fs) * fs
        self.assertEqual(min(inp[cutoff:]), out[-1])
        self.assertEqual(min(inp[fs * 6:fs * 7]), out[6])


if __name__ == '__main__':
    unittest.main()
