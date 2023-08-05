import numpy as np
import pandas as pd

from Arora import math
from . import upper_lower_signal_envelopes


def find_features(epochized_signal: pd.DataFrame, sampling_freq: int or float,
                  filter_order: int) -> pd.DataFrame:
    """
    Args:
        epochized_signal: The segmented EEG data -> A DataFrame
        sampling_freq: The sampling frequency of the epochized signal -> an integer or a float
        filter_order: What the filter order should be -> integer

    Returns: A DataFrame that contains the main features of the signal

    """

    l = len(epochized_signal)
    mini = []
    maxi = []
    med = []
    upper_mean = []
    lower_mean = []
    upper_std = []
    lower_std = []
    upper_var = []
    lower_var = []
    PSD = []

    for i in range(0, l):
        mini.append(np.min(epochized_signal[i]))
        maxi.append(np.max(epochized_signal[i]))
        med.append(np.median(epochized_signal[i]))

        upper, lower = upper_lower_signal_envelopes(epochized_signal[i])
        upper_mean.append(np.mean(upper))
        lower_mean.append(np.mean(lower))
        upper_std.append(np.std(upper))
        lower_std.append(np.std(lower))
        upper_var.append(np.var(upper))
        lower_var.append(np.var(lower))

        PSDlist = math.welch_psd(epochized_signal[i], sampling_freq, filter_order)
        PSD.append(PSDlist)

    dataframe = epochized_signal

    dataframe['Epoch min'] = mini
    dataframe['Epoch max'] = maxi
    dataframe['Epoch median'] = med
    dataframe['Upper env mean'] = upper_mean
    dataframe['Lower env mean'] = lower_mean
    dataframe['Upper env std'] = upper_std
    dataframe['Lower env std'] = lower_std
    dataframe['Upper env var'] = upper_var
    dataframe['Lower env var'] = lower_var
    dataframe['PSD'] = PSD

    return dataframe
