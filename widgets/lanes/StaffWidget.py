from functools import cmp_to_key
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

from fonts.glyphs import Glyphs
from model.sample_piece_gen import Measure
from model.musical.structure import HorizontalChunk, Note, Rest
from utils.musical_layout.space import get_single_ruler, map_to
from widgets.lanes.BarrableWidget import BarrableWidget
from widgets.note_widgets.VisualNote import VisualNote
from widgets.painters.paint_manager import m_paint_visual



class StaffWidget(BarrableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.staff_widget = parent
        self.setCursor(Qt.CrossCursor)

        self.staff_offset = 30


        self.visual_notes: list[VisualNote] = []
        self.notes = []
        self.note_size = 120
        self.line_spacing = 10

    def set_content(self, h_chunk: HorizontalChunk):
        self.measures = h_chunk.measures

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
            
            for note in bar.time_holders:
                curr_x = int(note.offset_ratio.to_float() * (seg_end - seg_start) + seg_start)
                if isinstance(note, Note):
                    res_y = int( (-note.pitch * self.line_spacing) / 2) + self.line_spacing * 8
                elif isinstance(note, Rest):
                    res_y = int( (0) / 2) + self.line_spacing * 8

                vis_note = VisualNote(note, (curr_x, res_y))
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
            x0 = click_pos.x()
            y0 = click_pos.y()
            maybe = [v_n for v_n in self.visual_notes if abs(v_n.point[0] - x0) < 7 and abs(v_n.point[1] - y0) < 7]
            if not maybe:
                return
            
            maybe[0].inner.is_selected = True
            self.update()
            self.staff_widget.deselect_notes_but([maybe[0]])
    
    def select_all(self):
        selected = [d for d in self.visual_notes]
        if not selected:
            return
        
        for s in selected:
            s.inner.is_selected = True
        self.update()
            
    def delete_selected_notes(self):
        selected = [v_n for v_n in self.visual_notes if v_n.inner.is_selected]
        if not selected:
            return
        self.remove_note(selected[0])
        self.update()
        
        
            
    def deselect_notes_but(self, v_notes: list[VisualNote]):
        deselected = [d for d in self.visual_notes if d not in v_notes]
        if not deselected:
            return
        
        for d in deselected:
            d.inner.is_selected = False
        self.update()
            
    def remove_note(self, v_n: VisualNote):
        msr = v_n.inner.measure
        rest = Rest(base_duration=v_n.inner.base_duration, measure=msr, dotting=v_n.inner.dotting)
        rest.offset_ratio = v_n.inner.offset_ratio
        inner_note_idx = msr.time_holders.index(v_n.inner)
        msr.time_holders[inner_note_idx] = rest
        
        idx = self.visual_notes.index(v_n)
        self.visual_notes[idx] = VisualNote(rest, v_n.point)
        self.visual_notes[idx].inner.is_selected = True

    def get_staff_line_offsets(self):
        offsets = []
        for i in range(0, 5):
            offsets.append(self.staff_offset + i*self.line_spacing)
        return offsets
    
    """
    COMMAND METHODS
    """
    
    def select_prev_note(self):
        selected = [v_n for v_n in self.visual_notes if v_n.inner.is_selected][-1:]
        if not selected:
            return
        
        sel = selected[0]
        
        
        idx = self.visual_notes.index(sel)

        if idx == 0:
            return
        
        sel.inner.is_selected = False
        
        nxt = self.visual_notes[idx - 1]
        nxt.inner.is_selected = True
        
        self.update()
    
    
    def select_next_note(self):
        selected = self.get_last_selected_note()
        if not selected:
            return
        
        sel = selected[0]
        
        
        idx = self.visual_notes.index(sel)

        if idx == len(self.visual_notes) - 1:
            return
        
        sel.inner.is_selected = False
        
        nxt = self.visual_notes[idx + 1]
        nxt.inner.is_selected = True
        
        self.update()

    def get_last_selected_note(self):
        selected = [v_n for v_n in self.visual_notes if v_n.inner.is_selected][-1:]
        return selected
        
        
# def custom_comparator(x: 'Ratio', y: 'Ratio'):
#         if x < y:
#             return -1  # x comes before y
#         elif x > y:
#             return 1   # x comes after y
#         else:
#             return 0   # x and y are equal    
        
        
# custom_key = cmp_to_key(custom_comparator)