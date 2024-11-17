import sys
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from widgets.note_widget import NoteWidget

class StaffPanel(QWidget):
    def __init__(self, height=120):
        super().__init__()
        self.setFixedHeight(height)
        self.setStyleSheet("background-color: lightblue; border: 1px solid black;")
        self.note_widget = NoteWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.note_widget)
        self.note_widget.generate_notes()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stacked Panels")
        self.setGeometry(100, 100, 400, 800)

        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)

        for i in range(5):
            panel = StaffPanel(120)
            main_layout.addWidget(panel)

        self.setCentralWidget(main_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
