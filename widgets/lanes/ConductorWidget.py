from typing import Any, override
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QPainter, QPen

from model.structure import TempoMark
from widgets.lanes.BarrableWidget import BarrableWidget
from widgets.lanes.LaneWidget import LaneWidget
from widgets.compound.stack_panels import HStack, VStack


class RulerWidget(BarrableWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(40)
        
    @override
    def paintEvent(self, event):
        self.draw_content()

    @override
    def set_content(self, measures):
        self.measures = measures
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
        print("bar_segments:")
        for m_no, bar in enumerate(self.measures):
            seg_start = bar_segments[m_no][0]
            seg_end = bar_segments[m_no][1]
            print(seg_start, seg_end)
            if seg_end - seg_start < 10:
                continue
            self.draw_bar_frame(painter, seg_start, seg_end)
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
    