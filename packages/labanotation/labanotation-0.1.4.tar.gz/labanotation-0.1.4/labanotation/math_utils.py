from __future__ import division

import numpy as np
from pybsc import argclosest
from scipy import interpolate


def calc_velocity(timestamps, positions):
    """Calculate velocities

    Parameters
    ----------
    timestamps : numpy.ndarray
        (n,) timestapms.
    positions : numpy.ndarray
        (n,) or (n, dimensions)
    """
    n = len(timestamps)
    if n != len(positions):
        raise ValueError(
            'Inputs length are not same. '
            'len(timestamps)!=len(possitions)'
            '({}!={})'.format(len(timestamps), len(positions)))
    v = np.zeros(positions.shape)
    if positions.ndim == 1:
        v[1:] = (positions[1:] - positions[:-1]) \
            / (timestamps[1:] - timestamps[:-1])
    elif positions.ndim == 2:
        v[1:] = (positions[1:] - positions[:-1]) \
            / (timestamps[1:] - timestamps[:-1]).reshape(-1, 1)
    v[0] = v[1]
    return v


def calc_acceleration(timestamps, velocities):
    """Calculate acceleration from velocities

    Parameters
    ----------
    timestamps : numpy.ndarray
        (n,) timestapms.
    velocities : numpy.ndarray
        (n,) or (n, dimensions)
    """
    n = len(timestamps)
    if n != len(velocities):
        raise ValueError(
            'Inputs length are not same. '
            'len(timestamps)!=len(possitions)'
            '({}!={})'.format(len(timestamps), len(velocities)))
    acc = np.zeros(velocities.shape)
    if velocities.ndim == 1:
        acc[1:] = (velocities[1:] - velocities[:-1]) \
            / (timestamps[1:] - timestamps[:-1])
    elif velocities.ndim == 2:
        acc[1:] = (velocities[1:] - velocities[:-1]) \
            / (timestamps[1:] - timestamps[:-1]).reshape(-1, 1)
    acc[0] = acc[1]
    return acc


def der(y):
    y_der = np.diff(y, axis=0)
    y_der = np.concatenate([y_der, np.array([y_der[-1]])])
    return y_der


def inflection(y, thres_1=0.1**3, thres_2=0.1**3):
    y_dd = der(der(y))
    y_dd = 10.0 * y_dd / (max(y_dd) - min(y_dd))

    y_ddd = der(der(der(y)))
    y_ddd = 10.0 * y_ddd / (max(y_ddd) - min(y_ddd))

    infl = [0]
    # F_xx = 0 & F_xxx != 0
    for i in range(len(y_dd) - 1):
        if (y_dd[i] < 0 and y_dd[i + 1] >
                0) or (y_dd[i] > 0 and y_dd[i + 1] < 0):
            if abs(y_ddd[i]) > 0.1:
                if abs(y_dd[i] < y_dd[i + 1]):
                    infl.append(i)
                else:
                    infl.append(i + 1)
    infl.append(len(y_dd) - 1)

    return infl


def min_max_normalize(x):
    max_value = np.max(x, axis=0, keepdims=True)
    min_value = np.min(x, axis=0, keepdims=True)
    return (x - min_value) / (max_value - min_value)


def resample(positions, timestamps, rate=30):
    positions = np.array(positions, dtype=np.float64)
    timestamps = np.array(timestamps, dtype=np.float64)
    start_time = timestamps[0]
    timestamps = timestamps - start_time
    first_stamp = timestamps[0]
    last_stamp = timestamps[-1]
    n_sample = int(last_stamp * rate + 1)
    sampled_timestamps = np.linspace(first_stamp, last_stamp, num=n_sample)
    interpolated_f = interpolate.interp1d(
        timestamps, positions, kind='linear', axis=0)
    sampled_positions = interpolated_f(sampled_timestamps)
    return sampled_positions, sampled_timestamps + start_time


def sampled_indices_to_indices(
        sampled_indices,
        sampled_timestamps,
        timestamps):
    """Convert sampled indices to not sampled indices.

    Examples
    --------
    >>> sampled_indices_to_indices([1, 3],
    [0.0, 0.1, 0.2, 0.3, 0.4], [0.0, 0.2, 0.4])
    array([1, 1])
    """
    timestamps = np.array(timestamps, dtype=np.float64)
    timestamps = timestamps - timestamps[0]
    sampled_timestamps = np.array(sampled_timestamps, dtype=np.float64)
    sampled_timestamps = sampled_timestamps - sampled_timestamps[0]
    target_timestamps = sampled_timestamps[sampled_indices]
    indices = argclosest(timestamps, target_timestamps)
    return np.array(indices, dtype=np.int64)


def calc_geodesic_ang_speed(angles):
    """Calculate geodesic and speed.

    t: theta, p: phi
    dt:theta', dp: phi'
    v = sqrt[(p' * sint)^2+(t')^2]
    """
    n = len(angles)
    v = np.zeros(n)

    thetas = np.array([angles[i][1] for i in range(n)])
    phis = np.array([angles[i][2] for i in range(n)])
    # generate parameters
    dt = [thetas[i + 1] - thetas[i] for i in range(0, n - 1)]
    dt.append(dt[-1])
    dp = [phis[i + 1] - phis[i] for i in range(0, n - 1)]
    dp.append(dp[-1])

    for i in range(n):
        v_1 = dp[i] * np.sin(thetas[i])
        v_2 = dt[i]
        v[i] = np.sqrt(v_1**2 + v_2**2)
    return v
