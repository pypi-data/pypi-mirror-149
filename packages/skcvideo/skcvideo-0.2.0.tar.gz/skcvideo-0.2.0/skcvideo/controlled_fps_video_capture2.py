import math
import logging

import cv2


class ControlledFPSVideoCapture(object):
    """
    VideoCapture Reader from any input fps to any output fps.
    Has been tested with output_fps=10 and input_fps=10, 25, 30, 50, 60
    Note that input frame and output frame are the last decoded frames
    While cap.get(cv2.CAP_PROP_POS_FRAMES) is next frame to be read

    This class aims to simulate the result of downsampling by ffmpeg
    directly by reading the original video. This avoid having to store
    multiple versions of the video. 
    """
    def __init__(self, *args, **kwargs):
        logger = kwargs.pop('logger', logging.getLogger(__name__))

        self.input_frame = -1
        self.output_frame = -1
        self.output_fps = kwargs.pop('fps', 10)

        self._cap = cv2.VideoCapture(*args, **kwargs)
        # We round fps cause sometimes opencv gives fps like 25.00001429630351 while ffmpeg gives 25
        # Still don't know if we have correct behaviour for weird fps like 29.97
        self.input_fps = self._cap.get(cv2.CAP_PROP_FPS)

        if self.output_fps == 'same':
            self.output_fps = self.input_fps

        message = 'Initializing ControlledFPSVideoCapture with input_fps={} and output_fps={}'.format(
                self.input_fps, self.output_fps)
        print(message)
        logger.info(message)

    def read(self):
        self.output_frame += 1
        if self.output_fps == self.input_fps:
            self.input_frame += 1
            return self._cap.read()

        # This general case do not work with output_fps == input_fps (weird case output_frame == 2)
        if self.output_frame < 2:
            # Do not understand why but that's what ffmpeg does
            frames_to_get = 1
        else:
            target_input_frame = round(self.output_frame / self.output_fps * self.input_fps)

        while self.input_frame < target_input_frame:
            self.input_frame += 1
            ret, im = self._cap.read()
            if ret is False:
                return ret, im
        return ret, im

    def get(self, prop_id):
        if prop_id == cv2.CAP_PROP_BUFFERSIZE:
            raise NotImplementedError
        elif prop_id == cv2.CAP_PROP_FPS:
            return self.output_fps
        elif prop_id == cv2.CAP_PROP_POS_FRAMES:
            return self.output_frame + 1
        elif prop_id == cv2.CAP_PROP_POS_MSEC:
            return 1000 * float(self.output_frame + 1) / self.output_fps
        elif prop_id == cv2.CAP_PROP_FRAME_COUNT:
            return int(math.floor(float(self._cap.get(prop_id)) / self.input_fps * self.output_fps))
        else:
            return self._cap.get(prop_id)

    def set(self, prop_id, value):
        if prop_id in [cv2.CAP_PROP_BUFFERSIZE, cv2.CAP_PROP_FPS, cv2.CAP_PROP_FRAME_COUNT]:
            raise NotImplementedError
        elif prop_id in [cv2.CAP_PROP_POS_FRAMES, cv2.CAP_PROP_POS_MSEC, cv2.CAP_PROP_POS_AVI_RATIO]:
            if prop_id == cv2.CAP_PROP_POS_FRAMES:
                if value < 0:
                    value = 0
                output_frame = value - 1
            elif prop_id == cv2.CAP_PROP_POS_MSEC:
                output_frame = round(float(value * self.output_fps) / 1000) - 1
            elif prop_id == cv2.CAP_PROP_AVI_RATIO:
                output_frame = round(self.get(cv2.CAP_PROP_FRAME_COUNT) * cv2.CAP_PROP_POS_AVI_RATIO) - 1
            self.output_frame = output_frame
            fps_ratio = float(self.input_fps) / self.output_fps
            if fps_ratio == 1.0 or output_frame < 2:
                self.input_frame = self.output_frame
            else:
                self.input_frame = math.floor(output_frame*fps_ratio) - math.floor(fps_ratio + 1)
            return self._cap.set(prop_id, self.input_frame + 1)
        else:
            return self._cap.set(prop_id, value)

    def generator(self):
        while True:
            ret, im = self.read()
            if ret is False:
                raise StopIteration
            yield im

    def release(self):
        return self._cap.release()

    def isOpened(self):
        return self._cap.isOpened()

    def retrieve(self):
        return self._cap.retrieve()

    def open(self, *args, **kwargs):
        """ Could be implemented but we don't use it """
        raise NotImplementedError

    def grab(self):
        """ Could be implemented but we don't use it """
        raise NotImplementedError
