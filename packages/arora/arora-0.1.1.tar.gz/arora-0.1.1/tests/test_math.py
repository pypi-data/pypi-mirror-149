import unittest
from random import random
import numpy as np

from arora import mean_val, std_val, iqr_standardize


class TestMath(unittest.TestCase):

    def test_mean_val_empty(self):
        # Testing empty list
        signal_list = []
        try:
            out = mean_val(signal_list)
            self.assertIs(type(out), float)
            self.assertEqual(out, 0.0)
        except ZeroDivisionError:
            self.assertFalse(False, "Does not raise zero division error")

    def test_mean_val_zero(self):
        # Testing zero values
        signal_list = [0.0, 0.0, 0.0]
        out = mean_val(signal_list)
        self.assertIs(type(out), float, "Output is float")
        self.assertEqual(out, 0.0, "Mean value is 0.0")

    def test_mean_val_int(self):
        # Testing int values
        signal_list = [1, 2, 3]
        out = mean_val(signal_list)
        self.assertIs(type(out), float, "Output is float")
        self.assertEqual(out, 2.0, "Mean value is 2.0")

    def test_mean_val_float(self):
        # Testing float values
        signal_list = [1.0, 2.0, 3.0]
        out = mean_val(signal_list)
        self.assertEqual(out, 2.0, "Mean value is 2.0")

    def test_mean_val_mixed(self):
        # Testing mixed values
        signal_list = [1, 2, 3.0]
        out = mean_val(signal_list)
        self.assertIs(type(out), float, "Output is float")
        self.assertEqual(out, 2.0, "Mean value is 2.0")

    def test_mean_val_non_empty(self):
        # Testing non even result
        signal_list = [2.0, 3.0, 8.0, 10.0]
        out = mean_val(signal_list)
        self.assertIs(type(out), float, "Output is float")
        self.assertEqual(out, 5.75, "Mean value is 5.75")

    def test_std_val_empty(self):
        # Testing empty lists
        empty_signal_list = []
        empty_signal_list1 = [1]
        with self.assertRaises(Exception) as cx:
            std_val(empty_signal_list)
            self.assertTrue("Your array must contain at least two values" in cx.exception)
            std_val(empty_signal_list1)
            self.assertTrue("Your array must contain at least two values" in cx.exception)

    def test_std_val_int(self):
        # Testing int values
        signal_list = [1, 2, 3]
        out = std_val(signal_list)
        self.assertIs(type(out), float, "Output is float")
        self.assertEqual(out, 1.0, "Std. is 1")

    def test_std_val_float(self):
        # Testing float values
        signal_list = [3.0, 2.0, 5.0]
        out = std_val(signal_list)
        self.assertIs(type(out), float, "Output is float")
        self.assertEqual(round(out, 3), 1.528, "Std. is 1.528")

    def test_std_val_mixed(self):
        # Testing mixed values
        signal_list = [1, 2.0, 5.0]
        out = std_val(signal_list)
        self.assertIs(type(out), float, "Output is float")
        self.assertEqual(round(out, 3), 2.082, "Std. is 2.082")

    def test_standardize(self):
        lower = 25
        upper = 75
        r = 1000
        inp = [round(random() * 100, 1) for _ in range(r)]
        out = iqr_standardize(inp, lower, upper)
        self.assertEqual(len(out), r)
        self.assertNotEqual(inp, list(out))

    def test_standardize_zero(self):
        lower = 0
        upper = 25
        r = 100
        inp = [round(random() * 100, 1) for _ in range(r)]
        out = iqr_standardize(inp, lower, upper)
        self.assertEqual(len(out), r)
        self.assertNotEqual(inp, list(out))


if __name__ == "__main__":
    tm = TestMath()
