from typing import Callable
from fonts.glyphs import Glyphs
from model.musical.structure import HorizontalChunk, Note, Rest, VisualNote
from widgets.lanes.BarrableWidget import BarrableWidget
from widgets.lanes.StaffWidget import VirtualStaff
from PyQt5.QtWidgets import QWidget

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter


class DrawableWidget(QWidget):
    def __init__(self, parent=None, redraw_func: Callable[[int, QWidget],None] = None, staffs: list[VirtualStaff] = None):
        super().__init__(parent=parent)
        self.staff_widget = parent
        self.setCursor(Qt.CrossCursor)
        self.res_mtuples: list[list[VisualNote]] = []
        self.staff_offset = 30
        self.redraw_func = redraw_func

        self.visual_notes: list[VisualNote] = []
        self.notes = []
        self.note_size = 120
        self.line_spacing = 10
        self.staffs = staffs if staffs else []

    def paintEvent(self, event):
        if self.width() < 30 or self.height() < 30:
            return
        painter = QPainter(self)
        if self.redraw_func:
            self.redraw_func(self.width(), self)
        painter.end()

    def mousePressEvent(self, event):
        for staff in self.staffs:
                staff.mouse_press(event)
        self.update()