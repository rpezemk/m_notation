from typing import override
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QPainter, QPen

from widgets.lanes.LaneWidget import LaneWidget
from widgets.compound.stack_panels import HStack, VStack


class RulerWidget(LaneWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(40)
        
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
        self.draw_frame(painter)
        # super().paintEvent(event)
        pen = QPen(QColor(255, 255, 255, 80))  # Set the pen color to black
        painter.setPen(pen)
        pen.setWidth(1)       # Set the stroke thickness to 5 pixels
        painter.end()

    def draw_frame(self, painter: QPainter):
        w = self.width()
        h = self.height()
        rect = QRect(0, 0, w-1, h-1)
        painter.drawRect(rect)