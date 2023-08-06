# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------------------------

import numpy as np


def b_peak_dect(data, sect, k=5):
    y = np.array(data)

    # get its derivatives
    dy = np.array([(y[i] - y[i - 1]) for i in range(1, len(y))])
    scale = 1.0 / max(abs(dy.min()), abs(dy.max()))
    dy = dy * scale

    corner = []
    pos = 0
    valley = 0  # valley start sign

    # use the serial number of y for counting
    # start from 1 (0 has no derivative to the left)
    # end at len(u)-2 (len(u)-1 has no derivative to the right)
    for i in range(1, len(dy) - 2):
        zero = 10**(-6)
        # under some threshold, take dy as 0
        if dy[i] < 0 and dy[i + 1] > 0:
            # print 'acute valley'
            pos = i
            # search for the valley
            if pos < y.shape[0] - 1:
                if y[pos] > y[pos + 1]:
                    pos += 1
            corner.append(pos)
        # from neg to pos, or from pos to neg, means there should be 0 in
        # between
        elif dy[i] < -zero and abs(dy[i + 1]) < zero:
            # print 'down, valley start'
            valley = 1
            if pos < len(dy) - 1:
                if y[pos] > y[pos + 1]:
                    pos += 1
            corner.append(pos)
        elif abs(dy[i]) < zero and dy[i + 1] > zero and valley == 1:
            # print 'up, valley end'
            if pos < len(dy) - 1:
                if y[pos] > y[pos + 1]:
                    pos += 1
            corner.append(pos)
            valley = 0

    # remove duplicated element (if there is any)
    corner = sorted(set(corner), key=corner.index)
    # filter no. 4
    # remove extra marker in the same labanotation section
    for i in range(len(sect)):
        start = sect[i][0]
        end = sect[i][1]
        within = []
        for j in range(start, end + 1):
            if j in corner:
                within.append(j)
        for j in within[1:-1]:
            corner.remove(j)

    return corner


def peak_dect(data, x_thres=0, y_thres=360 / 16.0):
    # [[peak/valley index, status],...]
    # status==-1: valley,
    # status== 1, peak.
    peaks = [[0, 0]]

    grad = np.zeros(len(data) - 1)
    for i in range(len(data) - 1):
        grad[i] = data[i + 1] - data[i]

    # (>0,<0),(>0,=0) are peaks,
    # (<0,>0),(<0,=0) are valleys,
    # (=0,=0),(=0,<0),(=0,>0) are not needed.
    for i in range(1, len(grad) - 1):
        if grad[i] < 0 and grad[i + 1] >= 0:
            peaks.append([i + 1, -1])
        elif grad[i] > 0 and grad[i + 1] <= 0:
            peaks.append([i + 1, 1])
        else:
            continue

    remove = []

    # remove peaks/valleys too close to each other based on position and value
    for i in range(len(peaks) - 1, 0, -1):
        t = peaks[i - 1][1]   # type, peak or valley
        now = data[peaks[i][0]]
        prev = data[peaks[i - 1][0]]
        if t == -1:   # valley
            # set up upper and lower threshold differently to prevent
            # overshot/ringing
            up = y_thres * 2 / 3
            low = y_thres * 1 / 3
        else:   # peak
            up = y_thres * 1 / 3
            low = y_thres * 2 / 3
        if now < prev + up and now > prev - low:
            remove.append(peaks[i][0])
            del peaks[i]

    # or you can return peaks directly
    out_peaks = [peaks[j][0] for j in range(len(peaks)) if peaks[j][1] == 1]
    out_valleys = [peaks[j][0] for j in range(len(peaks)) if peaks[j][1] == -1]

    return (out_peaks, out_valleys, remove)
