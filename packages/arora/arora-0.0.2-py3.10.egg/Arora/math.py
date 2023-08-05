from typing import List, Tuple

import numpy as np
import statistics

import pandas as pd
from scipy import signal
from scipy.fftpack import fft
from scipy.stats import skew

from .core.EEG_freqbands import eeg_freq_bands


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


def fourier(epochized_data: List[int or float], sampling_freq: int or float) -> List[np.ndarray]:
	"""

	Args:
		epochized_data:
		sampling_freq:

	Returns:

	"""
	return_list = []
	T = 1 / sampling_freq
	for i in epochized_data:
		yf = fft(i)
		yf = np.array(yf)
		return_list.append(yf)
	return return_list


def welch_psd(epoch: pd.DataFrame, fs: int or float, filter_order: int)\
		-> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
	"""

	:param epoch: a segment of an edf signal in the form of a 1d array
	:param fs: the frequency of the epoch in the form of an integer
	:param filter_order: ???
	:return: ???
	"""
	# Acknowledgement: Katrín Hera, M.Sc
	delta_band, theta_band, alpha_band, beta_band = eeg_freq_bands(epoch, fs, filter_order)

	window_size = int((fs / 2) - 1)
	delta_nonbiased = delta_band - signal.savgol_filter(delta_band, window_size, filter_order)
	theta_nonbiased = theta_band - signal.savgol_filter(theta_band, window_size, filter_order)
	alpha_nonbiased = alpha_band - signal.savgol_filter(alpha_band, window_size, filter_order)
	beta_nonbiased = beta_band - signal.savgol_filter(beta_band, window_size, filter_order)
	F_AF3, delta_PSD = signal.welch(delta_nonbiased, fs / 2, nperseg=len(delta_nonbiased))
	F_AF3, theta_PSD = signal.welch(theta_nonbiased, fs / 2, nperseg=len(theta_nonbiased))
	F_AF3, alpha_PSD = signal.welch(alpha_nonbiased, fs / 2, nperseg=len(alpha_nonbiased))
	F_AF3, beta_PSD = signal.welch(beta_nonbiased, fs / 2, nperseg=len(beta_nonbiased))

	return delta_PSD, theta_PSD, alpha_PSD, beta_PSD
