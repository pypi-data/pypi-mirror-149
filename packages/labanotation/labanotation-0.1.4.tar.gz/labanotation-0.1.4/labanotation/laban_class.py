valid_levels = ('high', 'middle', 'low')
valid_directions = ('forward',
                    'right forward', 'right', 'right backward',
                    'backward',
                    'left backward', 'left', 'left forward',
                    'place')


class Labanotation(object):

    def __init__(self, direction='forward', level='middle'):
        self.level = level
        self.direction = direction

    @property
    def level(self):
        return self._level

    @property
    def direction(self):
        return self._direction

    @level.setter
    def level(self, level):
        level = level.lower()
        if level not in valid_levels:
            raise ValueError(f'Invalid level({level}) given. '
                             f"{valid_levels} are valid.")
        self._level = level

    @direction.setter
    def direction(self, direction):
        direction = direction.lower()
        if direction not in valid_directions:
            raise ValueError(f'Invalid direction({direction}) given. '
                             f"{valid_directions} are valid.")
        self._direction = direction

    def tolist(self):
        return [self.direction, self.level]


class LabanotationGroup(object):

    def __init__(self,
                 right_elbow=Labanotation(),
                 right_wrist=Labanotation(),
                 left_elbow=Labanotation(),
                 left_wrist=Labanotation(),
                 head=None):
        self.right_elbow = right_elbow
        self.right_wrist = right_wrist
        self.left_elbow = left_elbow
        self.left_wrist = left_wrist
        self.head = head

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = []
        if self.head is not None:
            s.append(f'Head:{self.head.direction}{self.head.level}')
        s += [
            f'Right Elbow:{self.right_elbow.direction}:{self.right_elbow.level}',  # NOQA
            f'Right Wrist:{self.right_wrist.direction}:{self.right_wrist.level}',  # NOQA
            f'Left Elbow:{self.left_elbow.direction}:{self.left_elbow.level}',  # NOQA
            f'Left Wrist:{self.left_wrist.direction}:{self.left_wrist.level}',  # NOQA
        ]
        return '\n'.join(s)

    def right_str(self):
        return "_".join(
            [self.right_elbow.direction,
             self.right_elbow.level,
             self.right_wrist.direction,
             self.right_wrist.level]).replace(' ', '_').lower()

    def left_str(self):
        return "_".join(
            [self.left_elbow.direction,
             self.left_elbow.level,
             self.left_wrist.direction,
             self.left_wrist.level]).replace(' ', '_').lower()

    def tolist(self):
        return [self.right_elbow.tolist(),
                self.right_wrist.tolist(),
                self.left_elbow.tolist(),
                self.left_wrist.tolist()]

    @staticmethod
    def from_list(xlst):
        right_elbow = Labanotation(xlst[0][0], xlst[0][1])
        right_wrist = Labanotation(xlst[1][0], xlst[1][1])
        left_elbow = Labanotation(xlst[2][0], xlst[2][1])
        left_wrist = Labanotation(xlst[3][0], xlst[3][1])
        return LabanotationGroup(right_elbow,
                                 right_wrist,
                                 left_elbow,
                                 left_wrist)
