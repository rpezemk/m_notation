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
        self.setFixedHeight(35)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  
        
    def paintEvent(self, event):
        if self.width() < 30 or self.height() < 30:
            return
        painter = QPainter(self)
        painter.setPen(self.very_light_gray)
        painter.setBrush(self.very_light_gray)
        
        w = 10
        h = 15
        s = 4    
        n = min(self.width() // (w + s) - 2, 7 * 12 + 1)
        
        oct_width = (w + s) * 12
        n_octaves = n // 12
        s_w = int(12/7 * w)
        for oct_no in range(n_octaves):
            
            painter.setBrush(self.very_light_gray)
            
            for strange in [12*x/7 for x in range(7)]:
                pitch = oct_no * 12 + strange
                x = int(pitch * (w + s))
                rect = QRect(x, 0, s_w+2, h*2)
                painter.drawRect(rect)
                
            painter.setBrush(self.very_dark_gray)
            
            for semi_no in range(12):
                pitch = oct_no * 12 + semi_no
                is_white = self.is_white(pitch)
                x = pitch * (w + s)
                if not is_white:
                    rect = QRect(x-5, 0, w+11, h+3)
                    painter.drawRect(rect)
                    rect = QRect(x-2, 0, w+5, h)
                    painter.drawRect(rect)
                
        painter.end()
        
    def is_white(self, pitch: int):
        semi = pitch % 12
        res = semi not in [1, 3, 6, 8, 10]
        return res
    
    