from collections import OrderedDict

import numpy as np


def joint_mapping(source_format, target_format):
    mapping = np.ones(len(target_format), dtype=np.int) * -1
    for joint_name in target_format:
        if joint_name in source_format:
            mapping[target_format[joint_name]] = source_format[joint_name]
    return np.array(mapping)


SMPL_24 = {
    'Pelvis_SMPL': 0,
    'L_Hip_SMPL': 1,
    'R_Hip_SMPL': 2,
    'Spine_SMPL': 3,
    'L_Knee': 4,
    'R_Knee': 5,
    'Thorax_SMPL': 6,
    'L_Ankle': 7,
    'R_Ankle': 8,
    'Thorax_up_SMPL': 9,
    'L_Toe_SMPL': 10,
    'R_Toe_SMPL': 11,
    'Neck': 12,
    'L_Collar': 13,
    'R_Collar': 14,
    'Jaw': 15,
    'L_Shoulder': 16,
    'R_Shoulder': 17,
    'L_Elbow': 18,
    'R_Elbow': 19,
    'L_Wrist': 20,
    'R_Wrist': 21,
    'L_Hand': 22,
    'R_Hand': 23}
SMPL_EXTRA_30 = {
    'Nose': 24,
    'R_Eye': 25,
    'L_Eye': 26,
    'R_Ear': 27,
    'L_Ear': 28,
    'L_BigToe': 29,
    'L_SmallToe': 30,
    'L_Heel': 31,
    'R_BigToe': 32,
    'R_SmallToe': 33,
    'R_Heel': 34,
    'L_Hand_thumb': 35,
    'L_Hand_index': 36,
    'L_Hand_middle': 37,
    'L_Hand_ring': 38,
    'L_Hand_pinky': 39,
    'R_Hand_thumb': 40,
    'R_Hand_index': 41,
    'R_Hand_middle': 42,
    'R_Hand_ring': 43,
    'R_Hand_pinky': 44,
    'R_Hip': 45,
    'L_Hip': 46,
    'Neck_LSP': 47,
    'Head_top': 48,
    'Pelvis': 49,
    'Thorax_MPII': 50,
    'Spine_H36M': 51,
    'Jaw_H36M': 52,
    'Head': 53}
SMPL_ALL_54 = {**SMPL_24, **SMPL_EXTRA_30}

kinect_names = ['spineB', 'spineM',
                'neck', 'head',
                'shoulderL', 'elbowL', 'wristL', 'handL',
                'shoulderR', 'elbowR', 'wristR', 'handR',
                'hipL', 'kneeL', 'ankleL', 'footL',
                'hipR', 'kneeR', 'ankleR', 'footR',
                'spineS', 'handTL', 'thumbL', 'handTR', 'thumbR', ]

Kinect_25 = OrderedDict(
    [('Pelvis', 0),
     ('Spine_H36M', 1),
     ('Neck', 2),
     ('Head', 3),
     ('L_Shoulder', 4),
     ('L_Elbow', 5),
     ('L_Wrist', 6),
     ('L_Hand', 7),
     ('R_Shoulder', 8),
     ('R_Elbow', 9),
     ('R_Wrist', 10),
     ('R_Hand', 11),
     ('L_Hip', 12),
     ('L_Knee', 13),
     ('L_Ankle', 14),
     ('L_BigToe', 15),
     ('R_Hip', 16),
     ('R_Knee', 17),
     ('R_Ankle', 18),
     ('R_BigToe', 19),
     ('Thorax_MPII', 20),
     ('L_Hand_index', 21),
     ('L_Hand_thumb', 22),
     ('R_Hand_index', 23),
     ('R_Hand_thumb', 24), ]
)

kinect_to_index = joint_mapping(SMPL_ALL_54, Kinect_25)
kinect_name_to_smpl_index = {}
for kn, smpl_name, index in zip(kinect_names, Kinect_25, kinect_to_index):
    kinect_name_to_smpl_index[kn] = index
