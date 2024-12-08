import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame

class Canvas1(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 200)  # Set the size of the canvas (background)
        self.setStyleSheet("background-color: lightgray;")  # Background color for clarity

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)

        # Set the background color of Canvas1 (e.g., light gray)
        painter.setBrush(QColor(200, 200, 200))  # Light gray background
        painter.drawRect(0, 0, self.width(), self.height())  # Fill the entire canvas

        # Draw a static element (e.g., a blue rectangle)
        painter.setBrush(QColor(0, 0, 255))  # Blue
        painter.drawRect(50, 50, 100, 100)

        painter.end()


class Canvas2(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 200)  # Set the size of the canvas (foreground)
        self.setStyleSheet("background: transparent;")  # Make the background transparent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)

        # Set the background to be transparent (handled by QWidget transparency)
        painter.setBrush(QColor(255, 0, 0, 100))  # Semi-transparent Red (alpha = 100)
        painter.setPen(QColor(255, 0, 0))  # Red pen
        painter.drawEllipse(70, 50, 100, 100)  # Draw a semi-transparent red circle

        painter.end()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Canvas with Background Example")
        self.setGeometry(100, 100, 400, 400)

        # Create a container widget to hold both canvases
        self.container = QWidget(self)
        self.container.setGeometry(50, 50, 400, 200)  # Set the shared area for both canvases

        # Create the first canvas (background)
        canvas1 = Canvas1()
        canvas1.setParent(self.container)

        # Create the second canvas (foreground)
        canvas2 = Canvas2()
        canvas2.setParent(self.container)

        # Show both canvases in the same area
        canvas1.show()
        canvas2.show()

        # Set layout for the container (empty layout since we're using absolute positioning)
        # self.setLayout(QVBoxLayout(self))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
