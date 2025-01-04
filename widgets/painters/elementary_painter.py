from fonts.glyphs import Glyphs
from utils.geometry.transform2d import Transform2D
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor

from widgets.note_widgets.VisualNote import VisualNote

class ElementaryPainter():    
    def __init__(self):
        self.size = 120 
        self.offset = Transform2D()
        
    def paint(self, t: Transform2D, q_painter: QPainter, s: str):
        t2 = self.self_transform(t)
        text_rect = QRect(t2.x - self.size, t2.y - self.size, self.size * 2, self.size * 2)
        q_painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, s) 
        
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
        self.offset = Transform2D(12)
        
    def paint(self, t, q_painter, s: str):
        super().paint(t, q_painter, s)


class FlagPainter(ElementaryPainter):
    def __init__(self):
        super().__init__()
        self.offset = Transform2D(11, -38)
        
    def paint(self, t, q_painter, s: str):
        super().paint(t, q_painter, s)
        
        
class MTuplePainter():
    def paint(self, q_painter: QPainter, v_notes: list[VisualNote]):
        p1 = v_notes[:1][0].point
        p2 = v_notes[-1:][0].point
        
        
        d = 12
        h = 15
        w = 30
        q_painter.drawLine(p1[0], p1[1] + d, p1[0], p1[1] + h + d)
        q_painter.drawLine(p1[0], p1[1] + d + h, p2[0], p2[1] + h + d)
        q_painter.drawLine(p2[0], p2[1] + d, p2[0], p2[1] + h + d)
        x_m = int((p1[0] + p2[0])/2)
        y_m = int((p1[1] + p2[1])/2)
        # aleft: int, atop: int, awidth: int, aheight: int) -> None: ...
        text_rect = QRect(int(x_m - w/2), y_m + 30, w, w)
        q_painter.drawText(text_rect, Qt.AlignCenter | Qt.AlignVCenter, Glyphs.Tuplet_3) 
        
        