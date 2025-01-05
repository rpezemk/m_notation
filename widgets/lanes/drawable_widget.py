from fonts.glyphs import Glyphs
from model.musical.structure import HorizontalChunk, Note, Rest
from widgets.lanes.BarrableWidget import BarrableWidget
from widgets.note_widgets.VisualNote import VisualNote
from widgets.painters.paint_manager import m_paint_tuple, m_paint_visual


from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter


class DrawableWidget(BarrableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.staff_widget = parent
        self.setCursor(Qt.CrossCursor)
        self.res_mtuples: list[list[VisualNote]] = []
        self.staff_offset = 30


        self.visual_notes: list[VisualNote] = []
        self.notes = []
        self.note_size = 120
        self.line_spacing = 10

    def set_content(self, h_chunk: HorizontalChunk):
        self.measures = h_chunk.measures

    def paintEvent(self, event):
        self.no_of_measures = len(self.measures)
        if self.width() < 30 or self.height() < 30:
            return
        self.draw_content()

    def draw_content(self):
        painter = QPainter(self)
        painter.setFont(self.bravura_font)
        painter.setPen(self.dark_gray)
        painter.setBrush(self.dark_gray)

        self.draw_clef(painter)
        self.draw_staff_lines(painter)
        
        painter.setPen(self.light_gray)
        painter.setBrush(self.light_gray)
        painter.end()

    def draw_clef(self, painter: QPainter):
        painter.drawText(QRect(0, -23, 40, 200), Qt.AlignTop, Glyphs.G_Clef)

   
    def get_staff_line_offsets(self):
        offsets = []
        for i in range(0, 5):
            offsets.append(self.staff_offset + i*self.line_spacing)
        return offsets

    def draw_staff_lines(self, painter: QPainter):
        for y_offset in self.get_staff_line_offsets():
            painter.drawRect(QRect(0, y_offset, self.width(), 1))

   