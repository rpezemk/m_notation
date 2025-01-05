from typing import Callable
from fonts.glyphs import Glyphs
from model.musical.structure import HorizontalChunk, Note, Rest
from widgets.lanes.BarrableWidget import BarrableWidget
from widgets.note_widgets.VisualNote import VisualNote
from widgets.painters.paint_manager import m_paint_tuple, m_paint_visual


from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter


class DrawableWidget(BarrableWidget):
    def __init__(self, parent=None, redraw_func: Callable[[QPainter, int],None] = None):
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


    def paintEvent(self, event):
        if self.width() < 30 or self.height() < 30:
            return
        painter = QPainter(self)
        # painter.setFont(self.bravura_font)
        # painter.setPen(self.very_dark_gray)
        # painter.setBrush(self.very_dark_gray)

        # painter.setPen(self.light_gray)
        # painter.setBrush(self.light_gray)
        if self.redraw_func:
            self.redraw_func(painter, self.width())
        painter.end()
