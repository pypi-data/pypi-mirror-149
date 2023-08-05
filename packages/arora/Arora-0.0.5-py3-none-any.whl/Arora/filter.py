from scipy import signal
import numpy as np
from typing import List

"""
TODO: Make the code more readable and document/comment it
"""


def low_pass_filter(data: List[int or float], cutoff: int or float,
					frequency: int or float, order=5) -> np.ndarray:
	"""
	:param data: Array of integers or float
	:param cutoff: The frequency that is to be filtered through --> integer or float
	:param frequency: The frequency of the data --> integer or float
	:param order: The order of the filter --> integer
	:return: An array of filtered data using the Buttersworth method --> Numpy ndarray
	"""
	b, a = butter_pass(cutoff, frequency, btype='lowpass', order=order)
	y = signal.lfilter(b, a, data)
	return y


def high_pass_filter(data: List[int or float] or np.ndarray, cutoff: int or float,
					 frequency: int or float, order=5) -> np.ndarray:
	"""
	:param data: Array of integers or float
	:param cutoff: The frequency that is to be filtered through --> integer or float
	:param frequency: The frequency of the data --> integer or float
	:param order: The order of the filter --> integer
	:return: An array of filtered data using the Buttersworth method --> Numpy ndarray
	"""
	b, a = butter_pass(cutoff, frequency, btype='highpass', order=order)
	y = signal.filtfilt(b, a, data)
	return y


def butter_pass(cutoff: int or float, frequency: int or float,
				btype: str, order: int = 5) -> (np.ndarray, np.ndarray):
	"""

	:param cutoff: The frequency that is to be filtered through --> integer or float
	:param frequency: The frequency of the data --> integer or float
	:param order: The order of the filter --> integer
	:param btype: The type of filtering --> string
	:return: The denominator and the numerator polynomials of the IIR filter --> Numpy ndarray, numpy ndarray
	"""
	nyq = 0.5 * frequency
	normal_cutoff = cutoff / nyq
	b, a = signal.butter(order, normal_cutoff, btype=btype, analog=False)
	return b, a
