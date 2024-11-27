from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QFont


class MyButton(QPushButton):
    def __init__(self, text, click_func=None):
        super().__init__(text)
        self.setStyleSheet("color: white;")
        font = QFont("Courier New") 
        font.setStyleHint(QFont.Monospace)  
        self.setFont(font)
        self.clicked.connect(click_func)
        self.setFixedHeight(30)