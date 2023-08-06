from random import random
from typing import List
import numpy as np
from scipy import signal


def segment_fs(signals: List[float or int], fs: int) -> List[List[int or float]]:
	"""

	Args:
		signals:
		fs:

	Returns:

	"""
	# Maybe have this in a separate file for everyone to use
	return [signals[x:x + fs] for x in range(0, len(signals), fs)]


def resample(signals: List[int or float], newfs: int, oldfs: int):
	"""
	Matias gave us the base of this code
	Args:
		signals:
		newfs:
		oldfs:

	Returns:

	"""
	return signal.resample(signals, int((newfs/oldfs)*len(signals)))


def lower_frequency(signals: List[float or int], method: str, new_fs: int) -> List[float or int]:
	"""
	Lowers the frequency of the given signals by some given method
	Args:
		signals: List of time series signals
		method: The method how the frequency should be lowered
		new_fs: The new frequency of the signals

	Returns: List of new values corresponding to the method given

	"""
	new_signal = []
	segmented_signal = segment_fs(signals, new_fs)
	if method.lower() == 'min':
		for index in range(0, len(segmented_signal)):
			the_lowest = min(segmented_signal[index])
			new_signal.append(the_lowest)

	elif method.lower() == 'max':
		for index in range(0, len(segmented_signal)):
			the_lowest = max(segmented_signal[index])
			new_signal.append(the_lowest)

	elif method.lower() == 'mean':
		for index in range(0, len(segmented_signal)):
			the_lowest = np.mean(segmented_signal[index])
			new_signal.append(the_lowest)

	elif method.lower() == 'median':
		for index in range(0, len(segmented_signal)):
			the_lowest = np.median(segmented_signal[index])
			new_signal.append(the_lowest)

	return new_signal
