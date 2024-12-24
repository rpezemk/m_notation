from typing import override
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QPainter, QPen

from utils.musical_layout.Ratio import Ratio
from widgets.lanes.BarrableWidget import BarrableWidget
from utils.musical_layout.precise_aftermath import ratio_lanes_to_ruler, chunk_widths_by_duration


class RulerWidget(BarrableWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(40)

    @override
    def paintEvent(self, event):
        self.draw_content()

    @override
    def set_content(self, mov: list[Ratio], widths: list[Ratio]):
        self.moving_sum = mov
        
        self.measures: list[list[Ratio]] = chunk_widths_by_duration(widths, Ratio(t=(4, 4)))
        
        ...

    def draw_content(self):
        painter = QPainter(self)
        painter.setFont(self.bravura_font)
        painter.setPen(self.dark_gray)
        painter.setBrush(self.black)
        pen = QPen(self.very_light_gray)
        painter.setPen(pen)
        self.draw_frame(painter)
        # super().paintEvent(event)
        pen = QPen(QColor(255, 255, 255, 80))
        painter.setPen(pen)
        pen.setWidth(1)
        self.y_offsets = self.get_x_offsets()
        bar_segments = self.get_h_segments()
        self.visual_notes = []
        
        for m_no, bar in enumerate(self.measures):
            seg_start = bar_segments[m_no][0]
            seg_end = bar_segments[m_no][1]
            if seg_end - seg_start < 10:
                continue
            self.draw_bar_frame(painter, seg_start, seg_end)
            curr_x = 0
            for r in bar:
                n = r.numerator
                d = r.denominator 
                curr_x += n/d * (seg_end - seg_start)
                self.draw_bar_frame(painter, int(curr_x) + seg_start, int(curr_x) + seg_start + 3)
                
        painter.end()

    def draw_frame(self, painter: QPainter):
        w = self.width()
        h = self.height()
        rect = QRect(0, 0, w-1, h-1)
        painter.drawRect(rect)

    def draw_bar_frame(self, painter: QPainter, x0, x1):
        w = self.width()
        h = self.height() - 5
        rect = QRect(x0, 2, x1 - x0, h-3)
        painter.drawRect(rect)