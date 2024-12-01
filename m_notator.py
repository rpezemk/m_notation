import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from widgets.main_window import MainWindow
from widgets.note_widget import PartWidget
import model.piece 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    piece = model.piece.generate_sample_piece(4, 8)
    window.load_piece(piece)
    sys.exit(app.exec_())
