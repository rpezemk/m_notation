from PyQt5.QtGui import QPainter, QColor

from model.duration import Duration
from widgets.painters.painter_definitions import get_painter_definitions
from widgets.note_widgets.VisualNote import VisualNote
from model.structure import TimeHolder
from widgets.painters.elementary_painter import ElementaryPainter, HeadPainter, StemPainter, FlagPainter
from utils.geometry.transform2d import Transform2D
painter_data_list = get_painter_definitions()

head_painter = HeadPainter()
beam_painter = StemPainter()
flag_painter = FlagPainter()
dark_gray = QColor(100, 100, 100)
light_gray = QColor(140, 140, 140)
very_light_gray = QColor(160, 160, 160)
red = QColor(200, 44, 44)

def m_paint_visual(q_painter: QPainter, vn: VisualNote):
    inner = vn.inner
    t = type(inner)
    maybe = [p for p in painter_data_list if p.t == t and p.d == inner.duration]
    
    if len(maybe) == 0:
        return
    
    p_d = maybe[0]
    
    transform = Transform2D(vn.point[0], vn.point[1])
    if inner.is_selected:
        q_painter.setPen(red)
        q_painter.setBrush(red)
        
    head_painter.paint(t=transform, q_painter=q_painter, s=p_d.head_str)
    if p_d.stemed:
        beam_painter.paint(t=transform, q_painter=q_painter, s=p_d.stem_str)
    if p_d.flagged:
        flag_painter.paint(t=transform, q_painter=q_painter, s=p_d.flag_str)
    
    if inner.is_selected:
        q_painter.setPen(light_gray)
        q_painter.setBrush(light_gray)