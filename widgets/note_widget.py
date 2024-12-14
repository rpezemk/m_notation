from typing import Any, override
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QPen

from fonts.glyphs import Glyphs
import fonts.loader
from model.piece import Measure
from model.structure import Note, Rest
from widgets.compound.stack_panels import VStack
from widgets.widget_utils import VisualNote
from widgets.painters.paint_manager import m_paint_visual
from utils.space import get_single_ruler, map_to
from widgets.text_box import TextBox
from utils.file_utils.os_utils import get_absolute_path
from model.audiofile import AudioFile

class PartWidget(QWidget):
    def __init__(self, parent=None, flags=None, widget_type: type = None):
        super().__init__(parent, flags or Qt.WindowFlags())
        layout = QHBoxLayout(self)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        
        layout.addWidget(
            VStack(
                margin=(0, 0, 0, 0), 
                children=[QLabel(text="Label")],
                fixed_width=100, stretch=False)
            .widget)
        
        self.staff_widget = widget_type()
        layout.addWidget(self.staff_widget)


class LaneWidget(QWidget):
    def __init__(self):
        super().__init__()
        res, self.bravura_font = fonts.loader.try_get_music_font()
        self.dark_gray = QColor(100, 100, 100)
        self.light_gray = QColor(140, 140, 140)
        self.very_light_gray = QColor(160, 160, 160)
        self.light_black = QColor(13, 13, 13)
        self.black = QColor(0, 0, 0)
        self.setFixedHeight(120) 
        
    def set_content(self, data: Any):
        ...
        
    @override
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    @override
    def paintEvent(self, event):
        super().paintEvent(event)
        
    
audio_ranges = [(11, 12.3), (13, 16), (17, 19.7)]

class ConductorWidget(LaneWidget):
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
        
class AudioWidget(LaneWidget):
    def __init__(self):
        super().__init__()
        self.view_time_start = 10 # sec
        self.view_time_end = 20 # sec
        self.sample_file_path = "./audio_samples/harvard.wav"
        self.abs_path_sample = get_absolute_path(self.sample_file_path)
        self.audiofile = AudioFile(self.abs_path_sample)
        self.simple = self.audiofile.get_simplified(10, 10)
        
    @override
    def set_content(self, data: Any):
        ...
        
    @override
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        
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
        self.draw_ranges(painter)
        pen = QPen(QColor(255, 255, 255, 80))  # Set the pen color to black
        painter.setPen(pen)
        pen.setWidth(1)       # Set the stroke thickness to 5 pixels
        self.draw_data(painter)
        painter.end()
        
    def draw_frame(self, painter: QPainter):
        w = self.width()
        h = self.height()
        rect = QRect(0, 0, w-1, h-1)
        painter.drawRect(rect)
    
        
        
    def draw_ranges(self, painter: QPainter):
        w = self.width()
        h = self.height()
        painter.setBrush(self.black)
        
        for rng in audio_ranges:
            start = rng[0]    
            end = rng[1]
            time_range = self.view_time_end - self.view_time_start
            
            x0 = int(((start - self.view_time_start)/time_range) * w)
            y0 = 5
            r_w = int(((end - start)/time_range) * w)
            r_h = h - 10
            
            rect = QRect(x0, y0, r_w, r_h)
            painter.drawRect(rect)
            
            
    def draw_data(self, painter: QPainter):
        w = self.width()
        h = self.height()
        painter.setBrush(self.black)
        
        for rng in audio_ranges:
            start = rng[0]    
            end = rng[1]
            time_range = self.view_time_end - self.view_time_start
            
            x0 = int(((start - self.view_time_start)/time_range) * w)
            y0 = 5
            r_w = int(((end - start)/time_range) * w)
            r_h = h
            self.draw_range_data(painter, x0, y0, r_w, r_h)
            
    def draw_range_data(self, painter: QPainter, x0, y0, r_w, r_h):
        simplified = self.audiofile.get_simplified(r_h, 1)
        max__ = max(simplified)
        simplified = [(r*r_h)/max__ for r in simplified]
        lenght = len(simplified)
        cnt = 0
    
        for val in simplified:
            res_x0 = int(x0 + (r_w*cnt/lenght))
            val = int(val)
            painter.drawPoint(res_x0, r_h - val - 5)
            cnt += 1
            
class StaffWidget(LaneWidget):
    def __init__(self):
        super().__init__()
        self.notes = []  
        self.note_size = 120    
        self.line_spacing = 10
        self.staff_offset = 30
        self.no_of_measures = 4
        self.measures = []
        self.clef_margin = 30
        self.bar_left_margin = 25
        self.bar_right_margin = 5
        self.visual_notes = []
        self.y_offsets = None
        
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

    def get_y_segments(self):
        l_mar = self.bar_left_margin
        r_mar = self.bar_right_margin
        areas = [self.y_offsets[idx:idx+2] for idx in range(0, len(self.y_offsets)-1)]
        areas_2 = [[a[0] + l_mar, a[1] - r_mar] for a in areas]
        return areas_2
        
    def place_vis_notes(self):
        bar_segments = self.get_y_segments()
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

    def get_x_offsets(self) -> list[int]:
        av_space = self.width() - self.clef_margin
        if av_space < 10:
            return [0, 10]
        measure_width = int(av_space/self.no_of_measures)
        infos = []
        for i in range(0, self.no_of_measures + 1):
            infos.append(self.clef_margin + measure_width * i)
        return infos
    
    def get_staff_line_offsets(self):
        offsets = []
        for i in range(0, 5):
            offsets.append(self.staff_offset + i*self.line_spacing)
        return offsets
        