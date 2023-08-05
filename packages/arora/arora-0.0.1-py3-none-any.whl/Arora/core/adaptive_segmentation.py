from typing import Union, List
import numpy as np

"""
TODO: Implement the functions and add them to the adaptive segmentations function
TODO: Document and comment the functions
TODO: Move find_transients function to some other file
"""

def _signal_afc(N: Union[int, float], i: Union[int, float],
				signals: Union[List[Union[int, float]], np.ndarray]):
	R_sum = 0

	for n in range(1, N - i):
		R_sum += signals[n] * signals[n + i]

	R_sum = R_sum * (1 / N)

	return R_sum


def _lp_filter_creation():
	return None


def _est_signal_value(signal, p, a, n):
	the_sum = 0
	for index in range(1, p):
		# TODO: check if the n is smaller than p and make some error handling for that, this should be able to go back in time
		the_sum += a[index] * signal[n - index]
	return -1 * the_sum

def error_of_signal():




def _calculate_pe_val():
	return None


def _calculate_pe_acf():
	return None


def _calculate_sem():
	return None


def find_transients(hello):
	# This is part of the feature extraction process
	return None

def adaptive_segmentation(signals: Union[List[Union[int, float]], np.ndarray]):
	"""

	:param signals:
	:return:
	"""
	# Store segment length - Store both the onset and the duration
	# Store signal predictor
	# Store corrective predictor
	N = None or 10 # maybe 50?
	i = None or 666 or 56

	# Step 1:
	# 	a. Compute new signal ACF
	_signal_afc(N, i, signals)

	# 	b. adapt LP filter
	# Step 2:

	return None