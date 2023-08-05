import pandas as pd
import pyedflib as edf
from typing import List


def get_edf(file) -> (List[float], pd.DataFrame):
	"""

	:param file: The edf file to be read
	:return: An array of all the signals and a DataFrame with information about the signals
	"""

	# Read the file and return the signals, data about the signal and data about the file
	signals, signal_headers, header = edf.highlevel.read_edf(file)

	# Turn the signal headers into a DataFrame
	signal_headersdf = pd.DataFrame(data=signal_headers)

	return signals, signal_headersdf


# if __name__ == "__main__":
# 	file = "C:\Haskoli\YearThree\Spring\LOKA\arora\src\ma0844az_1-1+.edf"
# 	get_edf(file)