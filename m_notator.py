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
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
