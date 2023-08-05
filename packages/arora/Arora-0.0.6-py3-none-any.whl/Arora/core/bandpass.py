import numpy as np
import pandas as pd
import scipy
from scipy import signal

"""
This is a work in a WIP and will be changed, at the moment is butter returned too many values so 
this will be needed to change
"""


def bandpass(raw_signal: pd.DataFrame, lower_cutoff: int or float,
             upper_cutoff: int or float, sampling_freq: int or float, filter_order: int) -> np.ndarray:
    """

    Args:
        raw_signal: The EEG signal that is to be processed -> an array of float/integers value
        lower_cutoff: The lower frequency value -> a float or an integer
        upper_cutoff: The upper frequency value -> a float or an integer
        sampling_freq: The frequency of the raw_signal -> a float or an integer
        filter_order: The maximum number of delay elements used in the filter circuit -> an integer value

    Returns: A filtered array

    """

    w1 = lower_cutoff / (sampling_freq / 2) # Normalize the frequencies
    w2 = upper_cutoff / (sampling_freq / 2)

    # w1 = lower_cutoff / sampling_freq
    # w2 = upper_cutoff / sampling_freq
    b, a, x = signal.butter(filter_order, [w1, w2], btype='bandpass', output='ba') #make filter
    output_band = scipy.signal.lfilter(b, a, raw_signal)
    return output_band
