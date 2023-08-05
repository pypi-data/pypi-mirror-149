import pandas as pd
from numpy import ndarray

from . import bandpass


def eeg_freq_bands(eeg_signal: pd.DataFrame, sampling_freq: float or int,
                   filter_order: float or int) -> (ndarray, ndarray, ndarray, ndarray):
    """

    Args:
        eeg_signal: One type of signal from the edf file
        sampling_freq: The sampling frequency of the eeg signal
        filter_order:

    Returns: Four arrays that contain each bandpass of the most common frequencies

    """
    alpha_lower = 8
    alpha_upper = 14
    beta_lower = 14
    beta_upper = 50
    delta_lower = 0.5
    delta_upper = 4
    theta_lower = 4
    theta_upper = 8
    delta_band = bandpass(eeg_signal, delta_lower, delta_upper, sampling_freq, filter_order)
    theta_band = bandpass(eeg_signal, theta_lower, theta_upper, sampling_freq, filter_order)
    alpha_band = bandpass(eeg_signal, alpha_lower, alpha_upper, sampling_freq, filter_order)
    beta_band = bandpass(eeg_signal, beta_lower, beta_upper, sampling_freq, filter_order)
    return delta_band, theta_band, alpha_band, beta_band
