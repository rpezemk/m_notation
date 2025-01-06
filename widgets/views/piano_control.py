from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QSizePolicy
import fonts.loader


class PianoHorizontal(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        res, self.bravura_font = fonts.loader.try_get_music_font()
        self.very_dark_gray = QColor(40, 40, 40)
        self.dark_gray = QColor(100, 100, 100)
        self.light_gray = QColor(140, 140, 140)
        self.very_light_gray = QColor(160, 160, 160)
        self.light_black = QColor(13, 13, 13)
        self.black = QColor(0, 0, 0)
        self.setFixedHeight(60)
        # self.setFixedWidth(50)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  
        
    def paintEvent(self, event):
        if self.width() < 30 or self.height() < 30:
            return
        painter = QPainter(self)
        painter.setPen(self.very_light_gray)
        painter.setBrush(self.very_light_gray)
        
        max_w = int(self.width()*0.99)
        w = 13
        h = 26
        s = 4    
        n = min(self.width() // (w + s) - 2, 7 * 12)
        for k in range(n):
            is_white = self.is_white(k)
            painter.setBrush(self.very_light_gray if is_white else self.very_dark_gray)
            x = k * (w + s)
            if is_white:
                rect = QRect(x, 0, w, h * 2)
                painter.drawRect(rect)
            else:
                rect = QRect(x, 0, w, h)
                painter.drawRect(rect)
                painter.setBrush(self.very_light_gray)
                painter.setPen(QPen(self.very_light_gray, 0))
                rect = QRect(x - 3, h + 3, w//2+2, h - 3)
                painter.drawRect(rect)
                rect = QRect(x + 3 + w//2, h + 3, w//2+1, h - 3)
                painter.drawRect(rect)
            pitch = k + 24
            if pitch == 60:
                painter.setBrush(self.very_dark_gray)
                painter.setPen(QPen(self.very_light_gray, 1))
                rect = QRect(x + 5, h + 5, 15, 15)
                painter.drawRect(rect)
                
        painter.end()
        
    def is_white(self, pitch: int):
        semi = pitch % 12
        res = semi not in [1, 3, 6, 8, 10]
        return res