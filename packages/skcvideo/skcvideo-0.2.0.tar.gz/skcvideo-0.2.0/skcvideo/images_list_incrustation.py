import os

import numpy as np
import cv2


class ImagesListIncrustation(object):
    def __init__(self, box=[0, 575, 720, 575 + 1280], images_paths=None, shuffle=False, maximum_length=None):
        self.box = box
        self.images_paths = images_paths

        if shuffle:
            indices = np.random.permutation(len(self.images_paths))
            if maximum_length is not None:
                indices = indices[:maximum_length]
            self.images_paths = [self.images_paths[i] for i in indices]
        elif maximum_length is not None:
            self.images_paths = self.images_paths[:maximum_length]

        self.image_name_to_i = {}
        for i, image_path in enumerate(self.images_paths):
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            self.image_name_to_i[image_name] = i

        self.images_list = []
        for image_path in self.images_paths:
            image = cv2.imread(image_path)
            self.images_list.append(image)

    def build(self, *args, **kwargs):
        pass

    def incrust_image(self, big_image, image):
        y1, x1, y2, x2 = self.box
        box_height, box_width = y2 - y1, x2 - x1
        im_height, im_width = image.shape[:2]
        if im_height != box_height or im_width != box_width:
            image = cv2.resize(image, (box_width, box_height))
        big_image[y1:y2, x1:x2, :] = image

    def process_image(image, frame):
        return image

    def refresh(self, big_image, frame):
        image = self.images_list[frame].copy()
        image = self.process_image(image, frame)
        self.incrust_image(big_image, image)

    def get_image_path(self, frame):
        return self.images_paths[frame]

    def get_frame(self, image_name):
        return self.image_name_to_i.get(image_name, None)
