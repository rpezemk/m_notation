from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit
from PyQt5.QtGui import QFont

class TextBox(QTextEdit):
    def __init__(self, txt: str = "", read_only: bool = False):
        super().__init__(txt)
        self.txt = txt
        self.setFixedHeight(40)
        self.setStyleSheet("color: white;")
        font = QFont("Courier New") 
        font.setStyleHint(QFont.Monospace)  
        self.setFont(font)
        if read_only:
            self.setReadOnly(True)
            
    def append_text(self, txt: str = ""):
        self.txt += txt
        self.setText(self.txt)  
        self.moveCursor(self.textCursor().End)
        self.ensureCursorVisible()
        
    def append_log(self, txt: str = ""):
        self.txt += "\n" + txt
        self.setText(self.txt)
        self.moveCursor(self.textCursor().End)
        self.ensureCursorVisible()
        
class Label(QLabel):
    def __init__(self, txt: str = ""):
        super().__init__(txt)
        self.txt = txt
        self.setFixedHeight(40)
        self.setStyleSheet("color: white; background-color: black;")
        font = QFont("Courier New", 14) 
        font.setStyleHint(QFont.Monospace)  
        self.setFont(font)