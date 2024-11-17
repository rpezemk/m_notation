import sys
import os
import random
from typing import Tuple
import PyQt5.QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QPainterPath
from PyQt5.QtGui import QFont, QFontDatabase
from fonts.glyphs import Glyphs

from model.structure import Note
import fonts.loader
from widgets.note_widget import NoteWidget

class MainWindow(QMainWindow):
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
    window = MainWindow()
    res, font = fonts.loader.try_get_music_font()
    window.note_widget.bravura_font = font
    window.show()
    sys.exit(app.exec_())
