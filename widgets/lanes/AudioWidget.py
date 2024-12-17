from model.audiofile import AudioFile
from utils.file_utils.os_utils import get_absolute_path
from widgets.painters.audio_painter import AudioPainter
from widgets.lanes.LaneWidget import LaneWidget

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QPen
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
        pen = QPen(self.very_light_gray)  # Set the pen color to black
        self.draw_lane()
        self.draw_all_data()
        
        
    def draw_lane(self):
        painter = QPainter(self)
        painter.setPen(self.dark_gray)
        painter.setBrush(self.black)
        w = self.width()
        h = self.height()
        rect = QRect(0, 0, w-1, h-1)
        painter.drawRect(rect)
        painter.end()
        
    def draw_all_data(self):
        for rng in self.audio_ranges:
            start = rng[0]
            end = rng[1]
            AudioPainter().draw(self, self.view_time_start, self.view_time_end, start, end, self.audiofile)


