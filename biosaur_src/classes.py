import numpy as np


def meanfilt(data, window_width):
    cumsum_vec = np.cumsum(np.insert(data, 0, 0))
    ma_vec = (cumsum_vec[window_width:] -
              cumsum_vec[:-window_width]) / window_width
    ma_vec = data[:1] + list(ma_vec) + data[-1:]
    return ma_vec
