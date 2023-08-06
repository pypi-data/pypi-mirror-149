from scipy import signal
import numpy as np
from typing import List

"""
TODO: Make the code more readable and document/comment it
"""


def standardize(epoch: List[int or float]):
	"""
	Matias gave us this code
	Z-score normalization for the signals.
	Args:
		epoch: An epoch of some signal
	Returns:
	"""
	return (epoch - np.mean(epoch)) / np.std(epoch)


def low_pass_filter(
		data: List[int or float],
		cutoff: int or float,
		frequency: int or float = 200,
		order=5) -> np.ndarray:
	"""
	:param data: Array of integers or float
	:param cutoff: The frequency that is to be filtered through --> integer or float
	:param frequency: The frequency of the data --> integer or float
	:param order: The order of the filter --> integer
	:return: An array of filtered data using the Buttersworth method --> Numpy ndarray
	"""
	b, a = _butter_pass(cutoff, frequency, btype='lowpass', order=order)
	y = signal.lfilter(b, a, data)
	return y


def cheby2_highpass_filtfilt(
		signals,
		fs,
		cutoff,
		order=5,
		rs=40.0):
	"""
	Chebyshev type1 highpass filtering.
	Matias gave us this code
	Args:
		signals: the signals
		fs: sampling freq in Hz
		cutoff: cutoff freq in Hz
		order:
		rs:
	Returns:
		the filtered signals
	"""
	nyq = 0.5 * fs
	norm_cutoff = cutoff / nyq
	sos = signal.cheby2(order, rs, norm_cutoff, btype='highpass', output='sos')
	return signal.sosfiltfilt(sos, signals)


def high_pass_filter(
		data: List[int or float] or np.ndarray,
		cutoff: int or float,
		frequency: int or float = 200,
		order=5) -> np.ndarray:
	"""
	Args:
		data: Array of integers or float
		cutoff: The frequency that is to be filtered through --> integer or float
		frequency: The frequency of the data --> integer or float
		order: The order of the filter --> integer

	Returns: An array of filtered data using the Buttersworth method --> Numpy ndarray
	"""
	b, a = _butter_pass(cutoff, frequency, btype='highpass', order=order)
	y = signal.filtfilt(b, a, data)
	return y


def _butter_pass(
		cutoff: int or float,
		frequency: int or float,
		btype: str,
		order: int = 5) -> (np.ndarray, np.ndarray):
	"""
	Args:
		cutoff: The frequency that is to be filtered through --> integer or float
		frequency: The frequency of the data --> integer or float
		btype: The order of the filter --> integer
		order: The type of filtering --> string
	Returns:The denominator and the numerator polynomials of the IIR filter --> Numpy ndarray, numpy ndarray
	"""
	nyq = 0.5 * frequency
	normal_cutoff = cutoff / nyq
	b, a = signal.butter(order, normal_cutoff, btype=btype, analog=False)
	return b, a
