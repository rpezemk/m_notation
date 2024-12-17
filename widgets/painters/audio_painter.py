from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QWidget

from model.audiofile import AudioFile

class AudioPainter():
    def __init__(self):
        self.dark_gray = QColor(100, 100, 100)
        self.light_gray = QColor(140, 140, 140)
        self.very_light_gray = QColor(160, 160, 160)
        self.light_black = QColor(13, 13, 13)
        self.black = QColor(0, 0, 0)

    def draw(self, qwidget: QWidget, view_time_start: float, view_time_end: float, start, end, audiofile: AudioFile):
        w = qwidget.width()
        h = qwidget.height()
        painter = QPainter(qwidget)
        painter.setPen(self.dark_gray)
        painter.setBrush(self.black)
        time_range = view_time_end - view_time_start
        x0 = int(((start - view_time_start)/time_range) * w)
        y0 = 5
        r_w = int(((end - start)/time_range) * w)
        r_h = h - 10

        rect = QRect(x0, y0, r_w, r_h)
        painter.setPen(self.very_light_gray)
        painter.drawRect(rect)
        simplified = audiofile.get_simplified(10, 10)
        max__ = max(simplified) if simplified else [1]
        normalized = [(r*r_h)/max__ for r in simplified]
        lenght = len(normalized)
        cnt = 0

        for val in normalized:
            res_x0 = int(x0 + (r_w*cnt/lenght))
            val = int(val)
            painter.drawPoint(res_x0, r_h - val - 5)
            cnt += 1

        painter.end()