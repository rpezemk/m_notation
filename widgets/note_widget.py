import random
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor
from fonts.glyphs import Glyphs

from model.structure import Note

class NoteWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = []  
        self.note_size = 30  
        self.stem_height = 15  
        self.flag_width = 7  
        self.bravura_font = None
        
    def show(self):
        self.generate_notes()
        
    def generate_notes(self):
        w = self.width()
        h = self.height()
        self.notes = [
            (Note(random.randint(0, w), random.randint(0, h),
             QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            for _ in range(200)
        ]
        self.update()  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(self.bravura_font)
        for note in self.notes:
            self.draw_note(painter, note.time, note.pitch, note.color)

    def draw_note(self, painter, x, y, color):
        painter.setPen(QColor(0, 0, 0))
        painter.setFont(painter.font())  # Optionally, set a custom font or size
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
