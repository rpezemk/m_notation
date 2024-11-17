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
    for i in range(5):
        window.add_child_to_stack(PartWidget())
    window.stack_layout.addStretch()
    window.show()
    all_objs = [window.stack_layout.itemAt(i) for i in range(0, window.stack_layout.count())]
    sys.exit(app.exec_())
