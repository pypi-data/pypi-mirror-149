from __future__ import division

from collections import Counter

import numpy as np
from skrobot.coordinates.math import rotation_matrix_from_axis

from labanotation.k4a_kinematics import (
    normalize_keypoint_names_to_indices as k4a_kp_name_to_indices
)
from labanotation.kinematics import normalize_keypoint_names_to_indices


def most_frequent_pid(results_poses):
    """Return most frequent pid from results_poses.

    """
    pids = []
    for results in results_poses:
        for res in results:
            pid = res['pid']
            pids.append(pid)
    cnt = Counter(pids)
    return cnt.most_common()


def extract_target_pid_indices(results_poses, pid):
    n_frame = len(results_poses)
    start_index = None
    for i in range(n_frame):
        results = results_poses[i]
        for res in results:
            if pid == res['pid']:
                start_index = i
                break
        if start_index is not None:
            break
    if start_index is None:
        return None

    end_index = None
    for i in range(n_frame - 1, -1, -1):
        results = results_poses[i]
        for res in results:
            if pid == res['pid']:
                end_index = i + 1
                break
        if end_index:
            break
    return range(start_index, end_index)


def extract_most_frequent_pid_indices(results_poses):
    cnt = most_frequent_pid(results_poses)
    if len(cnt) == 0:
        raise ValueError
    pid = cnt[0][0]
    return pid, extract_target_pid_indices(results_poses, pid)


def extract_target_joint_positions(
        results_poses, pid, joint_id, dataset='k4a',
        key='keypoints',
        timestamps=None):
    if dataset == 'coco':
        joint_index = normalize_keypoint_names_to_indices(
            joint_id)
    elif dataset == 'k4a':
        joint_index = k4a_kp_name_to_indices(
            joint_id)
    else:
        raise NotImplementedError
    joint_positions = []
    indices = []
    for i, results in enumerate(results_poses):
        for res in results:
            if pid == res['pid']:
                keypoints = res[key]
                joint_positions.append(keypoints[joint_index])
                indices.append(i)
                break
    if timestamps is not None:
        timestamps = np.array(timestamps, dtype=np.float64)[indices]
        return joint_positions, indices, timestamps
    return joint_positions, indices


def extract_target_pid_joint_positions(results_poses, pid,
                                       key='keypoints', timestamps=None):
    joint_positions_list = []
    indices = []
    for i, results in enumerate(results_poses):
        for res in results:
            if pid == res['pid']:
                joint_positions_list.append(res[key])
                indices.append(i)
                break
    if timestamps is not None:
        timestamps = np.array(timestamps, dtype=np.float64)[indices]
        return joint_positions_list, indices, timestamps
    return joint_positions_list, indices


def extract_target_pid_poses(results_poses, target_pid):
    """Extract target pid poses

    Parameters
    ----------
    results_poses : list[list[dict]]
        input poses
    target_pid : int
        target pid

    Returns
    -------
    new_results_poses : list[list[dict]]
        output poses
    """
    new_results_poses = []
    for results_pose in results_poses:
        new_results_poses.append(
            [res for res in results_pose if res['pid'] == target_pid])
    return new_results_poses


def extract_most_frequent_pid_poses(results_poses, timestamps):
    pid, indices = extract_most_frequent_pid_indices(results_poses)

    target_results_poses = [results_poses[i] for i in indices]
    np_stamps = np.array(timestamps, dtype=np.float64)[indices]
    return target_results_poses, np_stamps, indices, pid


def calculate_base_rotations(
        shoulder_r_positions,
        shoulder_l_positions,
        chest_positions,
        base_positions):
    shoulder_r_positions = np.array(shoulder_r_positions)
    shoulder_l_positions = np.array(shoulder_l_positions)
    chest_positions = np.array(chest_positions)
    base_positions = np.array(base_positions)
    v1s = shoulder_r_positions - chest_positions
    v2s = shoulder_l_positions - chest_positions
    upright_vector = chest_positions - base_positions
    # z-axis: center direction of human
    # x-axis: direction of left shoulder to right shoulder

    base_rotations = []
    for v1, v2, up in zip(v1s, v2s, upright_vector):
        base_rotation = rotation_matrix_from_axis(
            up, np.cross(v2, v1), axes='yz')
        base_rotations.append(base_rotation)
    return base_rotations
