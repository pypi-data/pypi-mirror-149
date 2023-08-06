from collections import Counter
from collections import namedtuple
from collections import OrderedDict
from numbers import Number
from typing import Dict
from typing import List

import numpy as np
from skrobot.coordinates import Coordinates
from skrobot.coordinates.math import angle_between_vectors
from skrobot.coordinates.math import rotation_matrix_from_axis


Labanotation = namedtuple(
    'Labanotation', ('spherical', 'laban'))

LabanotationData = namedtuple(
    'LabanotationData',
    ('elbow_right', 'wrist_right',
     'elbow_left', 'wrist_left'))


def l2_normalize(x):
    return x / np.linalg.norm(x, ord=2)


def cartesian_to_spherical(vec):
    """Converting a vector from Cartesian coordianates to spherical coordinates

    theta: 0~180 (zenith), phi: 0~180 for left, 0~-180 for right (azimuth)

    Examples
    --------
    >>> cartesian_to_spherical([1, 1, 1])
    (1.7320508075688772, 54.735610317245346, 45.0)
    >>> cartesian_to_spherical([1, 0, 0])
    (1.0, 90.0, 0.0)
    >>> cartesian_to_spherical([0, 0, -1])
    (1.0, 180.0, 0.0)
    >>> cartesian_to_spherical([0, 0, 1])
    (1.0, 0.0, 0.0)
    >>> cartesian_to_spherical([0, 1, 0])
    (1.0, 90.0, 90.0)
    """
    x, y, z = vec
    vec = np.array(vec, dtype=np.float32)
    r = np.sqrt(np.sum(vec ** 2))
    if r == 0.0:
        return 0.0, 0.0, 0.0
    theta = np.degrees(np.arccos(z / r))
    if x != 0.0:
        phi = np.degrees(np.arctan(y / x))
    else:
        if y > 0:
            phi = 90
        else:
            phi = -90
    if x < 0 and y > 0:
        phi = 180 + phi
    elif x < 0 and y < 0:
        phi = -180 + phi
    else:
        phi = phi
    return r, theta, phi


def coordinates2labanotation(theta, phi):
    """Convert theta phi coordinates to labanotation.

    """
    # set default labanotation
    laban = ['Middle', 'Forward']

    # find direction, phi, (-180,180]
    # forward
    if 0 <= phi <= 22.5 or -22.5 < phi < 0:
        laban[0] = 'Forward'
    elif 22.5 < phi <= 67.5:
        laban[0] = 'Left Forward'
    elif 67.5 < phi <= 112.5:
        laban[0] = 'Left'
    elif 112.5 < phi <= 157.5:
        laban[0] = 'Left Backward'
    elif -180 < phi <= -157.5 or 157.5 < phi <= 180:
        laban[0] = 'Backward'
    elif -157.5 < phi <= -112.5:
        laban[0] = 'Right Backward'
    elif -112.5 < phi <= -67.5:
        laban[0] = 'Right'
    else:
        laban[0] = 'Right Forward'

    # find height, theta, [0,180]
    # place high
    if theta < 22.5:
        laban = ['Place', 'High']
    # high
    elif theta < 67.5:
        laban[1] = 'High'
    # normal/mid
    elif theta < 112.5:
        laban[1] = 'Middle'
    # low
    elif theta < 157.5:
        laban[1] = 'Low'
    # place low
    else:
        laban = ['Place', 'Low']

    return laban


def calculate_labanotation(
        spine_position, shoulder_r_position, shoulder_l_position,
        elbow_r_position, elbow_l_position,
        wrist_r_position, wrist_l_position,
        base_rotation=None):
    spine_position = np.array(spine_position)
    shoulder_l_position = np.array(shoulder_l_position)
    shoulder_r_position = np.array(shoulder_r_position)
    elbow_r_position = np.array(elbow_r_position)
    elbow_l_position = np.array(elbow_l_position)
    wrist_r_position = np.array(wrist_r_position)
    wrist_l_position = np.array(wrist_l_position)

    if base_rotation is None:
        # calculate base coordinates.
        v1 = shoulder_l_position - shoulder_r_position
        v2 = spine_position - shoulder_r_position
        # x-axis: center direction of human
        # y-axis: direction of left shoulder to right shoulder
        base_rotation = rotation_matrix_from_axis(
            np.cross(v2, v1), v1, axes='xy')

    shoulder_to_elbow_r_vector = elbow_r_position - shoulder_r_position
    shoulder_to_elbow_l_vector = elbow_l_position - shoulder_l_position
    elbow_to_wrist_r_vector = wrist_r_position - elbow_r_position
    elbow_to_wrist_l_vector = wrist_l_position - elbow_l_position

    # convert kinect space coordinates to human-centered spherical coordinates.
    elbow_r_radius, elbow_r_theta, elbow_r_phi = cartesian_to_spherical(
        np.dot(base_rotation.T, shoulder_to_elbow_r_vector))
    elbow_l_radius, elbow_l_theta, elbow_l_phi = cartesian_to_spherical(
        np.dot(base_rotation.T, shoulder_to_elbow_l_vector))
    wrist_r_radius, wrist_r_theta, wrist_r_phi = cartesian_to_spherical(
        np.dot(base_rotation.T, elbow_to_wrist_r_vector))
    wrist_l_radius, wrist_l_theta, wrist_l_phi = cartesian_to_spherical(
        np.dot(base_rotation.T, elbow_to_wrist_l_vector))

    return (elbow_r_radius, elbow_r_theta, elbow_r_phi), \
        (elbow_l_radius, elbow_l_theta, elbow_l_phi), \
        (wrist_r_radius, wrist_r_theta, wrist_r_phi), \
        (wrist_l_radius, wrist_l_theta, wrist_l_phi), \
        coordinates2labanotation(elbow_r_theta, elbow_r_phi), \
        coordinates2labanotation(elbow_l_theta, elbow_l_phi), \
        coordinates2labanotation(wrist_r_theta, wrist_r_phi), \
        coordinates2labanotation(wrist_l_theta, wrist_l_phi)


def laban_keyframe_to_script(idx, time, dur, laban_score):
    strScript = ""
    strScript += '#' + str(idx) + '\n'
    strScript += 'Start Time:' + \
        str(time) + '\nDuration:' + str(dur) + '\nHead:Forward:Middle\n'
    strScript += 'Right Elbow:' + \
        laban_score[0][0] + ':' + laban_score[0][1] + '\n'
    strScript += 'Right Wrist:' + \
        laban_score[1][0] + ':' + laban_score[1][1] + '\n'
    strScript += 'Left Elbow:' + \
        laban_score[2][0] + ':' + laban_score[2][1] + '\n'
    strScript += 'Left Wrist:' + \
        laban_score[3][0] + ':' + laban_score[3][1] + '\n'
    strScript += 'Rotation:ToLeft:0.0\n'
    return strScript


def labanotation_to_script(time_indices: List[int],
                           all_laban: List[List[str]]) -> str:
    """Convert labanotation to plain text.

    Examples
    --------
    >>> time_indices = [1, 67]
    >>> all_laban = [
    ... [['Place', 'Low'], ['Place', 'Low'],
    ...  ['Place', 'Low'], ['Place', 'Low']],
    ... [['Place', 'Low'], ['Place', 'Low'],
    ...  ['Place', 'Low'], ['Place', 'Low']],
    ... ]
    >>> text = labanotation_to_script(time_indices, all_laban)
    >>> print(text)
    #0
    Start Time:1
    Duration:1
    Head:Forward:Middle
    Right Elbow:Place:Low
    Right Wrist:Place:Low
    Left Elbow:Place:Low
    Left Wrist:Place:Low
    Rotation:ToLeft:0.0
    #1
    Start Time:67
    Duration:-1
    Head:Forward:Middle
    Right Elbow:Place:Low
    Right Wrist:Place:Low
    Left Elbow:Place:Low
    Left Wrist:Place:Low
    Rotation:ToLeft:0.0
    """
    if all_laban is None:
        return ""

    text = ""
    cnt = len(all_laban)
    for j in range(cnt):
        if j == 0:
            time = 1
        else:
            time = int(time_indices[j])

        if j == (cnt - 1):
            dur = '-1'
        else:
            dur = '1'

        text += laban_keyframe_to_script(j, time, dur, all_laban[j])

    return text


def get_labanotation_keyframe_data(
        time: Number,
        duration: Number,
        laban: List[List[str]]) -> Dict:
    data = OrderedDict()
    data["start time"] = [str(time)]
    data["duration"] = [str(duration)]
    data["head"] = ['Forward', 'Middle']
    data["right elbow"] = [laban[0][0], laban[0][1]]
    data["right wrist"] = [laban[1][0], laban[1][1]]
    data["left elbow"] = [laban[2][0], laban[2][1]]
    data["left wrist"] = [laban[3][0], laban[3][1]]
    data["rotation"] = ['ToLeft', '0']
    return data


def append_edge_indices(indices, length):
    if len(indices) == 0:
        if length == 0:
            return np.array([0])
        return np.array([0, length])
    if indices[0] != 0:
        indices = np.concatenate([np.array([0]), indices])
    if indices[-1] != length:
        indices = np.concatenate([indices, np.array([length])])
    return indices


def segmentation_from_labanotations(
        labans: List[List[str]]) -> List[List[int]]:
    n = len(labans)
    # ptr always pointed to the
    ptr = 1
    start = 0
    laban_sect = []
    while ptr < n and start < n:
        while labans[ptr] == labans[start] and ptr < n - 1:
            ptr += 1
        # (x_start, y_start), x_width, y_width, alpha
        laban_sect.append([start, ptr - 1])
        start = ptr
        ptr += 1
    return laban_sect


def calculate_z_axis(shoulder_l_positions,
                     shoulder_r_positions,
                     base_positions):
    v1s = shoulder_l_positions - shoulder_r_positions
    v2s = base_positions - shoulder_r_positions
    x_axes = np.cross(v2s, v1s)
    x_axes = x_axes / np.linalg.norm(x_axes, axis=1, keepdims=True, ord=2)
    y_axes = v1s / np.linalg.norm(v1s, axis=1, keepdims=True, ord=2)
    z_axes = np.cross(x_axes, y_axes)
    max_axes = np.argmax(np.abs(z_axes), axis=1)
    tmp = np.sign(z_axes[(np.arange(len(z_axes)), max_axes)]) * (max_axes + 1)
    tmp = np.array(tmp, dtype=np.int32)
    c = Counter(tmp.tolist()).most_common()[0][0]
    if c == 1:
        return [1, 0, 0]
    elif c == 2:
        return [0, 1, 0]
    elif c == 3:
        return [0, 0, 1]
    elif c == -1:
        return [-1, 0, 0]
    elif c == -2:
        return [0, -1, 0]
    elif c == -3:
        return [0, 0, -1]
    else:
        raise RuntimeError


def _calculate_base_orientation(shoulder_l_position,
                                shoulder_r_position,
                                base_position,
                                base_rotation=None,
                                z_axis=None):
    if base_rotation is not None:
        shoulder_l_position = np.dot(base_rotation.T, shoulder_l_position)
        shoulder_r_position = np.dot(base_rotation.T, shoulder_r_position)
        base_position = np.dot(base_rotation.T, base_position)
    v1 = shoulder_l_position - shoulder_r_position
    v2 = base_position - shoulder_r_position
    # x-axis: center direction of human
    # y-axis: direction of left shoulder to right shoulder
    if z_axis is None:
        base_rotation = rotation_matrix_from_axis(
            np.cross(v2, v1), v1, axes='xy')
    else:
        base_rotation = rotation_matrix_from_axis(
            z_axis, np.cross(v2, v1), axes='zx')
    return base_rotation


def calculate_unfiltered_labanotations(
        joint_positions_dict: Dict[str, np.ndarray],
        base_rotation_style: str = 'first',
        base_limb_name: str = 'spine_navel',
        z_axis: list = None,
        angle_threashold: float = 50.0):
    if base_rotation_style not in ['first', 'every', 'update']:
        raise ValueError

    n = len(joint_positions_dict[base_limb_name])

    # get hand position
    elR = np.zeros((n, 3))
    elL = np.zeros((n, 3))
    wrR = np.zeros((n, 3))
    wrL = np.zeros((n, 3))

    if base_rotation_style in ['first', 'update']:
        base_rotation = _calculate_base_orientation(
            joint_positions_dict['shoulder_left'][0],
            joint_positions_dict['shoulder_right'][0],
            joint_positions_dict[base_limb_name][0],
            z_axis=z_axis)

    # [right upper/elbow, right lower/wrist, left upper/elbow, left lower/wrist]  # NOQA
    # use coordinate2laban to generate labanotation for all frames
    unfilteredLaban = []

    for i in range(n):
        if base_rotation_style == 'every':
            base_rotation = _calculate_base_orientation(
                joint_positions_dict['shoulder_left'][i],
                joint_positions_dict['shoulder_right'][i],
                joint_positions_dict[base_limb_name][i],
                z_axis=z_axis)
        elif base_rotation_style == 'update':
            current_base_rotation = _calculate_base_orientation(
                joint_positions_dict['shoulder_left'][i],
                joint_positions_dict['shoulder_right'][i],
                joint_positions_dict[base_limb_name][i],
                base_rotation=base_rotation,
                z_axis=z_axis)
            angle = angle_between_vectors(
                Coordinates(rot=current_base_rotation).x_axis,
                [0, 1, 0],
                directed=False)
            if np.abs(np.rad2deg(angle)) >= angle_threashold:
                base_rotation = _calculate_base_orientation(
                    joint_positions_dict['shoulder_left'][i],
                    joint_positions_dict['shoulder_right'][i],
                    joint_positions_dict[base_limb_name][i],
                    z_axis=z_axis)

        pelvis_position = joint_positions_dict[base_limb_name][i]
        shoulder_l_position = joint_positions_dict['shoulder_left'][i]
        shoulder_r_position = joint_positions_dict['shoulder_right'][i]
        elbow_l_position = joint_positions_dict['elbow_left'][i]
        elbow_r_position = joint_positions_dict['elbow_right'][i]
        wrist_l_position = joint_positions_dict['wrist_left'][i]
        wrist_r_position = joint_positions_dict['wrist_right'][i]
        elR[i], elL[i], wrR[i], wrL[i], \
            elbow_r_laban, elbow_l_laban, wrist_r_laban, wrist_l_laban \
            = calculate_labanotation(
                pelvis_position, shoulder_r_position, shoulder_l_position,
                elbow_r_position, elbow_l_position,
                wrist_r_position, wrist_l_position,
                base_rotation=base_rotation
            )

        unfilteredLaban.append(
            [elbow_r_laban,
             wrist_r_laban,
             elbow_l_laban,
             wrist_l_laban])

    lines = \
        [[elR, [unfilteredLaban[i][0] for i in range(n)], 'b', "Right Elbow"],
         [wrR, [unfilteredLaban[i][1] for i in range(n)], 'c', "Right Wrist"],
         [elL, [unfilteredLaban[i][2] for i in range(n)], 'y', "Left Elbow"],
         [wrL, [unfilteredLaban[i][3] for i in range(n)], 'm', "Left Wrist"]]
    return lines


def calculate_unfiltered_labanotations_smart(*args, **kwargs):
    lines = calculate_unfiltered_labanotations(*args, **kwargs)
    return LabanotationData(
        elbow_right=Labanotation(lines[0][0], lines[0][1]),
        wrist_right=Labanotation(lines[1][0], lines[1][1]),
        elbow_left=Labanotation(lines[2][0], lines[2][1]),
        wrist_left=Labanotation(lines[3][0], lines[3][1]))


def laban_format_str(x: str):
    x = x.lower()
    tmp = x.split()
    if len(tmp) == 2:
        x = tmp[0] + tmp[1].capitalize()
    return x


def laban2str2(upper, lower, dir_height=False,
               space_delimiter='_'):
    """Convert upper and lower labanotations to string.

    Examples
    --------
    >>> upper = ['Middle', 'Forward']
    >>> lower = ['Place', 'Low']
    >>> laban2str(upper, lower)
    'middle_forward_place_low'
    >>> upper = ['Middle', 'Left Forward']
    >>> lower = ['Place', 'Low']
    >>> laban2str(upper, lower)
    'middle_left_forward_place_low'
    """
    if dir_height:
        '_'.join(
            [laban_format_str(upper[1]), laban_format_str(upper[0]),
             laban_format_str(lower[1]), laban_format_str(lower[0])]).replace(
                 ' ', space_delimiter)
    return '_'.join(
        [laban_format_str(upper[0]), laban_format_str(upper[1]),
         laban_format_str(lower[0]), laban_format_str(lower[1])]).replace(
             ' ', space_delimiter)


def laban2vec(laban: List[str],
              limb: str,
              limb_length: float = 5.0) -> List[float]:
    """Convert the labanotation for a given limb to a vector

    Examples
    --------
    >>> limb = 'right elbow'
    >>> laban = ['start time:1', 'duration:0', 'head:forward:middle', 'right elbow:place:low', 'right wrist:forward:low', 'left elbow:place:low', 'left wrist:forward:low', 'Rotation:ToLeft:0.0']  # NOQA
    >>> laban2vec(laban, limb)
    (0.0, -4.980973467754132, 0.4357789732529257)
    """
    theta = 175
    phi = 0
    for i in range(0, len(laban)):
        laban[i] = laban[i].lower()
        tmp_str = laban[i].split(":")
        if tmp_str[0] != limb:
            continue
        direction, level = tmp_str[1], tmp_str[2]
        if level == "high":
            theta = 45
        elif level == "middle":
            theta = 90
        elif level == "low":
            theta = 135
        else:
            theta = 180
            print('Unknown Level.')

        if direction == "forward":
            phi = 0
        elif direction == "right forward":
            phi = -45
        elif direction == "right":
            phi = -90
        elif direction == "right backward":
            phi = -135
        elif direction == "backward":
            phi = 180
        elif direction == "left backward":
            phi = 135
        elif direction == "left":
            phi = 90
        elif direction == "left forward":
            phi = 45
        elif direction == "place":
            if level == "high":
                theta = 5
                phi = 0
            elif level == "low":
                theta = 175
                phi = 0
            else:
                theta = 180
                phi = 0
                print('Unknown Place')
        else:
            phi = 0
            print('Unknown Direction.')
        break

    y = limb_length * np.cos(np.deg2rad(theta))
    x = limb_length * np.sin(np.deg2rad(theta)) * np.sin(np.deg2rad(phi))
    z = limb_length * np.sin(np.deg2rad(theta)) * np.cos(np.deg2rad(phi))
    return [x, y, z]


def arrange_labanotations(
        labanotations_list: List[List[List[str]]]) -> List[List[List[str]]]:
    if len(set([len(labans) for labans in labanotations_list])) != 1:
        raise ValueError
    n = len(labanotations_list[0])
    return [[labans[i] for labans in labanotations_list]
            for i in range(n)]


def extract_target_labanotations(
        target_indices: List[int],
        unfiltered_labanotations:
        List[List[List[str]]]) -> List[List[List[str]]]:
    """Extract target indices's labanotations.

    """
    all_laban = []
    target_indices = append_edge_indices(
        np.array(target_indices, dtype='i'),
        len(unfiltered_labanotations) - 1)
    for i, target_index in enumerate(target_indices):
        all_laban.append(unfiltered_labanotations[target_index])
    return target_indices, all_laban


def decompress_keyframe_labans(keyframe_indices, labans):
    max_index = keyframe_indices[-1]
    all_indices = np.array([0 for _ in range(max_index + 1)], 'i')
    i = 0
    j = 0
    while i < max_index:
        while i > keyframe_indices[j]:
            j += 1
        all_indices[i] = j
        i += 1
    return [labans[index] for index in all_indices]
