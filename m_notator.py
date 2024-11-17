import sys
import os
import random
from typing import Tuple
import PyQt5.QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from widgets.main_window import MainWindow
from widgets.note_widget import PartWidget
import model.piece 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    piece = model.piece.generate_sample_piece(4, 8)
    window = MainWindow()
    # window.load_piece(piece)
    window.show()
    # all_objs = [window.score_layout.itemAt(i) for i in range(0, window.score_layout.count())]
    sys.exit(app.exec_())
