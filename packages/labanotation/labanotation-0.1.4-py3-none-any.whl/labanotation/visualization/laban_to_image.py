from typing import List

import cv2
import numpy as np
from pybsc.image_utils import resize_keeping_aspect_ratio

from labanotation.labanotation_utils import labanotation_to_script


color_white = (255, 255, 255)
color_black = (0, 0, 0)


class ConvertLabanScriptToView(object):
    cnt = 0
    width = 480
    height = 960
    bottom = 160
    scale = 100  # pixels/second
    img = np.array((height, width))
    name = ''
    timeOffset = 0.0
    timeScale = 1.0
    duration = 0

    # ------------------------------------------------------------------------------
    # class initialization
    # w: width; h: height; text: labanotation script
    #
    def __init__(self, w, h, text,
                 timestamps: List[int] = None,
                 imgs: List[np.ndarray] = None):
        if (text == ""):
            self.timeOffset = 0.0
            self.timeScale = 1.0
            self.width = w
            self.height = h
            self.img = np.ones((self.height, self.width), np.uint8)
            self.img = self.img * 255
            return

        l_elbow = []
        l_wrist = []
        r_wrist = []
        r_elbow = []
        head = []
        i = 0
        self.duration = 0
        self.cnt = 0
        self.name = 'labanotation view'
        laban_line = text.split("\n")

        while i < len(laban_line):  # and laban_line[i]!="":
            laban_line[i] = laban_line[i].lower()
            if laban_line[i] == "\n" or laban_line[i] == "":
                # empty line skip
                i += 1
                continue
            elif laban_line[i][0] == "#":
                # comment, skip
                i += 1
                continue
            tmp_str = laban_line[i].split(":")
            # [time, direction, level]
            if tmp_str[0] == "start time":
                if self.cnt == 0:
                    start = int(tmp_str[1])
                self.cnt += 1
                self.duration = int(tmp_str[1]) - start
                time_stamp = int(tmp_str[1]) / 1000.0
            elif tmp_str[0] == "left elbow":
                l_elbow.append([time_stamp, tmp_str[1], tmp_str[2]])
            elif tmp_str[0] == "left wrist":
                l_wrist.append([time_stamp, tmp_str[1], tmp_str[2]])
            elif tmp_str[0] == "right wrist":
                r_wrist.append([time_stamp, tmp_str[1], tmp_str[2]])
            elif tmp_str[0] == "right elbow":
                r_elbow.append([time_stamp, tmp_str[1], tmp_str[2]])
            elif tmp_str[0] == "head":
                head.append([time_stamp, tmp_str[1], tmp_str[2]])
            i += 1

        self.scale = h // (2 + self.duration // 1000)
        self.width = w
        self.height = h + self.bottom
        self.timeOffset = h
        # (h * 1000.0 / float(self.duration))
        self.timeScale = (self.scale * (self.duration / 1000.0))

        self.img = np.ones((self.height, self.width, 3), np.uint8)
        self.img = self.img * 255
        self.init_canvas()

        self.draw_limb(1, "left", l_wrist)
        self.draw_limb(2, "left", l_elbow)
        self.draw_limb(9, "right", r_elbow)
        self.draw_limb(10, "right", r_wrist)
        self.draw_limb(11, "right", head)

        if timestamps is not None:
            floor = self.height - self.bottom
            dash = 10
            for tm in timestamps:
                y = floor - (tm / 1000.0) * self.scale
                y = int(y)
                for i in range(0, (np.abs(self.width - 0)) // dash):
                    cv2.line(self.img, (self.width - i * dash, y),
                             (self.width - i * dash - dash // 2, y),
                             color_black, 2)
                if self.width - (i + 1) * dash > 0:
                    cv2.line(self.img,
                             (self.width - (i + 1) * dash, y),
                             (0, y),
                             color_black, 2)
            if imgs is not None:
                for i, (tm, img) in enumerate(zip(timestamps, imgs)):
                    if img is None:
                        continue
                    y = floor - (tm / 1000.0) * self.scale
                    y = int(y)
                    cell = 4 + (i % 4)
                    unit = self.width // 11
                    x1 = (cell - 1) * unit - 10  # left top corner
                    x2 = cell * unit + 10
                    img_width = x2 - x1
                    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    resized_img = resize_keeping_aspect_ratio(
                        img, width=img_width)
                    h, w, _ = resized_img.shape
                    top = y - h // 2
                    bottom = top + h
                    self.img[max(top, 0):bottom, x1:x2] = resized_img[
                        h - (bottom - max(top, 0)):]

    # ------------------------------------------------------------------------------
    # draw a vertical dashed line.
    def dashed(self, x1, y1, y2):
        dash = 40
        if y1 > y2:
            y1, y2 = y2, y1
        for i in range(0, (np.abs(y2 - y1)) // dash):
            cv2.line(self.img, (x1, y2 - i * dash),
                     (x1, y2 - i * dash - dash // 2), color_black, 2)
        if y2 - (i + 1) * dash > y1:
            cv2.line(self.img, (x1, y2 - (i + 1) * dash), (x1, y1),
                     color_black, 2)

    # ------------------------------------------------------------------------------
    # canvas initialization

    def init_canvas(self):
        unit = self.width // 11
        floor = self.height - self.bottom
        cv2.line(self.img, (unit * 3, 0), (unit * 3, floor), color_black, 2)
        cv2.line(self.img, (unit * 5, 0), (unit * 5, floor), color_black, 2)
        cv2.line(self.img, (unit * 7, 0), (unit * 7, floor), color_black, 2)
        cv2.line(self.img, (unit * 3, floor),
                 (unit * 7, floor), color_black, 2)
        cv2.line(self.img, (unit * 3, floor + 4),
                 (unit * 7, floor + 4), color_black, 2)
        for i in range(1, 11):
            self.dashed(unit * i, 0, floor)
        i = 0
        while True:
            x1 = unit * 5 - 3
            x2 = unit * 5 + 3
            y = floor - i * self.scale
            if y < 0:
                break
            cv2.line(self.img, (x1, y), (x2, y), color_black, 2)
            i += 1
        font = cv2.FONT_HERSHEY_SIMPLEX
        subtitle = self.height - 50
        title = self.height - 20
        cv2.putText(
            self.img,
            'lower',
            (0 * unit + 5,
             subtitle),
            font,
            0.5,
            1,
            2)
        cv2.putText(
            self.img,
            'upper',
            (1 * unit + 5,
             subtitle),
            font,
            0.5,
            1,
            2)
        cv2.putText(
            self.img,
            'upper',
            (8 * unit + 5,
             subtitle),
            font,
            0.5,
            1,
            2)
        cv2.putText(
            self.img,
            'lower',
            (9 * unit + 5,
             subtitle),
            font,
            0.5,
            1,
            2)
        cv2.putText(self.img, 'head', (10 * unit - 5, title), font, 0.8, 1, 2)
        cv2.putText(
            self.img,
            'arm(L)',
            (0 * unit + 10,
             title),
            font,
            0.8,
            1,
            2)
        cv2.putText(
            self.img,
            'arm(R)',
            (8 * unit + 10,
             title),
            font,
            0.8,
            1,
            2)
        # cv2.putText(
        #     self.img, self.name,(3*unit+10,self.height-35), font, 0.8, 1,2)

    # ------------------------------------------------------------------------------
    # draw sign of Labanotation.
    # side: right hand side, left hand side
    #     for determin which forward/backward sign should be used.
    # direction: place,
    #     forward, backward
    #     right, left
    #     right forward (diagonal), right backward (diagonal)
    #     left forward (diagonal), left backward (diagonal)
    # level: low, middle, high
    # (x1,y1) is the left top corner, (x2,y2) is the right bottom corner.
    #
    def sign(
            self,
            cell,
            xxx_todo_changeme,
            side="right",
            dire="place",
            lv="low"):
        (time1, time2) = xxx_todo_changeme
        unit = self.width // 11
        x1 = (cell - 1) * unit + 7  # left top corner
        x2 = cell * unit - 5
        y1 = self.height - self.bottom - \
            int(time2 * self.scale) + 3  # right bottom corner
        y2 = self.height - self.bottom - int(time1 * self.scale) - 3
        # shading: pattern/black/dot
        if lv == "middle":
            cv2.circle(self.img, ((x1 + x2) // 2, (y1 + y2) // 2), 4,
                       color_black, -1)
        elif lv == "high":
            step = 20
            i = 0
            while True:
                xl = x1  # start point at the left
                yl = y1 + i * step
                xr = x1 + i * step  # end point at th right
                yr = y1
                if yl > y2:
                    xl = yl - y2 + xl
                    yl = y2
                if xr > x2:
                    yr = y1 + xr - x2
                    xr = x2
                if (xl > xr) or (yr > yl):
                    break
                cv2.line(self.img, (xl, yl), (xr, yr), 0, 2)
                i += 1
        elif lv == "low":
            cv2.rectangle(self.img, (x1, y1), (x2, y2), 0, -1)
        else:
            print("Unknow Level: " + lv)
        # shape: trapezoid, polygon, triangle, rectangle
        if dire == "right":
            pts = np.array([[x1, y1 - 1], [x2 + 1, y1 - 1],
                           [x2 + 1, (y1 + y2) // 2]], np.int32)
            cv2.fillPoly(self.img, [pts], color_white)
            pts = np.array([[x1, y2 + 1], [x2 + 1, y2 + 1],
                           [x2 + 1, (y1 + y2) // 2]], np.int32)
            cv2.fillPoly(self.img, [pts], color_white)
            pts = np.array([[x1, y1], [x1, y2], [x2, (y1 + y2) // 2]],
                           np.int32)
            cv2.polylines(self.img, [pts], True, 0, 2)
        elif dire == "left":
            pts = np.array([[x1 - 1, y1 - 1], [x2, y1 - 1],
                           [x1 - 1, (y1 + y2) // 2]], np.int32)
            cv2.fillPoly(self.img, [pts], color_white)
            pts = np.array([[x1 - 1, y2 + 1], [x2, y2 + 1],
                           [x1 - 1, (y1 + y2) // 2]], np.int32)
            cv2.fillPoly(self.img, [pts], color_white)
            pts = np.array([[x1, (y1 + y2) / 2], [x2, y1], [x2, y2]],
                           np.int32)
            cv2.polylines(self.img, [pts], True, 0, 2)
        elif dire == "left forward":
            pts = np.array([[x1, y1 - 1], [x2 + 1, y1 - 1],
                           [x2 + 1, y1 + (y2 - y1) // 3]], np.int32)
            cv2.fillPoly(self.img, [pts], color_white)
            pts = np.array([[x1, y1], [x2, y1 + (y2 - y1) // 3],
                           [x2, y2], [x1, y2]], np.int32)
            cv2.polylines(self.img, [pts], True, 0, 2)
        elif dire == "right forward":
            pts = np.array([[x1 - 1, y1 - 1], [x2 + 1, y1 - 1],
                           [x1 - 1, y1 + (y2 - y1) // 3]], np.int32)
            cv2.fillPoly(self.img, [pts], color_white)
            pts = np.array([[x1, y1 + (y2 - y1) // 3], [x2, y1],
                           [x2, y2], [x1, y2]], np.int32)
            cv2.polylines(self.img, [pts], True, 0, 2)
        elif dire == "left backward":
            pts = np.array([[x1, y2 + 1], [x2 + 1, y2 + 1],
                           [x2 + 1, y2 - (y2 - y1) // 3]], np.int32)
            cv2.fillPoly(self.img, [pts], color_white)
            pts = np.array(
                [[x1, y1], [x2, y1], [x2, y2 - (y2 - y1) // 3], [x1, y2]],
                np.int32)
            cv2.polylines(self.img, [pts], True, 0, 2)
        elif dire == "right backward":
            pts = np.array([[x1 - 1, y2 + 1], [x2 + 1, y2 + 1],
                           [x1 - 1, y2 - (y2 - y1) // 3]], np.int32)
            cv2.fillPoly(self.img, [pts], color_white)
            pts = np.array([[x1, y1], [x2, y1], [x2, y2], [
                           x1, y2 - (y2 - y1) // 3]], np.int32)
            cv2.polylines(self.img, [pts], True, 0, 2)
        elif dire == "forward" and side == "right":
            cv2.rectangle(self.img, (x1 + (x2 - x1) // 2, y1 - 1),
                          (x2 + 1, y1 + (y2 - y1) // 3), color_white, -1)
            pts = np.array([[x1, y1],
                            [x1 + (x2 - x1) // 2, y1],
                            [x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 3],
                            [x2, y1 + (y2 - y1) // 3],
                            [x2, y2], [x1, y2]],
                           np.int32)
            cv2.polylines(self.img, [pts], True, 0, 2)
        elif dire == "forward" and side == "left":
            cv2.rectangle(self.img, (x1 - 1, y1 - 1),
                          (x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 3),
                          color_white, -1)
            pts = np.array([[x1, y1 + (y2 - y1) // 3],
                            [x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 3],
                            [x1 + (x2 - x1) // 2, y1],
                            [x2, y1], [x2, y2], [x1, y2]],
                           np.int32)
            cv2.polylines(self.img, [pts], True, 0, 2)
        elif dire == "backward" and side == "right":
            cv2.rectangle(self.img, (x1 + (x2 - x1) // 2, y2 -
                          (y2 - y1) // 3), (x2 + 1, y2 + 1), color_white, -1)
            pts = np.array([[x1, y1], [x2, y1], [x2, y2 -
                                                 (y2 -
                                                  y1) //
                                                 3], [x1 +
                                                      (x2 -
                                                       x1) //
                                                      2, y2 -
                                                      (y2 -
                                                          y1) //
                                                      3], [x1 +
                                                           (x2 -
                                                            x1) //
                                                           2, y2],
                            [x1, y2]], np.int32)
            cv2.polylines(self.img, [pts], True, 0, 2)
        elif dire == "backward" and side == "left":
            cv2.rectangle(self.img, (x1 - 1, y2 - (y2 - y1) // 3),
                          (x1 + (x2 - x1) // 2, y2 + 1), color_white, -1)
            pts = np.array([[x1, y1], [x2, y1], [x2, y2],
                            [x1 + (x2 - x1) // 2, y2],
                            [x1 + (x2 - x1) // 2, y2 - (y2 - y1) // 3],
                            [x1, y2 - (y2 - y1) // 3]], np.int32)
            cv2.polylines(self.img, [pts], True, 0, 2)
        elif dire == "place":  # "Place"
            cv2.rectangle(self.img, (x1, y1), (x2, y2), 0, 2)
        else:
            print("Unknow Direction: " + side + ": " + dire)

    # ------------------------------------------------------------------------------
    # draw one column of labanotation for one limb
    #
    def draw_limb(self, cell, side, laban):
        self.sign(cell, (-90.0 / self.scale, -5.0 / self.scale),
                  side, laban[0][1], laban[0][2])
        i = 1
        while i <= self.cnt - 1:
            if laban[i -
                     1][1] == laban[i][1] and laban[i -
                                                    1][2] == laban[i][2]:
                pass
            else:
                # sign(cell,(time1,time2), side="Right", dire = "Place",lv =
                # "Low"):
                self.sign(cell, (laban[i - 1][0], laban[i]
                          [0]), side, laban[i][1], laban[i][2])
            i += 1


def labanotation_to_image(timestamps: List[int],
                          labans: List[List[List[str]]],
                          imgs: List[np.ndarray] = None,
                          scale: int = 60) -> np.ndarray:
    """Convert labanotations to image.

    Parameters
    ----------
    timestamps : list[int]
        timestamp in seconds.
    labans : list[list[list[str]]]
        labanotations.
    """
    if len(timestamps) != len(labans):
        raise ValueError
    timestamps = 1000.0 * np.array(timestamps, dtype=np.float64)
    cnt = len(timestamps)
    script = labanotation_to_script(timestamps, labans)
    width = scale * 10
    height = scale * cnt
    view = ConvertLabanScriptToView(width, height, script, timestamps,
                                    imgs=imgs)
    return view.img
