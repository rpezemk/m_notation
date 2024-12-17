from model.audiofile import AudioFile
from utils.file_utils.os_utils import get_absolute_path
from widgets.lanes.LaneWidget import LaneWidget

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QPainter, QPen


from typing import Any, override


g_audio_ranges = [(11, 12.3), (13, 16), (17, 19.7)]

class AudioWidget(LaneWidget):
    def __init__(self):
        super().__init__()
        self.view_time_start = 10 # sec
        self.view_time_end = 20 # sec
        self.sample_file_path = "./audio_samples/harvard.wav"
        self.abs_path_sample = get_absolute_path(self.sample_file_path)
        self.audiofile = AudioFile(self.abs_path_sample)
        self.simple = self.audiofile.get_simplified(10, 10)
        self.audio_ranges = g_audio_ranges
        
    @override
    def set_content(self, data: Any):
        if isinstance(data, str):
            path = data
            self.view_time_start = 0
            self.view_time_end = 10
            self.sample_file_path = path
            self.audio_ranges = [(0, 10)]
            self.abs_path_sample = get_absolute_path(self.sample_file_path)
            self.audiofile = AudioFile(self.abs_path_sample)
            self.simple = self.audiofile.get_simplified(10, 10)
        ...

    @override
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    @override
    def paintEvent(self, event):
        self.draw_content()

    def draw_content(self):
        painter = QPainter(self)
        painter.setFont(self.bravura_font)
        painter.setPen(self.dark_gray)
        painter.setBrush(self.black)
        pen = QPen(self.very_light_gray)  # Set the pen color to black
        painter.setPen(pen)
        self.draw_lane(painter)
        # super().paintEvent(event)
        self.draw_ranges(painter)
        pen = QPen(QColor(255, 255, 255, 255))  # Set the pen color to black
        pen.setWidth(2)       # Set the stroke thickness to 5 pixels
        painter.setPen(pen)
        self.draw_data(painter)
        painter.end()

    def draw_lane(self, painter: QPainter):
        w = self.width()
        h = self.height()
        rect = QRect(0, 0, w-1, h-1)
        painter.drawRect(rect)



    def draw_ranges(self, painter: QPainter):
        w = self.width()
        h = self.height()
        painter.setBrush(self.black)

        for rng in self.audio_ranges:
            start = rng[0]
            end = rng[1]
            time_range = self.view_time_end - self.view_time_start

            x0 = int(((start - self.view_time_start)/time_range) * w)
            y0 = 5
            r_w = int(((end - start)/time_range) * w)
            r_h = h - 10

            rect = QRect(x0, y0, r_w, r_h)
            painter.drawRect(rect)


    def draw_data(self, painter: QPainter):
        w = self.width()
        h = self.height()
        painter.setBrush(self.black)

        for rng in self.audio_ranges:
            start = rng[0]
            end = rng[1]
            time_range = self.view_time_end - self.view_time_start

            x0 = int(((start - self.view_time_start)/time_range) * w)
            y0 = 5
            r_w = int(((end - start)/time_range) * w)
            r_h = h
            self.draw_range_data(painter, x0, y0, r_w, r_h)

    def draw_range_data(self, painter: QPainter, x0, y0, r_w, r_h):
        simplified = self.audiofile.get_simplified(r_h, 1)
        max__ = max(simplified) if simplified else [1]
        simplified = [(r*r_h)/max__ for r in simplified]
        lenght = len(simplified)
        cnt = 0

        for val in simplified:
            res_x0 = int(x0 + (r_w*cnt/lenght))
            val = int(val)
            painter.drawPoint(res_x0, r_h - val - 5)
            cnt += 1