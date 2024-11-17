import sys
import os
import random
from typing import Tuple
import PyQt5.QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from widgets.main_window import MainWindow
from widgets.note_widget import PartWidget
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    
    window.show()
    # all_objs = [window.score_layout.itemAt(i) for i in range(0, window.score_layout.count())]
    sys.exit(app.exec_())
