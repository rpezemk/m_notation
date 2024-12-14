from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit
from PyQt5.QtGui import QFont

class TextBox(QTextEdit):
    def __init__(self, txt: str = "", read_only: bool = False, set_fixed_height = -1):
        super().__init__(txt)
        self.txt = txt
        if set_fixed_height > 0:
            self.setFixedHeight(set_fixed_height)
        else:
            self.setFixedHeight(40)
        font = QFont("Courier New") 
        font.setStyleHint(QFont.Monospace)  
        self.setFont(font)
        if read_only:
            self.setReadOnly(True)
            
    def append_text(self, txt: str = ""):
        self.txt += f"{txt}"
        self.setText(self.txt)  
        self.moveCursor(self.textCursor().End)
        self.ensureCursorVisible()
        
    def append_log(self, txt: str = ""):
        self.txt += f"\n{txt}"
        self.setText(self.txt)
        self.moveCursor(self.textCursor().End)
        self.ensureCursorVisible()
        