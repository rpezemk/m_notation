import sys
import os
import random
import PyQt5.QtGui
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QPainterPath
from PyQt5.QtGui import QFont, QFontDatabase


    

from model.note import Note

working_dir = os.getcwd()

font_path = os.path.join(working_dir, "fonts/Bravura.otf")

ex = os.path.exists(font_path)



class NoteWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = []  
        self.note_size = 30  
        self.stem_height = 15  
        self.flag_width = 7  
        self.bravura_font = None
    def show(self):
        super().show()
        self.generate_notes()
        
    def generate_notes(self):
        w = self.width()
        h = self.height()
        self.notes = [
            (Note(random.randint(0, w), random.randint(0, h),
             QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            for _ in range(10000)
        ]
        self.update()  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(self.bravura_font)
        for note in self.notes:
            self.draw_note(painter, note.x, note.y, note.color)

    def draw_note(self, painter, x, y, color):
        painter.setPen(color)
        painter.setFont(painter.font())  # Optionally, set a custom font or size
        text_rect = QRect(x - self.note_size, y - self.note_size, self.note_size * 2, self.note_size * 2)
        painter.drawText(text_rect, Qt.AlignCenter, "\uE050")  # Draw the "X" centered at the position



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            click_pos = event.pos()
            
            for note in self.notes[:]:
                x, y = (note.x, note.y)
                if (x - click_pos.x())**2 + (y - click_pos.y())**2 <= (self.note_size // 2)**2:
                    self.notes.remove(note)  
                    self.update()  
                    break  


class NoteWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("m_notator")
        self.setGeometry(100, 100, 800, 600)
        self.note_widget = NoteWidget()
        self.redraw_button = QPushButton("Redraw Notes")
        self.redraw_button.clicked.connect(self.note_widget.generate_notes)
        layout = QVBoxLayout()
        layout.addWidget(self.note_widget)
        layout.addWidget(self.redraw_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        
        
    def resizeEvent(self, event):
        new_size = event.size()  # Get the new size of the window
        self.setWindowTitle(f"Window resized to: {new_size.width()} x {new_size.height()}")
        super().resizeEvent(event)  # Call the parent class's resizeEvent
        self.note_widget.show()
    def show(self):
        super().show()
        self.note_widget.generate_notes()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoteWindow()
    try:
        font_db = PyQt5.QtGui.QFontDatabase()
        font_path = os.path.join(os.getcwd(), "fonts", "Bravura.otf")
        font_id = font_db.addApplicationFont(font_path)
        if font_id == -1:
            print("Failed to load the font.")
        else:
            print(f"Font loaded successfully with ID: {font_id}")
        font_family = font_db.applicationFontFamilies(font_id)[0]
        window.note_widget.bravura_font = QFont(font_family, 40)
    except Exception as e:
        print(f"Error loading font: {e}")
    window.show()
    sys.exit(app.exec_())
