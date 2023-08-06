from collections import defaultdict
from typing import List
from typing import Union

import numpy as np
from scipy import signal

from labanotation.cluster import b_peak_dect
from labanotation.filter import apply_gaussian_filter
from labanotation.k4a_kinematics import keypoint_names
from labanotation.labanotation_utils import (
    calculate_unfiltered_labanotations_smart
)
from labanotation.labanotation_utils import append_edge_indices
from labanotation.labanotation_utils import arrange_labanotations
from labanotation.labanotation_utils import calculate_z_axis
from labanotation.labanotation_utils import extract_target_labanotations
from labanotation.labanotation_utils import segmentation_from_labanotations
from labanotation.math_utils import calc_acceleration
from labanotation.math_utils import calc_geodesic_ang_speed
from labanotation.math_utils import calc_velocity
from labanotation.math_utils import inflection
from labanotation.math_utils import min_max_normalize
from labanotation.math_utils import resample


def _detect_peak(x, order=3, max=False):
    """Detect peak

    """
    if max:
        indices = signal.argrelmax(x, order=order)[0]
    else:
        indices = signal.argrelmin(x, order=order)[0]
    return indices


def detect_min_peak(x, order=3):
    return _detect_peak(x, order=order, max=False)


def detect_max_peak(x, order=3):
    return _detect_peak(x, order=order, max=True)


def energy_function(velocities, accelerations, normalize=True,
                    velocity_only=False):
    if len(velocities) != len(accelerations):
        raise ValueError
    ev = np.sqrt(np.sum(velocities ** 2, axis=1)) / 3.0
    ea = np.sqrt(np.sum(accelerations ** 2, axis=1)) / 3.0
    if normalize is True:
        ea = min_max_normalize(ea)
        ev = min_max_normalize(ev)
    if velocity_only:
        total_energy = ev
    else:
        total_energy = ea - ev
    return total_energy


def total_energy(timestamps, positions, gauss_window_size=31, gauss_sigma=5,
                 normalize=True,
                 append_edge=True,
                 velocity_only=False):
    """Apply total energy algoritm

    Apply total energy algoritm to joint data frames
    and calculate labanotation.
    If you want to calculate naive energy, please set gauss_sigma=1.

    Parameters
    ----------
    timestamps : numpy.ndarray
        time stamps
    positions : numpy.ndarray
        positions (n, dimensions)
    """
    filtered_positions = apply_gaussian_filter(
        positions, window_size=gauss_window_size, sigma=gauss_sigma)
    velocities = calc_velocity(timestamps, filtered_positions)
    accelerations = calc_acceleration(timestamps, velocities)
    energy = energy_function(velocities, accelerations,
                             normalize=normalize,
                             velocity_only=velocity_only)

    peak_indices = detect_max_peak(energy)
    if append_edge:
        peak_indices = append_edge_indices(
            peak_indices, len(timestamps) - 1)
    return peak_indices, energy, velocities, accelerations


def parallel_energy_impl(labanotations: List[List[str]],
                         positions: np.ndarray,
                         gauss_window_size: int = 31,
                         gauss_large_sigma: int = 3,
                         gauss_small_sigma: int = 1) -> List[int]:
    sect = segmentation_from_labanotations(labanotations)
    v_tmp = calc_geodesic_ang_speed(positions)

    energy = apply_gaussian_filter(
        v_tmp, window_size=gauss_window_size, sigma=gauss_large_sigma)

    naive_energy = apply_gaussian_filter(
        v_tmp, window_size=gauss_window_size, sigma=gauss_small_sigma)

    # v_max = max(energy.max(), naive_energy.max())

    corner = b_peak_dect(energy, sect)
    infl = inflection(energy)

    # search the minimum point along the narrow gaussian within the boundary
    # defined by the inflection pairs correspondng the the
    # minimum point of the wider gaussian
    real_corner = []
    for j in corner:
        right = 0
        left = 0
        for k in range(len(infl)):
            if infl[k] > j:
                left = infl[k - 1]
                right = infl[k]
                break
        min_val = naive_energy[left]
        min_ptr = left
        for k in range(left, right + 1):
            if naive_energy[k] < min_val:
                min_val = naive_energy[k]
                min_ptr = k
        real_corner.append(min_ptr)
    return real_corner, energy, naive_energy


def parallel_energy(
        labanotations_list: List[List[str]],
        positions_list: np.ndarray,
        gauss_window_size: int = 31,
        gauss_large_sigma: int = 3,
        gauss_small_sigma: int = 1):
    """Parallel energy method.

    """
    # n_limbs = len(labanotations_list)
    valley_output = []
    energy_list = []
    naive_energy_list = []
    for labans, positions in zip(labanotations_list,
                                 positions_list):
        real_corner, energy, naive_energy = parallel_energy_impl(
            labans, positions,
            gauss_window_size=gauss_window_size,
            gauss_large_sigma=gauss_large_sigma,
            gauss_small_sigma=gauss_small_sigma)
        valley_output.append(real_corner)
        energy_list.append(energy)
        naive_energy_list.append(naive_energy)

    keyframe_indices = merge_keyframe_indices(
        valley_output,
        n=len(labanotations_list[0]),
        thres_dis=9)
    return keyframe_indices, valley_output, energy_list, naive_energy_list


def extract_keyframe_labanotations(timestamps, labanotations, indices):
    if len(timestamps) != len(labanotations):
        raise ValueError
    indices = append_edge_indices(indices, len(timestamps) - 1)
    keyframe_timestamps = [timestamps[i] for i in indices]
    keyframe_labanotations = [labanotations[i] for i in indices]
    return keyframe_timestamps, keyframe_labanotations


def calculate_section_timestamps(
        joint_positions_list: Union[List[List[float]], np.ndarray],
        timestamps: Union[List[float], np.ndarray],
        gauss_window_size: int = 61,
        gauss_sigma: int = 5,
        limb_type: str = 'hand_right',
        method: str = 'parallel',
        velocity_only=False) -> List[List[float]]:
    joint_positions_dict = defaultdict(list)
    for i, name in enumerate(keypoint_names):
        for j in joint_positions_list:
            joint_positions_dict[name].append(j[i])
        joint_positions_dict[name], sampled_timestamps = resample(
            np.array(joint_positions_dict[name]),
            timestamps)

    if method == 'parallel':
        z_axis = calculate_z_axis(joint_positions_dict['shoulder_left'],
                                  joint_positions_dict['shoulder_right'],
                                  joint_positions_dict['spine_navel'],)
        laban_data = calculate_unfiltered_labanotations_smart(
            joint_positions_dict,
            base_rotation_style='first',
            z_axis=z_axis)

        if limb_type == 'parallel':
            labanotations_list = [laban_data.elbow_right.laban,
                                  laban_data.wrist_right.laban,
                                  laban_data.elbow_left.laban,
                                  laban_data.wrist_left.laban]
            positions_list = [laban_data.elbow_right.spherical,
                              laban_data.wrist_right.spherical,
                              laban_data.elbow_left.spherical,
                              laban_data.wrist_left.spherical]
        elif limb_type == 'hand_right':
            labanotations_list = [laban_data.elbow_right.laban,
                                  laban_data.wrist_right.laban]
            positions_list = [laban_data.elbow_right.spherical,
                              laban_data.wrist_right.spherical]
        elif limb_type == 'hand_left':
            labanotations_list = [laban_data.elbow_left.laban,
                                  laban_data.wrist_left.laban]
            positions_list = [laban_data.elbow_left.spherical,
                              laban_data.wrist_left.spherical]
        else:
            raise RuntimeError

        keyframe_indices, valley_output, energy, naive_energy_list = \
            parallel_energy(
                labanotations_list, positions_list,
                gauss_window_size=gauss_window_size,
                gauss_large_sigma=gauss_sigma)
        all_labans = arrange_labanotations(labanotations_list)
        keyframe_indices, labans = extract_target_labanotations(
            keyframe_indices, all_labans)

        frame_to_second = (sampled_timestamps[-1] - sampled_timestamps[0]) \
            / len(all_labans)
    elif method == 'total':
        if limb_type == 'hand_right':
            positions = joint_positions_dict['wrist_right']
        elif limb_type == 'hand_left':
            positions = joint_positions_dict['wrist_left']
        else:
            raise RuntimeError

        keyframe_indices, energy, _, _ = total_energy(
            sampled_timestamps,
            positions,
            gauss_window_size=gauss_window_size,
            gauss_sigma=gauss_sigma,
            velocity_only=velocity_only)
        frame_to_second = (sampled_timestamps[-1] - sampled_timestamps[0]) \
            / len(positions)

    keyframe_timestamps = frame_to_second * keyframe_indices
    section_timestamps = [
        [float(a), float(b)]
        for a, b in zip(keyframe_timestamps[:-1], keyframe_timestamps[1:])]
    return section_timestamps, energy, sampled_timestamps, \
        keyframe_timestamps, keyframe_indices


def merge_keyframe_indices(keyframe_indices_list, n, thres_dis=9):
    n_limbs = len(keyframe_indices_list)

    indices = []
    ptr = 0

    center = np.zeros(n, dtype=np.int32)
    for i in range(n_limbs):
        for j in keyframe_indices_list[i]:
            center[j] += 1

    while ptr < n:
        tmp = center[ptr]
        if tmp > 0:
            indices.append(ptr)
            ptr += thres_dis
        else:
            ptr += 1

    new_indices = []
    keyframe_indices_list_new = []
    for i in keyframe_indices_list:
        tmp = []
        for j in i:
            tmp.append(j)
        keyframe_indices_list_new.append(tmp)

    for i in range(len(indices)):
        left = indices[i]
        right = indices[i] + thres_dis
        group = []
        for j in range(n_limbs):
            ptr = 0
            while ptr < len(keyframe_indices_list_new[j]):
                tmp = keyframe_indices_list_new[j][ptr]
                if left <= tmp <= right:
                    group.append(tmp)
                    del keyframe_indices_list_new[j][ptr]
                ptr += 1
        if len(group) == 0:
            continue
        # kf = sum(group)/len(group)
        # the first key frame, use the first potential frame in its group
        if i == 0:
            group.sort()
            kf = group[0]
        # the last key frame, use the last potential frame in its group
        elif i == len(indices) - 1:
            group.sort()
            kf = group[-1]
        else:
            kf = sum(group) // len(group)
        new_indices.append(kf)

    keyframe_indices = sorted(set(new_indices))
    keyframe_indices = np.array(keyframe_indices, dtype=np.int64)
    return keyframe_indices
