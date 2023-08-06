import sys
import os
import time

import numpy as np
import cv2
import imageio

from skcvideo.utils import put_text
from skcvideo.colors import WHITE, RED


class Button(object):
    """
    Used to define a clickable button on the image executing a given callback
    when cliked. Some data specifying the button can be passed at the object
    creation. 

    Args:
        - hitbox: tuple (x1, y1, x2, y2) the bounding box of the clickable area. 
        - callback: a function taking x, y (the coordinates of the click) and
          optionnaly data as arguments.
        - data (optionnal): data of any shape that will be used by the callback.
    """
    def __init__(self, hitbox, callback, data=None):
        self.hitbox = hitbox
        self.data = data
        self.given_callback = callback

    def callback(self, *kwargs):
        if self.data is None:
            return self.given_callback(*kwargs)
        else:
            return self.given_callback(self.data, *kwargs)


class Reader(object):
    """
    A video displayer that allows interaction with the image by using buttons
    or keyboard.

    The main advantage of this displayer is that it allows to read the video
    backward while keeping relatively fast. 

    The best way to use this displayer is to make your own class inheriting
    from this one and overridding its methods. 
    """
    def __init__(self, *args, **kwargs):
        self.to_exit = False
        self.size = kwargs.get('size', (1920, 1080))
        self.min_frame = kwargs.get('min_frame', 0)
        self.max_frame = kwargs.get('max_frame', 9000)
        self.frame = self.min_frame

        self.is_playing = False
        self.max_playing_fps = kwargs.get('max_playing_fps', 10.0)
        self.playing_fps = None

        # The key/function mapping
        self.keydict = {
            'k': self.next,
            'j': self.previous,
            'q': self.exit,
            'p': self.toggle_is_playing,
        }

        # Widgets (the order of the widgets defines the order in which they
        # will be drawn)
        self.widgets = []
        for widget in kwargs.get('widgets', []):
            self.add_widget(widget)

        # The clickable buttons
        self.buttons = []

        self.background = self.build()

        self._refresh()

        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("image", 1280, 720)
        cv2.setMouseCallback("image", self.click_event)

    @property
    def image_to_disp(self):
        """
        This property specifies the image to be displayed. You would override
        it at your convenience e.g. to only display a subpart of the global
        image.
        """
        return self.big_image

    def toggle_is_playing(self):
        self.is_playing = not self.is_playing

    def next(self):
        if self.frame < self.max_frame:
            self.frame += 1
        self._refresh()

    def previous(self):
        if self.frame > self.min_frame:
            self.frame -= 1
        self._refresh()

    def jump(self, frame):
        if frame < self.min_frame:
            self.frame = self.min_frame
        elif frame >= self.max_frame:
            self.frame = self.max_frame - 1
        else:
            self.frame = frame

    def exit(self):
        self.to_exit = True

    def add_widget(self, widget):
        self.widgets.append(widget)
        widget.parent = self

    def build(self):
        """
        Here you define the elements of the image that don't change throughout
        the video or manipulations. 
        """
        im = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)
        for widget in self.widgets:
            widget.build(im)
        return im

    def click_event(self, event, x, y, flags, param):
        """
        Part of the core engine that manages the buttons.

        /!\ Should not be overridden without knowing what you do. 
        """
        if event == cv2.EVENT_LBUTTONUP:
            for button in [b for widget in [self] + self.widgets for b in getattr(widget, 'buttons', [])]:
                x1, y1, x2, y2 = button.hitbox
                if x1 < x < x2 and y1 < y < y2:
                    button.callback(x, y)
            self._refresh()

    def _refresh(self):
        """
        Here you define the appearance of the image to be displayed with
        respect to structural elements such as the frame index. 

        It is called each time the user is interacting with the image
        (clicks, keys, previous, next, ...) to allow updating it with new
        information. 
        """
        self.big_image = self.background.copy()
        self.refresh()

    def refresh(self):
        for widget in self.widgets:
            widget.refresh(self.big_image, self.frame)
        put_text(
            img=self.big_image,
            text='Frame {}'.format(self.frame),
            org=(20, 20),
            align_x='left',
            align_y='top',
        )
        if self.is_playing and self.playing_fps is not None:
            put_text(
                img=self.big_image,
                text='fps: {:.2f}'.format(self.playing_fps),
                org=(1900, 20),
                align_x='right',
                align_y='top',
            )

    def start(self):
        """
        Part of the core engine that manages the display of the image and the
        keys.

        /!\ Should not be overridden without knowing what you do. 
        """
        last_time = None
        while not self.to_exit:
            cv2.imshow("image", self.image_to_disp)
            key = cv2.waitKey(1) & 0xFF
            for k, fun in self.keydict.items():
                if key == ord(k):
                    fun()

            if self.is_playing:
                if last_time is not None:
                    spent_time = time.time() - last_time
                    if spent_time < 1 / self.max_playing_fps:
                        time.sleep(1 / self.max_playing_fps - spent_time)

                    self.playing_fps = 1 / (time.time() - last_time)
                last_time = time.time()
                self.next()

    def create_video(self, video_path='video.mp4'):
        if os.path.exists(video_path):
            print('video_path already exists, overwite (y/n)?')
            answer = input()
            if answer.lower() != 'y':
                return
        video = imageio.get_writer(video_path, 'ffmpeg', fps=10, quality=5.5)
        print('Creating video...')
        for frame in range(self.min_frame, self.max_frame):
            sys.stdout.write('\r{}/{}'.format(frame - self.min_frame, self.max_frame - self.min_frame - 1))
            sys.stdout.flush()
            self.seek(frame)
            self._refresh()
            video.append_data(cv2.cvtColor(self.big_image, cv2.COLOR_BGR2RGB))
        sys.stdout.write('\n')
        sys.stdout.flush()
        print('Done')
        video.close()


if __name__ == '__main__':
    reader = Reader()
    reader.start()
