import random
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor

from fonts.glyphs import Glyphs
import fonts.loader
from model.piece import Measure, Part
from model.structure import Note, Rest
from widgets.compound.stack_panels import HStack, VStack
from widgets.widget_utils import VisualNote

from widgets.painters.paint_manager import m_paint_visual
from utils.space import get_single_ruler, map_to


class PartWidget(QWidget):
    def __init__(self, parent=None, flags=None):
        super().__init__(parent, flags or Qt.WindowFlags())
        
        self.left_area_width = 100
        layout = QHBoxLayout(self)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(
            VStack(margin=(0, 0, 0, 0), 
                         children=[QLabel("Label")], 
                         black_on_white=True)          \
                  .fixed_width(self.left_area_width)   \
                  .widget)
        
        self.staff_widget = StaffWidget(foreground=99)
        layout.addWidget(self.staff_widget)

class StaffWidget(QWidget):
    def __init__(self, foreground: int = 99):
        super().__init__()
        self.notes = []  
        self.note_size = 120    
        res, self.bravura_font = fonts.loader.try_get_music_font()
        self.line_spacing = 10
        self.staff_offset = 30
        self.no_of_measures = 4
        self.dark_gray = QColor(100, 100, 100)
        self.light_gray = QColor(140, 140, 140)
        self.measures = []
        self.measure_width = 100
        self.clef_margin = 30
        self.bar_left_margin = 25
        self.bar_right_margin = 5
        self.visual_notes = []
        self.y_offsets = None
        
    def set_bars(self, measures: list[Measure]):
        self.measures = measures
        
    def paintEvent(self, event):
        if self.width() < 30 or self.height() < 30:
            return
        self.draw_content()
        
    def draw_content(self):
        painter = QPainter(self)
        self.y_offsets = self.get_y_offsets()
        painter.setFont(self.bravura_font)
        painter.setPen(self.dark_gray)
        painter.setBrush(self.dark_gray)
        self.draw_clef(painter) 
        self.draw_staff_lines(painter)
        self.draw_bar_lines(painter)
        self.calculate_vis_notes(painter)
        painter.setPen(self.light_gray)
        painter.setBrush(self.light_gray)
        for v_n in self.visual_notes:
            m_paint_visual(painter, v_n)
        painter.end()

    def draw_clef(self, painter: QPainter):
        painter.drawText(QRect(0, -23, 40, 200), Qt.AlignTop, Glyphs.G_Clef)

    def get_y_segments(self):
        l_mar = self.bar_left_margin
        r_mar = self.bar_right_margin
        areas = [self.y_offsets[idx:idx+2] for idx in range(0, len(self.y_offsets)-1)]
        areas_2 = [[a[0] + l_mar, a[1] - r_mar] for a in areas]
        return areas_2
        
    def calculate_vis_notes(self, painter: QPainter):
        bar_segments = self.get_y_segments()
        self.visual_notes = []
        for m_no, bar in enumerate(self.measures):
            seg_start = bar_segments[m_no][0]
            seg_end = bar_segments[m_no][1]
            av_width = seg_end - seg_start
            if av_width < 10:
                return
            x_start = seg_start
            x_end = seg_end
            ruler = get_single_ruler(list([th.duration.to_beats for th in bar.time_holders]))
            ruler = map_to(ruler, x_start, x_end)
            
            for idx, note in enumerate(bar.time_holders):
                x_0 = int(ruler[idx])
                if isinstance(note, Note):
                    res_y = int( (-note.get_pitch() * self.line_spacing) / 2) + self.line_spacing * 8
                elif isinstance(note, Rest):
                    res_y = int( (0) / 2) + self.line_spacing * 8
                    
                vis_note = VisualNote(note, (x_0, res_y))
                self.visual_notes.append(vis_note)
                                                
    def draw_staff_lines(self, painter: QPainter):
        for y_offset in self.get_staff_line_infos():
            painter.drawRect(QRect(0, y_offset, self.width(), 1))

    def draw_bar_lines(self, painter):
        self.measure_width = int(self.width()/self.no_of_measures)
        painter.drawRect(QRect(0, self.staff_offset, 1, 4*self.line_spacing))
        for s in self.y_offsets[1:]:
            curr_x = s
            painter.drawRect(QRect(curr_x, self.staff_offset, 1, 4*self.line_spacing))
                    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            click_pos = event.pos()
            for v_n in self.visual_notes:
                x, y = (v_n.point[0], v_n.point[1])
                if (x - click_pos.x())**2 + (y - click_pos.y())**2 <= (self.note_size // 2)**2:
                    m = v_n.inner_note.measure
                    rest = Rest(duration=v_n.inner_note.duration, measure=m)
                    inner_note_idx = m.time_holders.index(v_n.inner_note)
                    m.time_holders[inner_note_idx] = rest
                    idx = self.visual_notes.index(v_n)
                    new_vis_note = VisualNote(rest, v_n.point)
                    print(new_vis_note)
                    print(new_vis_note.inner_note)
                    self.visual_notes[idx] = new_vis_note
                    self.update()  
                    break  

    def get_y_offsets(self) -> list[int]:
        av_space = self.width() - self.clef_margin
        if av_space < 10:
            return [0, 10]
        self.measure_width = int(av_space/self.no_of_measures)
        infos = []
        for i in range(0, self.no_of_measures + 1):
            infos.append(self.clef_margin + self.measure_width * i)
        return infos
    
    def get_staff_line_infos(self):
        offsets = []
        for i in range(0, 5):
            offsets.append(self.staff_offset + i*self.line_spacing)
        return offsets
        