from typing import List
import pandas as pd
from scipy.io import loadmat


def load_mat(file: str) -> (List[int, float], pd.DataFrame):
	# If mat files all have the same format then hardcode how to insert the code into the dataframe and signal list
	data = loadmat(file)

	return