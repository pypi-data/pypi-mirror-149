import sys
import os

import numpy as np
import cv2
import imageio

from skcvideo.video_capture import StoredImagesVideoCapture
from skcvideo.video_incrustation import VideoIncrustation
from skcvideo.timeline import Timeline, VlcTimeline
from skcvideo.minimap import Minimap
from skcvideo.utils import put_text
from skcvideo.colors import BLACK, WHITE, RED


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


class Reader(StoredImagesVideoCapture):
    """
    A video displayer that allows interaction with the image by using buttons
    or keyboard.

    The main advantage of this displayer is that it allows to read the video
    backward while keeping relatively fast. 

    The best way to use this displayer is to make your own class inheriting
    from this one and overridding its methods. 
    """
    def __init__(self, video_path, timeline=None, **kwargs):
        super(Reader, self).__init__(video_path, colormap='bgr', **kwargs)

        self.to_exit = False

        # The key/function mapping
        self.keydict = {
            'k': self.next,
            'j': self.previous,
            'q': self.exit,
        }

        # The clickable buttons
        self.buttons = []

        if not hasattr(self, 'video_incrustation'):
            self.video_incrustation = None

        if not hasattr(self, 'minimap'):
            self.minimap = Minimap(
                box=[200, 0, 590, 575],
                pitch_length=105.0,
                pitch_width=68.0,
            )

        if not hasattr(self, 'timeline'):
            self.timeline = VlcTimeline(
                box=[79, 1771],
                parent=self,
            )

        self.buttons.append(Button(self.timeline.hitbox, self.jump_event))

        self.background = self.create_background()

        self.init(video_path, **kwargs)

        self._refresh()

        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("image", 1280, 720)
        cv2.setMouseCallback("image", self.click_event)

    def init(self, video_path, **kwargs):
        pass

    @property
    def image_to_disp(self):
        """
        This property specifies the image to be displayed. You would override
        it at your convenience e.g. to only display a subpart of the global
        image.
        """
        return self.big_image

    def next(self):
        super(Reader, self).next()
        self._refresh()

    def previous(self):
        super(Reader, self).previous()
        self._refresh()

    def exit(self):
        self.to_exit = True

    def create_background(self):
        """
        Here you define the elements of the image that don't change throughout
        the video or manipulations. 
        """
        im = np.zeros((980, 1855, 3), dtype=np.uint8)
        if self.video_incrustation is not None:
            self.video_incrustation.build(im)
        self.minimap.build(im)
        self.timeline.build(im)
        im = self.draw_background(im)
        return im

    def draw_background(self, im):
        return im

    def timeline_color(self, frame):
        """
        Here you define the color of the timeline with repect to the frame.
        """
        return (0, 0, 0)

    def jump_event(self, x, y, *kwargs):
        frame = self.timeline.get_frame(x, y)
        self.jump(frame)

    def click_event(self, event, x, y, flags, param):
        """
        Part of the core engine that manages the buttons.

        /!\ Should not be overridden without knowing what you do. 
        """
        if event == cv2.EVENT_LBUTTONUP:
            if hasattr(self, 'buttons'):
                for button in self.buttons:
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
        put_text(
            img=self.big_image,
            text='Frame {}'.format(self.frame),
            org=(20, 20),
            align_x='left',
            align_y='top',
        )
        self.timeline.refresh(self.big_image, self.frame)
        if self.video_incrustation is not None:
            self.video_incrustation.refresh(self.big_image, self.image.copy())
        self.minimap.refresh(self.big_image, [])

    def start(self):
        """
        Part of the core engine that manages the display of the image and the
        keys.

        /!\ Should not be overridden without knowing what you do. 
        """
        while not self.to_exit:
            cv2.imshow("image", self.image_to_disp)
            key = cv2.waitKey(1) & 0xFF
            for k, fun in self.keydict.items():
                if key == ord(k):
                    fun()

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
    import sys
    video_path = sys.argv[1]
    reader = Reader(video_path, fps=10)
    reader.start()
