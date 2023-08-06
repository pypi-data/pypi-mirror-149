import os

import numpy as np
import cv2

from skcvideo.reader import put_text, RED, WHITE


class Button(object):
    def __init__(self, hitbox, callback, data=None):
        self.hitbox = hitbox
        self.data = data
        self.given_callback = callback

    def callback(self, *kwargs):
        if self.data is None:
            return self.given_callback(*kwargs)
        else:
            return self.given_callback(self.data, *kwargs)


class ImageGenerator(object):
    def __init__(self, images_dir):
        self.to_exit = False

        self.keydict = {'k': self.next,
                        'j': self.previous,
                        'q': self.exit}

        self.buttons = []

        self.images_list = []
        for filename in os.listdir(images_dir):
            ext = os.path.splitext(filename)[1]
            if ext in ['.png', '.jpg']:
                image_path = os.path.join(images_dir, filename)
                image = cv2.imread(image_path)
                self.images_list.append(image)

        self.i = 0
        self.refresh()

        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.click_event)

    @property
    def image_to_disp(self):
        return self.big_image

    def next(self):
        if self.i < len(self.images_list) - 1:
            self.i += 1
            self.refresh()

    def previous(self):
        if self.i > 0:
            self.i -= 1
            self.refresh()

    def exit(self):
        self.to_exit = True

    def click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            if hasattr(self, 'buttons'):
                for button in self.buttons:
                    x1, y1, x2, y2 = button.hitbox
                    if x1 < x < x2 and y1 < y < y2:
                        button.callback(x, y)
            self.refresh()

    def refresh(self):
        self.big_image = np.zeros((150, 150, 3), dtype=np.uint8)

        self.image = self.images_list[self.i]

        put_text(self.big_image, 'i: {}'.format(self.i), (20, 30), WHITE)

        self.big_image[:, :75, :] = self.image

    def start(self):
        while not self.to_exit:
            cv2.imshow("image", self.image_to_disp)
            key = cv2.waitKey(1) & 0xFF
            for k, fun in self.keydict.items():
                if key == ord(k):
                    fun()


if __name__ == '__main__':
    import sys
    images_dir = sys.argv[1]

    ImageGenerator(images_dir).start()
