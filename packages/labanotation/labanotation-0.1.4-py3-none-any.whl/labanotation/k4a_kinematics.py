from enum import IntEnum


class K4AJointIndices(IntEnum):
    """Azure Kinect Joint Indices

    For more detail, please see a following link.
    https://docs.microsoft.com/de-de/azure/Kinect-dk/body-joints

    """
    K4ABT_JOINT_PELVIS = 0
    K4ABT_JOINT_SPINE_NAVEL = 1
    K4ABT_JOINT_SPINE_CHEST = 2
    K4ABT_JOINT_NECK = 3
    K4ABT_JOINT_CLAVICLE_LEFT = 4
    K4ABT_JOINT_SHOULDER_LEFT = 5
    K4ABT_JOINT_ELBOW_LEFT = 6
    K4ABT_JOINT_WRIST_LEFT = 7
    K4ABT_JOINT_HAND_LEFT = 8
    K4ABT_JOINT_HANDTIP_LEFT = 9
    K4ABT_JOINT_THUMB_LEFT = 10
    K4ABT_JOINT_CLAVICLE_RIGHT = 11
    K4ABT_JOINT_SHOULDER_RIGHT = 12
    K4ABT_JOINT_ELBOW_RIGHT = 13
    K4ABT_JOINT_WRIST_RIGHT = 14
    K4ABT_JOINT_HAND_RIGHT = 15
    K4ABT_JOINT_HANDTIP_RIGHT = 16
    K4ABT_JOINT_THUMB_RIGHT = 17
    K4ABT_JOINT_HIP_LEFT = 18
    K4ABT_JOINT_KNEE_LEFT = 19
    K4ABT_JOINT_ANKLE_LEFT = 20
    K4ABT_JOINT_FOOT_LEFT = 21
    K4ABT_JOINT_HIP_RIGHT = 22
    K4ABT_JOINT_KNEE_RIGHT = 23
    K4ABT_JOINT_ANKLE_RIGHT = 24
    K4ABT_JOINT_FOOT_RIGHT = 25
    K4ABT_JOINT_HEAD = 26
    K4ABT_JOINT_NOSE = 27
    K4ABT_JOINT_EYE_LEFT = 28
    K4ABT_JOINT_EAR_LEFT = 29
    K4ABT_JOINT_EYE_RIGHT = 30
    K4ABT_JOINT_EAR_RIGHT = 31
    K4ABT_JOINT_COUNT = 32


K4AJointConnections = (
    (K4AJointIndices.K4ABT_JOINT_SPINE_NAVEL, K4AJointIndices.K4ABT_JOINT_PELVIS),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_SPINE_CHEST, K4AJointIndices.K4ABT_JOINT_SPINE_NAVEL),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_NECK, K4AJointIndices.K4ABT_JOINT_SPINE_CHEST),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_CLAVICLE_LEFT, K4AJointIndices.K4ABT_JOINT_SPINE_CHEST),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_SHOULDER_LEFT, K4AJointIndices.K4ABT_JOINT_CLAVICLE_LEFT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_ELBOW_LEFT, K4AJointIndices.K4ABT_JOINT_SHOULDER_LEFT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_WRIST_LEFT, K4AJointIndices.K4ABT_JOINT_ELBOW_LEFT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_HAND_LEFT, K4AJointIndices.K4ABT_JOINT_WRIST_LEFT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_HANDTIP_LEFT, K4AJointIndices.K4ABT_JOINT_HAND_LEFT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_THUMB_LEFT, K4AJointIndices.K4ABT_JOINT_WRIST_LEFT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_CLAVICLE_RIGHT, K4AJointIndices.K4ABT_JOINT_SPINE_CHEST),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_SHOULDER_RIGHT, K4AJointIndices.K4ABT_JOINT_CLAVICLE_RIGHT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_ELBOW_RIGHT, K4AJointIndices.K4ABT_JOINT_SHOULDER_RIGHT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_WRIST_RIGHT, K4AJointIndices.K4ABT_JOINT_ELBOW_RIGHT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_HAND_RIGHT, K4AJointIndices.K4ABT_JOINT_WRIST_RIGHT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_HANDTIP_RIGHT, K4AJointIndices.K4ABT_JOINT_HAND_RIGHT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_THUMB_RIGHT, K4AJointIndices.K4ABT_JOINT_WRIST_RIGHT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_HIP_LEFT, K4AJointIndices.K4ABT_JOINT_PELVIS),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_KNEE_LEFT, K4AJointIndices.K4ABT_JOINT_HIP_LEFT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_ANKLE_LEFT, K4AJointIndices.K4ABT_JOINT_KNEE_LEFT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_FOOT_LEFT, K4AJointIndices.K4ABT_JOINT_ANKLE_LEFT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_HIP_RIGHT, K4AJointIndices.K4ABT_JOINT_PELVIS),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_KNEE_RIGHT, K4AJointIndices.K4ABT_JOINT_HIP_RIGHT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_ANKLE_RIGHT, K4AJointIndices.K4ABT_JOINT_KNEE_RIGHT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_FOOT_RIGHT, K4AJointIndices.K4ABT_JOINT_ANKLE_RIGHT),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_HEAD, K4AJointIndices.K4ABT_JOINT_NECK),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_NOSE, K4AJointIndices.K4ABT_JOINT_HEAD),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_EYE_LEFT, K4AJointIndices.K4ABT_JOINT_HEAD),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_EAR_LEFT, K4AJointIndices.K4ABT_JOINT_HEAD),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_EYE_RIGHT, K4AJointIndices.K4ABT_JOINT_HEAD),  # NOQA
    (K4AJointIndices.K4ABT_JOINT_EAR_RIGHT, K4AJointIndices.K4ABT_JOINT_HEAD))


keypoint_names = (
    "PELVIS",
    "SPINE_NAVEL",
    "SPINE_CHEST",
    "NECK",
    "CLAVICLE_LEFT",
    "SHOULDER_LEFT",
    "ELBOW_LEFT",
    "WRIST_LEFT",
    "HAND_LEFT",
    "HANDTIP_LEFT",
    "THUMB_LEFT",
    "CLAVICLE_RIGHT",
    "SHOULDER_RIGHT",
    "ELBOW_RIGHT",
    "WRIST_RIGHT",
    "HAND_RIGHT",
    "HANDTIP_RIGHT",
    "THUMB_RIGHT",
    "HIP_LEFT",
    "KNEE_LEFT",
    "ANKLE_LEFT",
    "FOOT_LEFT",
    "HIP_RIGHT",
    "KNEE_RIGHT",
    "ANKLE_RIGHT",
    "FOOT_RIGHT",
    "HEAD",
    "NOSE",
    "EYE_LEFT",
    "EAR_LEFT",
    "EYE_RIGHT",
    "EAR_RIGHT",
)

keypoint_names = list(map(lambda s: s.lower(), keypoint_names))


_index_to_keypoint_name = {
    i: name for i, name in enumerate(keypoint_names)
}


_keypoint_name_to_index = {
    name: i for i, name in enumerate(keypoint_names)
}


def index_to_keypoint_name(index):
    return _index_to_keypoint_name[index]


def indices_to_keypoint_names(indices):
    return [_index_to_keypoint_name[i] for i in indices]


def normalize_keypoint_names(values):
    names = []
    for value in values:
        if isinstance(value, int):
            value = _index_to_keypoint_name[value]
        else:
            raise ValueError('Unsupported type {}'.format(type(value)))
        names.append(value)
    return names


def normalize_keypoint_names_to_indices(values):
    if isinstance(values, list):
        atom = False
    else:
        values = [values]
        atom = True

    indices = []
    for value in values:
        if isinstance(value, int):
            pass
        elif isinstance(value, str):
            value = value.lower()
            if value in _keypoint_name_to_index:
                value = _keypoint_name_to_index[value]
            else:
                raise ValueError('Unsupported joint name: {}'
                                 'Valid joint names are {}.'
                                 .format(value, keypoint_names))
        else:
            raise ValueError('Unsupported type: {}'.format(type(value)))
        indices.append(value)
    if atom:
        return indices[0]
    return indices
