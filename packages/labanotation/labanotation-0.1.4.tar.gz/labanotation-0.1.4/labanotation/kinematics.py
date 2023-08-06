from __future__ import division

import numpy as np


keypoint_names = (
    'Nose',
    'LEye',
    'REye',
    'LEar',
    'REar',
    'LShoulder',
    'RShoulder',
    'LElbow',
    'RElbow',
    'LWrist',
    'RWrist',
    'LHip',
    'RHip',
    'LKnee',
    'RKnee',
    'LAnkle',
    'RAnkle',
    'Neck',
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
                raise ValueError('Unsupported finger joint name: {}'
                                 .format(value))
        else:
            raise ValueError('Unsupported type: {}'.format(type(value)))
        indices.append(value)
    if atom:
        return indices[0]
    return indices


name2indices = {
    'Nose': 0,
    'LEye': 1,
    'REye': 2,
    'LEar': 3,
    'REar': 4,
    'LShoulder': 5,
    'RShoulder': 6,
    'LElbow': 7,
    'RElbow': 8,
    'LWrist': 9,
    'RWrist': 10,
    'LHip': 11,
    'RHip': 12,
    'LKnee': 13,
    'RKnee': 14,
    'LAnkle': 15,
    'RAnkle': 16,
    'Neck': 17,
}


limb_sequence = [[2, 1], [1, 16], [1, 15], [6, 18], [3, 17],
                 [2, 3], [2, 6], [3, 4], [4, 5], [6, 7],
                 [7, 8], [2, 9], [9, 10], [10, 11], [2, 12],
                 [12, 13], [13, 14], [15, 17], [16, 18]]


index2limbname = ["Nose",
                  "Neck",
                  "RShoulder",
                  "RElbow",
                  "RWrist",
                  "LShoulder",
                  "LElbow",
                  "LWrist",
                  "RHip",
                  "RKnee",
                  "RAnkle",
                  "LHip",
                  "LKnee",
                  "LAnkle",
                  "REye",
                  "LEye",
                  "REar",
                  "LEar",
                  "Bkg"]

limb_length_hand_ratio = [
    0.6, 0.2, 0.2, 0.85, 0.85,
    0.6, 0.6, 0.93, 0.65, 0.95,
    0.65, 2.2, 1.7, 1.7, 2.2,
    1.7, 1.7, 0.25, 0.25]


def expand_bbox(bbox, frame_width, frame_height, scale=1.2,
                min_width=10, min_height=10):
    top, left, bottom, right = bbox
    width = max(right - left, min_width)
    height = max(bottom - top, min_height)
    ratio = (- width - height
             + np.sqrt(
                 width ** 2 - 2 * width
                 * height + 4 * width * height * scale + height ** 2)) / 2
    new_left = np.clip(left - ratio, 0, frame_width)
    new_right = np.clip(right + ratio, 0, frame_width)
    new_top = np.clip(top - ratio, 0, frame_height)
    new_bottom = np.clip(bottom + ratio, 0, frame_height)
    return int(new_top), int(new_left), int(new_bottom), int(new_right)


def _get_hand_roi_width(joint_positions):
    lengths = []
    for (j1_index, j2_index), ratio in zip(
            limb_sequence, limb_length_hand_ratio):
        j1_name = index2limbname[j1_index - 1]
        j2_name = index2limbname[j2_index - 1]
        j1 = joint_positions[name2indices[j1_name]]
        j2 = joint_positions[name2indices[j2_name]]
        length = 0
        j1_x, j1_y, j1_score = j1
        j2_x, j2_y, j2_score = j2
        if j1_score > 0 and j2_score > 0:
            dx = j1_x - j2_x
            dy = j1_y - j2_y
            length = np.linalg.norm([dx, dy])
        lengths.append(length / ratio)
    if np.sum(lengths[:5]) > 0:
        lengths = lengths[:5]
    return np.sum(lengths) / len(np.nonzero(lengths)[0])


def _crop_square_image(img, cx, cy, width):
    cx, cy, width = int(cx), int(cy), int(width)
    left, right = cx - int(width / 2), cx + int(width / 2)
    top, bottom = cy - int(width / 2), cy + int(width / 2)
    imh, imw, imc = img.shape
    top = max(0, top)
    bottom = min(imh, bottom)
    left = max(0, left)
    right = min(imw, right)
    return top, left, bottom, right


def get_hand_bbox(bgr_img, joint_positions, handedness='R',
                  elbow_score_threshold=0.3):
    handedness = handedness.lower()
    if handedness in ['r', 'right', 'rarm', 'rhand']:
        handedness = 'R'
    elif handedness in ['l', 'left', 'larm', 'lhand']:
        handedness = 'L'
    else:
        raise ValueError("Invalid handedness.")

    H, W = bgr_img.shape[:2]
    width = _get_hand_roi_width(joint_positions)
    if np.isnan(width):
        return 0.0, (0.0, 0.0, H - 1, W - 1)
    cx, cy, score = joint_positions[name2indices['{}Wrist'.format(handedness)]]
    elbow_x, elbow_y, elbow_score = joint_positions[
        name2indices['{}Elbow'.format(handedness)]]
    if elbow_score > elbow_score_threshold:
        cx += 0.3 * (cx - elbow_x)
        cy += 0.3 * (cy - elbow_y)
    y1, x1, y2, x2 = _crop_square_image(bgr_img, cx, cy, width)
    y1 = np.clip(y1, 0, H - 1)
    y2 = np.clip(y2, 0, H - 1)
    x1 = np.clip(x1, 0, W - 1)
    x2 = np.clip(x2, 0, W - 1)
    if y1 >= y2 or x1 >= x2:
        return None, None
    return score, (y1, x1, y2, x2)


def get_bbox_from_pose(pose, frame_width, frame_height, scale=1.2):
    xmin = np.min(pose[:, 0])
    xmax = np.max(pose[:, 0])
    ymin = np.min(pose[:, 1])
    ymax = np.max(pose[:, 1])

    return expand_bbox(
        (ymin, xmin, ymax, xmax), frame_width, frame_height,
        scale=scale)
