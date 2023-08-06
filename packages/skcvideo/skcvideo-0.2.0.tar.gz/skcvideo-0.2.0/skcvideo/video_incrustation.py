import numpy as np
import cv2

from skcvideo.video_capture import StoredImagesVideoCapture


class VideoIncrustation(StoredImagesVideoCapture):
    def __init__(self, video_path, box=[0, 575, 720, 575 + 1280], **kwargs):
        self.box = box
        colormap = kwargs.get('colormap', 'bgr')
        super(VideoIncrustation, self).__init__(video_path, colormap=colormap, **kwargs)
        self.max_frame = self.get_max_frame()

    def build(self, *args, **kwargs):
        pass

    def get_image(self, frame):
        if frame >= self.max_frame:
            y1, x1, y2, x2 = self.box
            box_height, box_width = y2 - y1, x2 - x1
            image = np.zeros((box_height, box_width, 3), dtype=np.uint8)
        else:
            image = self.seek(frame).copy()
        return image

    def process_image(self, image, frame):
        return image

    def incrust_image(self, big_image, image):
        y1, x1, y2, x2 = self.box
        box_height, box_width = y2 - y1, x2 - x1
        im_height, im_width = image.shape[:2]
        if im_height != box_height or im_width != box_width:
            image = cv2.resize(image, (box_width, box_height))
        big_image[y1:y2, x1:x2, :] = image

    def refresh(self, big_image, frame):
        image = self.get_image(frame)
        image = self.process_image(image, frame)
        self.incrust_image(big_image, image)
