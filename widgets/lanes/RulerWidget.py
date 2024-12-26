from typing import override
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QPainter, QPen

from model.ratio import Ratio
from model.chunk import Chunk
from widgets.lanes.BarrableWidget import BarrableWidget

class RulerWidget(BarrableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(40)
        self.ruler_bars = []
        self.chunk = None
        self.m_no = 0
        self.e_no = 0
        
    @override
    def paintEvent(self, event):
        self.draw_content()
        self.update()
        
    @override
    def set_content(self, chunk: Chunk):
        self.chunk = chunk
        self.ruler_bars = chunk.to_ruler_bars()
        
        ...

    def mark_at(self, m_no: int, e_no: int):
        self.m_no = m_no
        self.e_no = e_no

    def draw_content(self):
        painter = QPainter(self)
        painter.setFont(self.bravura_font)
        painter.setPen(self.dark_gray)
        painter.setBrush(self.black)
        pen = QPen(self.very_light_gray)
        painter.setPen(pen)
        self.draw_frame(painter)
        pen = QPen(QColor(255, 255, 255, 80))
        painter.setPen(pen)
        self.y_offsets = self.get_x_offsets()
        bar_segments = self.get_h_segments()
        self.visual_notes = []
        
        for m_no, ruler_bar in enumerate(self.ruler_bars):
            seg_start = bar_segments[m_no][0]
            seg_end = bar_segments[m_no][1]
            if seg_end - seg_start < 10:
                continue
            curr_x = 0
            for r_e in ruler_bar:
                curr_x = r_e.offset_ratio.to_float() * (seg_end - seg_start) + seg_start
                self.draw_bar_frame(painter, int(curr_x), int(curr_x) + 1)
        
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setPen(self.light_gray)
        painter.setBrush(self.light_gray)
        self.draw_marked(painter)  
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
        
    def draw_marked(self, painter: QPainter):
        e = self.ruler_bars[self.m_no][self.e_no]
        seg = self.get_h_segments()[self.m_no]
        seg_start = seg[0]
        seg_end = seg[1]
        curr_x = e.offset_ratio.to_float() * (seg_end - seg_start) + seg_start
        self.draw_bar_frame(painter, int(curr_x)-5, int(curr_x) + 5)
