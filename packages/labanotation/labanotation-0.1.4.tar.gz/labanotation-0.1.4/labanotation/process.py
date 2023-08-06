from pathlib import Path

import cv2
from eos import makedirs
import numpy as np
from pybsc import nsplit
from pybsc import save_json
from pybsc.video_utils import extract_target_frame_from_timestamp

from labanotation.algorithm import merge_keyframe_indices
from labanotation.io import read_from_labanotation_suite
from labanotation.labanotation_utils import arrange_labanotations
from labanotation.labanotation_utils import calculate_unfiltered_labanotations
from labanotation.labanotation_utils import extract_target_labanotations
from labanotation.labanotation_utils import laban2str2
from labanotation import parallel_energy
from labanotation import total_energy
from labanotation.visualization import labanotation_to_image


def get_labanotation_results(csv_filepath,
                             output_path,
                             video_path=None,
                             gauss_window_size=61,
                             gauss_sigma=5,
                             base_rotation_style='update',
                             save_laban_image=True,
                             return_full=False,
                             return_savefilepaths=False,
                             z_axis=None):
    output_path = Path(output_path)
    csv_filepath = Path(csv_filepath)
    save_filepaths = []

    joint_positions_dict, timestamps = read_from_labanotation_suite(
        csv_filepath)

    lines = calculate_unfiltered_labanotations(
        joint_positions_dict,
        base_rotation_style=base_rotation_style,
        z_axis=z_axis)
    labanotations_list = [line[1] for line in lines]
    positions_list = [line[0] for line in lines]
    keyframe_indices, valley_output, energy_list, naive_energy_list = \
        parallel_energy(
            labanotations_list,
            positions_list,
            gauss_window_size=gauss_window_size,
            gauss_large_sigma=gauss_sigma)
    all_labans = arrange_labanotations(labanotations_list)
    keyframe_indices, labans = extract_target_labanotations(
        keyframe_indices, all_labans)

    frame_to_second = (timestamps[-1] - timestamps[0]) / len(all_labans)
    keyframe_timestamps = frame_to_second * keyframe_indices

    if save_laban_image is True:
        makedirs(output_path)
        sp = max(1, len(keyframe_timestamps) // 20)
        for i, (a, b, idx) in enumerate(
                zip(nsplit(keyframe_timestamps, sp), nsplit(labans, sp),
                    nsplit(keyframe_indices, sp))):
            fm_a = np.array(a) - a[0]
            if video_path is not None:
                new_out = output_path \
                    / 'labanotation-{0:06}'.format(i)
                makedirs(new_out)
                imgs = []
                for j, c in enumerate(a):
                    img = extract_target_frame_from_timestamp(
                        video_path, c)
                    imgs.append(img)
                    if img is not None:
                        cv2.imwrite(str(new_out / '{0:06}.jpg'.format(j)), img)
                laban_img = labanotation_to_image(
                    fm_a, b, scale=100, imgs=imgs)
            else:
                laban_img = labanotation_to_image(fm_a, b, scale=100)
            cv2.imwrite(
                str(output_path
                    / 'labanotation-{0:06}.png'.format(i)),
                cv2.rotate(laban_img, cv2.ROTATE_90_CLOCKWISE))
            save_filepaths.append(
                str(output_path / 'labanotation-{0:06}.png'.format(i)))

    wrist_right_keyframe_indices, right_energy, _, _ = total_energy(
        timestamps,
        joint_positions_dict['wrist_right'],
        gauss_window_size=gauss_window_size,
        gauss_sigma=gauss_sigma)
    wrist_right_keyframe_indices = merge_keyframe_indices(
        [wrist_right_keyframe_indices], n=len(timestamps))
    wrist_left_keyframe_indices, left_energy, _, _ = total_energy(
        timestamps,
        joint_positions_dict['wrist_left'],
        gauss_window_size=gauss_window_size,
        gauss_sigma=gauss_sigma)
    wrist_left_keyframe_indices = merge_keyframe_indices(
        [wrist_left_keyframe_indices], n=len(timestamps))

    keyframe_dict = {}
    for index in keyframe_indices:
        keyframe_dict[int(index)] = True
    right_keyframe_dict = {}
    for index in wrist_right_keyframe_indices:
        right_keyframe_dict[int(index)] = True
    left_keyframe_dict = {}
    for index in wrist_left_keyframe_indices:
        left_keyframe_dict[int(index)] = True

    results = []
    for i, (tm, laban) in enumerate(zip(timestamps, all_labans)):
        d = {'timestamp': float(tm),
             'labanotation': {
                 'right': laban2str2(laban[0], laban[1],
                                     dir_height=True,
                                     space_delimiter=''),
                 'left': laban2str2(laban[2], laban[3],
                                    dir_height=True,
                                    space_delimiter=''),
                 # 'Right Elbow:': laban[0],
                 # 'Right Wrist:': laban[1],
                 # 'Left Elbow:': laban[2],
                 # 'Left Wrist:': laban[3],
             },
             'keyframe': False,
             'right_keyframe': False,
             'left_keyframe': False}
        d['keyframe'] = keyframe_dict.get(i, False)
        d['right_keyframe'] = right_keyframe_dict.get(i, False)
        d['left_keyframe'] = left_keyframe_dict.get(i, False)
        results.append(d)
    if return_full is False:
        laban_data = {
            'results': results,
        }
    else:
        laban_data = {
            'results': results,
            'keyframe_timestamps': keyframe_timestamps.tolist(),
            'keyframe_labanotations': labans,
            'keyframe_indices': keyframe_indices.tolist(),
            'timestamps': timestamps.tolist(),
            'labanotations': all_labans,
            'wrist_right_keyframe_timestamps':
            (frame_to_second * wrist_right_keyframe_indices).tolist(),
            'wrist_right_keyframe_indices':
            wrist_right_keyframe_indices.tolist(),
            'right_energy': right_energy.tolist(),
            'wrist_left_keyframe_timestamps':
            (frame_to_second * wrist_left_keyframe_indices).tolist(),
            'wrist_left_keyframe_indices':
            wrist_left_keyframe_indices.tolist(),
            'left_energy': left_energy.tolist(),
            'parameters': {'gauss_window_size': gauss_window_size,
                           'gauss_sigma': gauss_sigma,
                           'base_rotation_style': base_rotation_style,
                           'frame_to_second': float(frame_to_second)}}
    save_json(laban_data, output_path / 'labanotation.json')
    save_filepaths.append(output_path / 'labanotation.json')
    if return_savefilepaths:
        return laban_data, save_filepaths
    else:
        return laban_data
