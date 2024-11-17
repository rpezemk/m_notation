import sys
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from widgets.note_widget import NoteWidget

class StaffPanel(QWidget):
    def __init__(self, height=120):
        super().__init__()
        self.setFixedHeight(height)
        self.setStyleSheet("background-color: lightblue; border: 1px solid black;")
        self.note_widget = NoteWidget(190)
        layout = QVBoxLayout(self)
        layout.addWidget(self.note_widget)
        
    def draw(self):    
        self.note_widget.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stacked Panels")
        self.setGeometry(100, 100, 400, 800)

        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        self.panels = []
        for i in range(5):
            panel = StaffPanel(120)
            main_layout.addWidget(panel)
            self.panels.append(panel)

        self.setCentralWidget(main_widget)
        self.setStyleSheet("background-color: black;")
        
    def resizeEvent(self, event):
        new_size = event.size()  # Get the new size of the window
        self.setWindowTitle(f"Window resized to: {new_size.width()} x {new_size.height()}")
        super().resizeEvent(event)  # Call the parent class's resizeEvent
        self.show()

    def show(self):
        super().show()
        for panel in self.panels:
            panel.draw()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
