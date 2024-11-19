import random
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor

from fonts.glyphs import Glyphs
import fonts.loader
from model.piece import Measure, Part
from model.structure import Note

class PartWidget(QWidget):
    def __init__(self, parent=None, flags=None):
        super().__init__(parent, flags or Qt.WindowFlags())
        
        self.left_area_width = 100  # Fixed width for the left area
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Left area with a label
        self.left_area = QWidget()
        self.left_area.setFixedWidth(self.left_area_width)
        self.left_area.setStyleSheet("background-color: lightgray; border-right: 1px solid black;")
        self.label = QLabel("Label", self.left_area)
        self.label.setAlignment(Qt.AlignCenter)
        left_layout = QVBoxLayout(self.left_area)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.label)
        
        # Right area with StaffWidget
        self.staff_widget = StaffWidget(foreground=99)
        layout.addWidget(self.left_area)
        layout.addWidget(self.staff_widget)
        self.setStyleSheet("background-color: lightblue; border: 1px solid black;")
        
    def load_part(part: Part):
        pass


class StaffWidget(QWidget):
    def __init__(self, foreground: int = 99):
        super().__init__()
        self.notes = []  
        self.note_size = 120 
        self.stem_height = 15  
        self.flag_width = 7  
        self.foreground = foreground        
        res, self.bravura_font = fonts.loader.try_get_music_font()
        self.left_area_width = 100 
        self.line_spacing = 10
        self.staff_offset = 30
        self.no_of_measures = 4
        self.dark_gray = QColor(100, 100, 100)
        self.light_gray = QColor(140, 140, 140)
        self.measures = []
        
        w = 500
        self.notes = [
            (Note(random.randint(0, w), random.randint(0, 3)))
            for _ in range(10)
        ]
        
    def get_no_of_measures(self):
        return self.no_of_measures
    
    def set_bars(self, measures: list[Measure]):
        self.notes = []
        self.measures = measures
        for m in self.measures:
            for n in m.children:
                self.notes.append(n)
        print(len(self.measures))
        
    def paintEvent(self, event):
        w = self.width()
        h = self.height()
        if w < 30 or h < 30:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.setFont(self.bravura_font)
        
        self.draw_clef(painter) 
        self.draw_staff_lines(painter)
        self.draw_bar_lines(painter)
        self.draw_all_notes(painter)
            
        painter.end()

    def draw_clef(self, painter):
        painter.setPen(self.dark_gray)
        painter.setBrush(self.dark_gray)
        text_rect = QRect(0, -23, 40, 200)
        painter.drawText(text_rect, Qt.AlignTop, Glyphs.G_Clef)

    def draw_all_notes(self, painter):
        for note in self.notes:
            self.draw_note(painter, note)

    def draw_staff_lines(self, painter):
        painter.setBrush(self.dark_gray)
        painter.setPen(self.dark_gray)
        for i in range(0, 5):
            painter.drawRect(QRect(0, self.staff_offset + i*self.line_spacing, self.width(), 1))


    def draw_bar_lines(self, painter):
        measure_width = int(self.width()/self.no_of_measures)
        for i in range(0, self.no_of_measures + 1):
            curr_x = measure_width * i
            painter.drawRect(QRect(curr_x, self.staff_offset, 1, 4*self.line_spacing))
        
    def draw_note(self, painter, note):
        res_y = int( (-note.get_pitch() * self.line_spacing) / 2) + self.line_spacing * 8
        painter.setPen(self.light_gray)
        text_rect = QRect(note.time - self.note_size, res_y - self.note_size, self.note_size * 2, self.note_size * 2)
        painter.drawText(text_rect, Qt.AlignCenter, Glyphs.EighthNote) 


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            click_pos = event.pos()
            for note in self.notes:
                x, y = (note.time, note.get_pitch())
                if (x - click_pos.x())**2 + (y - click_pos.y())**2 <= (self.note_size // 2)**2:
                    self.notes.remove(note)  
                    self.update()  
                    break  
