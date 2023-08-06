from collections import defaultdict

import numpy as np
import pandas as pd

from labanotation.k4a_kinematics import keypoint_names
from labanotation.math_utils import resample


def read_from_labanotation_suite(csv_filepath: str):
    """Read from labanotation suite format.

    """
    csv_data_names = [
        'unixtime',
        'spineB', 'spineM',
        'neck', 'head',
        'shoulderL', 'elbowL', 'wristL', 'handL',
        'shoulderR', 'elbowR', 'wristR', 'handR',
        'hipL', 'kneeL', 'ankleL', 'footL',
        'hipR', 'kneeR', 'ankleR', 'footR',
        'spineS', 'handTL', 'thumbL', 'handTR', 'thumbR',
    ]

    new_csv_data_names = ['unixtime']
    for name in csv_data_names[1:]:
        for suffix in ['x', 'y', 'z']:
            new_csv_data_names.append(name + '_' + suffix)
        new_csv_data_names.append(name + '_tracked')
    new_csv_data_names.append('')  # for LabanSuite
    # tracked=2, inferred=1, nottracked=0

    k4a_and_kinect_joint_pairs = (
        ("SHOULDER_RIGHT", 'shoulderR'),
        ("SHOULDER_LEFT", 'shoulderL'),
        ("ELBOW_LEFT", 'elbowL'),
        ("ELBOW_RIGHT", 'elbowR'),
        ("WRIST_RIGHT", 'wristR'),
        ("WRIST_LEFT", 'wristL'),
        ("HAND_RIGHT", 'handR'),
        ("HAND_LEFT", 'handL'),
        ("NECK", 'neck'),
        ("HEAD", 'head'),
        ("HIP_LEFT", 'hipL'),
        ("HIP_RIGHT", 'hipR'),
        ("KNEE_RIGHT", 'kneeR'),
        ("KNEE_LEFT", 'kneeL'),
        ("ANKLE_RIGHT", 'ankleR'),
        ("ANKLE_LEFT", 'ankleL'),
        ("FOOT_RIGHT", 'footR'),
        ("FOOT_LEFT", 'footL'),
        ("THUMB_LEFT", 'thumbL'),
        ("THUMB_RIGHT", 'thumbR'),
        ("HANDTIP_LEFT", 'handTL'),
        ("HANDTIP_RIGHT", 'handTR'),
        ('NECK', 'spineS'),
        ("PELVIS", 'spineB'),
        ("SPINE_NAVEL", 'spineM'),
    )

    df = pd.read_csv(str(csv_filepath),
                     delimiter=',',
                     header=None,
                     names=new_csv_data_names)

    timestamps = np.array(df['unixtime'])
    # for LabanSuite
    if np.any(timestamps > 10e7):
        cnt = (timestamps[1:] - timestamps[:-1]) // 10000 // 30
        cnt = np.maximum(cnt, 1)
        cnt = np.cumsum(np.pad(cnt, (1, 0), 'constant'))
        timestamps = timestamps[0] + cnt * 33
        timestamps = timestamps * 0.001
    else:
        timestamps = np.array(df['unixtime']) * 0.001
    timestamps = timestamps - timestamps[0]

    conv_dict = {}
    for a, b in k4a_and_kinect_joint_pairs:
        conv_dict[a.lower()] = b

    joint_positions_dict = defaultdict(list)
    for i, name in enumerate(keypoint_names):
        if name not in conv_dict:
            continue
        kinect_name = conv_dict[name]
        joint_positions_dict[name] = np.array(
            df[[kinect_name + '_x', kinect_name + '_y', kinect_name + '_z']])
        # remove nan
        non_nan_indices = np.unique(
            np.argwhere(
                np.logical_not(np.isnan(joint_positions_dict[name])))[:, 0])
        joint_positions_dict[name], sampled_timestamps = resample(
            np.array(joint_positions_dict[name])[non_nan_indices],
            timestamps[non_nan_indices],
            rate=30)
    return joint_positions_dict, sampled_timestamps
