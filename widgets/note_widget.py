import random
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor

from fonts.glyphs import Glyphs
import fonts.loader
from model.structure import Note

class NoteWidget(QWidget):
    def __init__(self, foreground: int = 0):
        super().__init__()
        self.notes = []  
        self.note_size = 30  
        self.stem_height = 15  
        self.flag_width = 7  
        self.bravura_font = None
        self.foreground = foreground
        res, font = fonts.loader.try_get_music_font()
        if not res:
            raise "error loading font"
        self.bravura_font = font
        
    def show(self):
        self.draw()
        
    def draw(self):
        w = self.width()
        h = self.height()
        self.notes = [
            (Note(random.randint(0, w), random.randint(0, h),
             QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            for _ in range(10)
        ]
        self.update()  

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.painter.setFont(self.bravura_font)
        
        for note in self.notes:
            self.draw_note(note.time, note.pitch, note.color)

    def draw_note(self, x, y, color):
        self.painter.setPen(QColor(self.foreground, self.foreground, self.foreground))
        # self.painter.setFont(painter.font())  # Optionally, set a custom font or size
        text_rect = QRect(x - self.note_size, y - self.note_size, self.note_size * 2, self.note_size * 2)
        self.painter.drawText(text_rect, Qt.AlignCenter, Glyphs.EighthNote)  # Draw the "X" centered at the position
        self.painter.setPen(QColor(255, 0, 0))  # Red color
        self.painter.setPen(Qt.green)  # Or you can use predefined colors (e.g., Qt.green)
        self.painter.setPen(QColor(255, 0, 0))  # Red color for the line
        self.painter.setPen(Qt.SolidLine)  # Line style (default is solid)

        # Draw a line from (50, 50) to (300, 200)
        self.painter.drawLine(20, 20, 20, 100)
        
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            click_pos = event.pos()
            
            for note in self.notes[:]:
                x, y = (note.time, note.pitch)
                if (x - click_pos.x())**2 + (y - click_pos.y())**2 <= (self.note_size // 2)**2:
                    self.notes.remove(note)  
                    self.update()  
                    break  
