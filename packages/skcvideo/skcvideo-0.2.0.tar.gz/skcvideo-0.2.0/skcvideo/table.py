import cv2

from skcvideo.colors import WHITE
from skcvideo.utils import put_text
from skcvideo.core import Button


class Table(object):
    def __init__(self, box=[0, 0, 1920, 1080], data=[]):
        self.row_height = 20

        self.box = box
        self.data = data
        self.selected_item = None
        self.item_offset = 0

        x1, y1, x2, y2 = self.box
        self.number_of_rows = int((y2 - y1) / self.row_height)

    def build(self, image):
        self.parent.keydict['8'] = self.up
        self.parent.keydict['2'] = self.down
        self.parent.keydict['\r'] = self.activate

        x1, y1, x2, y2 = self.box
        image[y1:y2, x1:x2] = 0
        if self.selected_item is not None:
            image[y1 + self.selected_item * self.row_height:y1 + (self.selected_item + 1) * self.row_height, x1:x2] = 128

        cv2.rectangle(image, (x1, y1), (x2, y2), color=WHITE, thickness=2)

        self.buttons = []
        for i, y in enumerate(range(y1, y2, self.row_height)):
            cv2.line(image, (x1, y), (x2, y), color=WHITE, thickness=1)

            button = Button((x1, y, x2, y + self.row_height), self.select, data=i)
            self.buttons.append(button)

        for i in range(self.number_of_rows):
            if i + self.item_offset >= len(self.data):
                continue
            d = self.data[i + self.item_offset]
            y = int(round(y1 + (i + 0.5) * self.row_height))
            put_text(
                image,
                self.format_text(d),
                (x1 + 5, y),
                fontScale=0.5,
                align_x='left',
                align_y='center',
            )

    def format_text(self, d):
        return d['text']

    def select(self, i, *args, **kwargs):
        self.selected_item = i
        self.build(self.parent.background)

    def up(self):
        if self.selected_item is not None:
            if self.selected_item > 0:
                self.select(self.selected_item - 1)
            elif self.selected_item == 0 and self.item_offset > 0:
                self.item_offset -= 1
                self.build(self.parent.background)
            self.parent._refresh()

    def down(self):
        if self.selected_item is not None:
            if self.selected_item < self.number_of_rows - 1:
                self.select(self.selected_item + 1)
            elif self.selected_item == self.number_of_rows - 1 and self.item_offset < len(self.data) - self.number_of_rows:
                self.item_offset += 1
                self.build(self.parent.background)
            self.parent._refresh()

    def activate(self):
        """
        Example of usage : 

        if self.selected_item is not None:
            self.parent.jump(self.data[self.selected_item]['frame'])
            self.parent._refresh()
        """
        pass

    def refresh(self, image, frame):
        pass
