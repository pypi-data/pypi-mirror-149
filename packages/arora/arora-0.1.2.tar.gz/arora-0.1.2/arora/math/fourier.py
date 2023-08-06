from typing import List
import numpy as np
from scipy.fft import fft


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
