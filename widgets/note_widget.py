import random
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor

from fonts.glyphs import Glyphs
import fonts.loader
from model.structure import Note

class PartWidget(QWidget):
    def __init__(self, parent=None, flags=None):
        super().__init__(parent, flags or Qt.WindowFlags())
        
        self.left_area_width = 100  # Fixed width for the left area
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Left area with a label
        self.left_area = QWidget(self)
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
        
    def draw(self):
        self.staff_widget.draw()


class StaffWidget(QWidget):
    def __init__(self, foreground: int = 99):
        super().__init__()
        self.notes = []  
        self.note_size = 30  
        self.stem_height = 15  
        self.flag_width = 7  
        self.bravura_font = None
        self.foreground = foreground        
        res, self.bravura_font = fonts.loader.try_get_music_font()
        self.left_area_width = 100 
                
    def draw(self):
        w = self.width()
        h = self.height()
        self.notes = [
            (Note(random.randint(0, w), random.randint(0, h),
             QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            for _ in range(100)
        ]
        self.update()  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(self.bravura_font)
        
        for note in self.notes:
            self.draw_note(painter, note.time, note.pitch, note.color)
        painter.setBrush(QColor(0, 255, 0))  # Green color
        painter.drawRect(QRect(0, 0, 50, 50))
        painter.end()
        
    def draw_note(self, painter, x, y, color):
        painter.setPen(QColor(self.foreground, self.foreground, self.foreground))
        text_rect = QRect(x - self.note_size, y - self.note_size, self.note_size * 2, self.note_size * 2)
        painter.drawText(text_rect, Qt.AlignCenter, Glyphs.EighthNote)  # Draw the "X" centered at the position

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            click_pos = event.pos()
            for note in self.notes[:]:
                x, y = (note.time, note.pitch)
                if (x - click_pos.x())**2 + (y - click_pos.y())**2 <= (self.note_size // 2)**2:
                    self.notes.remove(note)  
                    self.update()  
                    break  
