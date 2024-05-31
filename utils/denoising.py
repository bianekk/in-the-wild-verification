import numpy as np
from scipy.signal import butter, sosfilt


def filter_butter(
    signal_arr: np.ndarray,
    fs: float,
    filter_order: int = 2,
    critical_freq: float = 1000.0,
) -> np.ndarray:
    """Filters noise in signal using Butterworth lowpass filter

    Args:
        signal_arr: 1D array containing raw signal values
        fs: sampling frequency of the signal (frame rate)
        filter_order: the order of the filter argument passed to scipy `butter`
        critical_freq: critical frequency for the filter

    Returns:
        1D array: filtered signal

    """
    sos = butter(filter_order, critical_freq, fs=fs, output="sos")
    return sosfilt(sos, signal_arr)
