import numpy as np
from scipy.ndimage import gaussian_filter1d


def apply_gaussian_filter(data: np.ndarray,
                          window_size: int = 5, sigma: float = 3.0):
    truncate = (((window_size - 1) // 2) - 0.5) / sigma
    return gaussian_filter1d(data,
                             sigma=sigma,
                             axis=0,
                             mode='nearest', truncate=truncate)
