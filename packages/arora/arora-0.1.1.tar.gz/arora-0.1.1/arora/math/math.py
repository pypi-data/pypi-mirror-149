from typing import List

import numpy as np
import statistics


def iqr_standardize(signals: List[int or float], lowerquantile: int, upperquantile: int):
	"""
	IQR standardization for the signals.
	Args:
		signals:
		lowerquantile:
		upperquantile:

	Returns:

	"""
	upperq, lowerq = np.percentile(signals, [upperquantile, lowerquantile])
	iqr = upperq - lowerq
	return (signals - np.median(signals)) / iqr


def mean_val(signal_list: List[int or float]) -> float or int:
	"""
	Function that find the mean of a give array

	:param signal_list: a 1d array of edf signals
	:return: The mean of the array
	"""
	length = len(signal_list)
	if length == 0:
		return 0.0

	return float(sum(signal_list) / length)


def std_val(signal_list: List[int or float]) -> float:
	"""
	Function that finds the given standard deviation of a given array

	:param signal_list:  a 1d array of edf signals
	:return: The standard deviation of the array
	"""
	if len(signal_list) < 2:
		raise Exception("Your array must contain at least two values")
	return statistics.stdev(signal_list)
