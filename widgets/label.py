from PyQt5.QtWidgets import QMainWindow, QComboBox, QLabel



class Label(QLabel):
    def __init__(self, label_txt):
        super().__init__(label_txt)
        self.setStyleSheet("background-color: black;")
        self.setStyleSheet("color: white;")