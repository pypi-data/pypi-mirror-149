from typing import List

import pandas as pd


# TODO: change the actual code to my code
# TODO: comment
# TODO: pretty up the code through typing conventions
# TODO: UnitTests


def get_segment(index1: int, index2: int, signal: pd.DataFrame) -> List[int or float]:
	"""
	Args:
		index1: The start of the epoch
		index2: The end of the epoch
		signal: The data

	Returns: An array of segmented data
	"""
	signal_list = []

	for i in range(index2 - index1):
		# while index < len(signal)
		signal_list.append(signal[index1 + i])
	return signal_list
