import pandas as pd
import numpy as np
import typing as Tuple
from scipy import signal
from arora.filter.EEG_freqbands import eeg_freq_bands

def welch_psd(epoch: pd.DataFrame, fs: int or float, filter_order: int) \
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
