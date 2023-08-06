import cv2


class ImagesDirIncrustation(object):
    def __init__(self, box=[0, 575, 720, 575 + 1280], images_dir, reccurent=False):
        self.box = box

        self.images_list = []
        for filename in os.listdir(images_dir):
            ext = os.path.splitext(filename)[1]
            if ext in ['.png', '.jpg']:
                image_path = os.path.join(images_dir, filename)
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

    def refresh(self, big_image, frame):
        image = self.images_list[frame]
        self.incrust_image(big_image, image)
