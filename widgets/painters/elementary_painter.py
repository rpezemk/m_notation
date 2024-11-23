from utils.transform2d import Transform2D
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor

class ElementaryPainter():    
    def __init__(self):
        self.size = 120 
        self.offset = Transform2D()
        
    def paint(self, t: Transform2D, q_painter: QPainter, s: str):
        t2 = self.self_transform(t)
        text_rect = QRect(t2.x - self.size, t2.y - self.size, self.size * 2, self.size * 2)
        q_painter.drawText(text_rect, Qt.AlignCenter, s) 
        
    def self_transform(self, t: Transform2D):
        res = self.offset + t
        return res
    
class HeadPainter(ElementaryPainter):
    def __init__(self):
        super().__init__()
        self.offset = Transform2D()
        
    def paint(self, t: Transform2D, q_painter: QPainter, s: str):
        super().paint(t, q_painter, s)
        
        
class StemPainter(ElementaryPainter):
    def __init__(self):
        super().__init__()
        self.offset = Transform2D(5)
        
    def paint(self, t, q_painter, s: str):
        super().paint(t, q_painter, s)


class FlagPainter(ElementaryPainter):
    def __init__(self):
        super().__init__()
        self.offset = Transform2D(9, -38)
        
    def paint(self, t, q_painter, s: str):
        super().paint(t, q_painter, s)