import numpy as np
import cv2

from skcvideo.utils import put_text
from skcvideo.field_model import create_field_objects
from skcvideo.colors import WHITE


FIELD_COLOR = (65, 165, 113)


class Minimap(object):
    def __init__(self, box=[200, 57, 740, 57 + 796], pitch_length=105.0, pitch_width=68.0):
        self.box = box
        self.pitch_length = pitch_length
        self.pitch_width = pitch_width

        self.xc, self.yc = (self.box[1] + self.box[3]) / 2.0, (self.box[0] + self.box[2]) / 2.0
        self.w, self.h = self.box[3] - self.box[1], self.box[2] - self.box[0]
        self.pixel_per_meter = 5.0 * min(float(self.h) / 390.0, float(self.w) / 575.0)

    def build(self, image):
        image[self.box[0]:self.box[2], self.box[1]:self.box[3], :] = np.array(FIELD_COLOR, dtype=np.uint8)[np.newaxis, np.newaxis, :]

        field_objects = create_field_objects(
            pitch_length=self.pitch_length,
            pitch_width=self.pitch_width,
        )

        for name, field_object in field_objects.items():
            if field_object['type'] == 'line':
                start_x, start_y = self.switch_coords_meter_to_minimap(*field_object['start_point'])
                end_x, end_y = self.switch_coords_meter_to_minimap(*field_object['end_point'])
                cv2.line(
                    img=image,
                    pt1=(start_x, start_y),
                    pt2=(end_x, end_y),
                    color=WHITE,
                    thickness=2,
                )
            elif field_object['type'] == 'circle':
                x, y = start_point = self.switch_coords_meter_to_minimap(
                    field_object['x'],
                    field_object['y'],
                )
                radius = int(np.round(self.pixel_per_meter * field_object['radius']))
                startAngle = int(np.round(180.0 * field_object['startAngle'] / np.pi))
                endAngle = int(np.round(180.0 * field_object['endAngle'] / np.pi))

                cv2.ellipse(
                    img=image,
                    center=(x, y),
                    axes=(radius, radius),
                    angle=0,
                    startAngle=startAngle,
                    endAngle=endAngle,
                    color=WHITE,
                    thickness=2,
                )

    def switch_coords_meter_to_minimap(self, x, y):
        x_to_disp =  np.round(x * self.pixel_per_meter + self.xc)
        y_to_disp =  np.round(- y * self.pixel_per_meter + self.yc)
        x_to_disp, y_to_disp = map(int, [x_to_disp, y_to_disp])
        return x_to_disp, y_to_disp

    def refresh(self, image, data, info_mapping=lambda d: d):
        '''
        info_mapping: a function taking d and returning a dict containing:
            {
                'x': float,
                'y': float,
                'radius': int,
                'color': (int, int, int),
                'second_color': (int, int, int),
                'text': str or None,
                'text_color': (int, int, int) or None,
            }
        '''
        for d in data:
            info = info_mapping(d)
            x, y = self.switch_coords_meter_to_minimap(info['x'], info['y'])
            cv2.circle(image, (x, y), info['radius'], info['color'], thickness=-1)
            cv2.circle(image, (x, y), info['radius'], info['second_color'], thickness=1)
            if info['text'] is not None:
                put_text(
                    img=image,
                    text=info['text'],
                    org=(x, y),
                    fontScale=0.4,
                    color=info['text_color'],
                    align_x='center',
                    align_y='center',
                )
