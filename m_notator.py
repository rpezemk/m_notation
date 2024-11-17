import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QPainterPath


class NoteWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = []  
        self.note_size = 15  
        self.stem_height = 40  
        self.flag_width = 20  
        self.generate_notes()

    def generate_notes(self):
        """Generate 1000 random notes."""
        self.notes = [
            (random.randint(0, self.width()), random.randint(0, self.height()),
             QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            for _ in range(1000)
        ]
        self.update()  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for x, y, color in self.notes:
            self.draw_note(painter, x, y, color)

    def draw_note(self, painter, x, y, color):
        
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRect(x - self.note_size // 2, y - self.note_size // 2,
                                   self.note_size, self.note_size))

        
        stem_x = x + self.note_size // 2
        painter.setPen(color)
        painter.drawLine(stem_x, y, stem_x, y - self.stem_height)

        
        path = QPainterPath()
        flag_start = QPointF(stem_x, y - self.stem_height)
        flag_end = QPointF(stem_x + self.flag_width, y - self.stem_height + 10)
        control_point = QPointF(stem_x + self.flag_width / 2, y - self.stem_height - 10)
        path.moveTo(flag_start)
        path.quadTo(control_point, flag_end)
        path.lineTo(stem_x, y - self.stem_height + 5)  
        painter.setBrush(color)
        painter.drawPath(path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            click_pos = event.pos()
            
            for note in self.notes[:]:
                x, y, _ = note
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoteWindow()
    window.show()
    sys.exit(app.exec_())
