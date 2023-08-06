import numpy as np
import cv2

from skcvideo.utils import put_text
from skcvideo.colors import WHITE, RED
from skcvideo.core import Button


class Timeline(object):
    def __init__(self, box=[955, 110, 1035, 1910], timeline_width=20, margin=5):
        self.name = 'Timeline'
        self.box = box

        self.timeline_width = timeline_width
        self.margin = margin
        self.gap = self.timeline_width + 2 * self.margin

        self.timeline_length = self.box[3] - self.box[1]

        self.hitbox = (self.box[1], self.box[0], self.box[3], self.box[2])
        self.buttons = [Button(self.hitbox, self.jump_event)]

    @property
    def min_frame(self):
        return getattr(self.parent, 'min_frame', 0)

    @property
    def max_frame(self):
        return getattr(self.parent, 'max_frame', 9000)

    @property
    def n_timelines(self):
        return (self.max_frame - self.min_frame) // self.timeline_length + 1

    def jump_event(self, x, y, *kwargs):
        frame = self.get_frame(x, y)
        self.parent.jump(frame)

    def timeline_color(self, frame):
        """
        Here you define the color of the timeline with repect to the frame.
        """
        return (0, 0, 0)

    def build(self, image):
        '''
        Draws the timeline's background composed of several timeline lines
        with box and graduations.
        '''
        # Puts time labels label
        put_text(
            img=image,
            text='min',
            org=(self.box[1] - 90, self.box[0] - self.margin - self.timeline_width // 2),
            fontScale=0.6,
            align_x='left',
        )

        # Draws graduations labels
        for frame in range(0, self.box[3] - self.box[1], 100):
            if (frame + 1) % 600 == 0:
                put_text(
                    img=image,
                    text='{}min'.format((frame + 1) // 600),
                    org=(self.box[1] + frame, self.box[0] - self.margin - self.timeline_width // 2 - 2),
                    fontScale=0.6,
                    align_x='center',
                )
            else:
                put_text(
                    img=image,
                    text='{}s'.format((frame + 1) % 600 // 10),
                    org=(self.box[1] + frame, self.box[0] - self.margin - self.timeline_width // 2 + 4),
                    fontScale=0.4,
                    align_x='center',
                )

        # Draws each timeline's line
        for i in range(self.n_timelines):
            self.draw_timeline_box(image, i)

        # Draws graduations
        for frame in range(self.max_frame - self.min_frame):
            x = frame % self.timeline_length
            y = frame // self.timeline_length

            # A small mark every 5 seconds
            if ((frame + 1) % 50) == 0:
                cv2.line(
                    image,
                    (self.box[1] + x, self.box[0] + y * self.gap + self.margin - 1),
                    (self.box[1] + x, self.box[0] + (y + 1) * self.gap - self.margin + 1),
                    color=WHITE,
                    thickness=1,
                )

            # A big mark every minute
            if ((frame + 1) % 600) == 0:
                cv2.line(
                    image,
                    (self.box[1] + x, self.box[0] + y * self.gap + self.margin - 3),
                    (self.box[1] + x, self.box[0] + (y + 1) * self.gap - self.margin + 3),
                    color=WHITE,
                    thickness=2,
                )

        self.draw_timeline_data(image)

    def refresh(self, image, frame):
        self.draw_timer(image, frame)

    def draw_timeline_box(self, image, i):
        '''
        Draws one line of the timeline's background, which consists in a
        simple white box. 
        '''
        # Manage the offset
        y_min =  self.box[0] + self.margin + i * self.gap
        y_max = y_min + self.timeline_width

        # The last box may not go up to the end.
        if i == self.n_timelines - 1:
            frame_max = (self.max_frame - self.min_frame) % self.timeline_length
            timeline_max = self.box[1] + frame_max
        else:
            timeline_max = self.box[3]

        # Draws the box
        cv2.rectangle(
            image,
            (self.box[1], y_min),
            (timeline_max, y_max),
            color=WHITE,
            thickness=1,
        )

        # Adds a time label before the line
        put_text(
            img=image,
            text='{}-{}'.format(3 * i, 3 * (i + 1)),
            org=(self.box[1] - 90, (y_min + y_max) // 2),
            fontScale=0.6,
            align_x='left',
        )

    def draw_timeline_data(self, im):
        """
        Draws information on the timeline. Useful to have a global view of
        your data or to have a reference for jumping in the video. 
        """
        for frame in range(self.min_frame, self.max_frame):
            self.draw_one_timeline_data(im, frame)

    def draw_one_timeline_data(self, im, frame):
        '''
        Colors the given frame on the timeline according to the timeline_color
        function
        '''
        color = self.timeline_color(frame)
        if color != (0, 0, 0):
            timer = frame - self.min_frame
            timer_x = timer % self.timeline_length
            timer_y = timer // self.timeline_length
            cv2.line(
                im,
                (self.box[1] + timer_x, timer_y * self.gap + self.box[0] + self.margin + 1),
                (self.box[1] + timer_x, timer_y * self.gap + self.box[0] + self.margin + self.timeline_width - 1),
                color=color,
            )

    def draw_timer(self, image, frame):
        '''
        Draws a timer on the timeline on the given frame. To be used in the
        refresh method of the parent Reader class. 
        '''
        timer = frame - self.min_frame
        timer_x = timer % self.timeline_length
        timer_y = timer // self.timeline_length
        cv2.line(
            image,
            (self.box[1] + timer_x, timer_y * self.gap + self.box[0]),
            (self.box[1] + timer_x, (timer_y + 1) * self.gap + self.box[0]),
            color=WHITE,
            thickness=3,
        )
        cv2.line(
            image,
            (self.box[1] + timer_x, timer_y * self.gap + self.box[0]),
            (self.box[1] + timer_x, (timer_y + 1) * self.gap + self.box[0]),
            color=RED,
            thickness=2,
        )

    def get_frame(self, x, y):
        '''
        Returns the frame corresponding to a given pixel of the timeline.
        It is used to be able to click one the timeline to jump to a
        particular frame.
        '''
        x = x - self.box[1]
        y = (y - self.box[0]) // self.gap
        frame = x + y * self.timeline_length + self.min_frame
        return frame


GRAY_BAR = np.array(
    [
        [189, 189, 190],
        [193, 193, 194],
        [196, 197, 198],
        [200, 201, 202],
        [204, 205, 206],
        [208, 208, 209],
        [212, 212, 213],
        [215, 216, 217],
        [219, 220, 221],
        [235, 235, 236],
    ],
)

BLUE_BAR = np.array(
    [
        [224, 137, 44],
        [218, 134, 43],
        [213, 130, 42],
        [207, 127, 41],
        [204, 125, 40],
        [204, 125, 40],
        [204, 125, 40],
        [204, 125, 40],
    ],
)


class VlcTimeline(object):
    def __init__(self, box=[79, 966, 1771, 976]):
        """
        Args:
            box: list [x1, y1, x2, y2]
        """
        self.box = box
        self.buttons = [Button(self.box, self.jump_event)]
        self.timeline_length = float(self.box[2] - self.box[0])

    @property
    def min_frame(self):
        return getattr(self.parent, 'min_frame', 0)

    @property
    def max_frame(self):
        return getattr(self.parent, 'max_frame', 9000)

    @property
    def frames_length(self):
        return float(self.max_frame - self.min_frame)

    def jump_event(self, x, y, *kwargs):
        frame = self.get_frame(x, y)
        self.parent.jump(frame)

    def build(self, image):
        image[self.box[1]:self.box[1] + 18] = np.array([240, 241, 242])[np.newaxis, np.newaxis, :]
        image[self.box[1] + 4:self.box[1] + 14, self.box[0]:self.box[2]] = GRAY_BAR[:, np.newaxis, :]

    def refresh(self, image, frame):
        self.draw_timer(image, frame)

    def draw_timer(self, image, frame):
        frame = float(frame - self.min_frame)
        i = int(np.round(frame / self.frames_length * self.timeline_length))
        image[self.box[1] + 5:self.box[1] + 13, self.box[0]:self.box[0] + i] = BLUE_BAR[:, np.newaxis, :]

    def get_frame(self, x, y):
        x = float(x - self.box[0])
        frame = int(np.round(x / self.timeline_length * self.frames_length)) + self.min_frame
        return frame
