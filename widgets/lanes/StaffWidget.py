from fonts.glyphs import Glyphs
from model.piece import Measure
from model.structure import Note, Rest
from utils.musical_layout.space import get_single_ruler, map_to
from widgets.lanes.BarrableWidget import BarrableWidget
from widgets.note_widgets.VisualNote import VisualNote
from widgets.painters.paint_manager import m_paint_visual


from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter


class StaffWidget(BarrableWidget):
    def __init__(self):
        super().__init__()
        

        self.staff_offset = 30


        self.visual_notes = []
        self.notes = []
        self.note_size = 120
        self.line_spacing = 10

    def set_content(self, measures: list[Measure]):
        self.measures = measures

    def paintEvent(self, event):
        if self.width() < 30 or self.height() < 30:
            return
        self.y_offsets = self.get_x_offsets()
        self.place_vis_notes()
        self.draw_content()

    def draw_content(self):
        painter = QPainter(self)
        painter.setFont(self.bravura_font)
        painter.setPen(self.dark_gray)
        painter.setBrush(self.dark_gray)

        self.draw_clef(painter)
        self.draw_staff_lines(painter)
        self.draw_bar_lines(painter)
        painter.setPen(self.light_gray)
        painter.setBrush(self.light_gray)
        for v_n in self.visual_notes:
            m_paint_visual(painter, v_n)
        painter.end()

    def draw_clef(self, painter: QPainter):
        painter.drawText(QRect(0, -23, 40, 200), Qt.AlignTop, Glyphs.G_Clef)

    def place_vis_notes(self):
        bar_segments = self.get_h_segments()
        self.visual_notes = []

        for m_no, bar in enumerate(self.measures):
            seg_start = bar_segments[m_no][0]
            seg_end = bar_segments[m_no][1]

            if seg_end - seg_start < 10:
                return
            ruler = get_single_ruler(list([th.duration.to_beats for th in bar.time_holders]))
            ruler = map_to(ruler, seg_start, seg_end)
            for idx, note in enumerate(bar.time_holders):
                x_0 = int(ruler[idx])
                if isinstance(note, Note):
                    res_y = int( (-note.get_pitch() * self.line_spacing) / 2) + self.line_spacing * 8
                elif isinstance(note, Rest):
                    res_y = int( (0) / 2) + self.line_spacing * 8

                vis_note = VisualNote(note, (x_0, res_y))
                self.visual_notes.append(vis_note)

    def draw_staff_lines(self, painter: QPainter):
        for y_offset in self.get_staff_line_offsets():
            painter.drawRect(QRect(0, y_offset, self.width(), 1))

    def draw_bar_lines(self, painter):
        painter.drawRect(QRect(0, self.staff_offset, 1, 4*self.line_spacing))
        for x in self.y_offsets[1:]:
            painter.drawRect(QRect(x, self.staff_offset, 1, 4*self.line_spacing))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            click_pos = event.pos()
            for v_n in self.visual_notes:
                x, y = (v_n.point[0], v_n.point[1])
                if (x - click_pos.x())**2 + (y - click_pos.y())**2 <= (self.note_size // 2)**2:
                    self.remove_note(v_n)
                    break

    def remove_note(self, v_n):
        m = v_n.inner_note.measure
        rest = Rest(duration=v_n.inner_note.duration, measure=m)
        inner_note_idx = m.time_holders.index(v_n.inner_note)
        m.time_holders[inner_note_idx] = rest
        idx = self.visual_notes.index(v_n)
        self.visual_notes[idx] = VisualNote(rest, v_n.point)
        self.update()

    def get_staff_line_offsets(self):
        offsets = []
        for i in range(0, 5):
            offsets.append(self.staff_offset + i*self.line_spacing)
        return offsets