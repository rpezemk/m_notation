from PyQt5.QtWidgets import QWidget

class MyCompound():
    def __init__(self, t: type):
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color: black;")
        self.layout = t(self.widget)
        
    def add_widgets(self, widgets: list[QWidget]):
        for w in widgets:
            self.layout.addWidget(w)
        return self
