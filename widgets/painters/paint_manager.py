from PyQt5.QtGui import QPainter, QColor

from model.musical.structure import Rest
from model.ratio import Ratio
from widgets.painters.painter_definitions import get_dotting_painters, get_painter_definitions
from widgets.note_widgets.VisualNote import VisualNote
from widgets.painters.elementary_painter import ElementaryPainter, HeadPainter, MTuplePainter, StemPainter, FlagPainter
from utils.geometry.transform2d import Transform2D
painter_data_list = get_painter_definitions()
dot_painters = get_dotting_painters()

head_painter = HeadPainter()
beam_painter = StemPainter()
flag_painter = FlagPainter()
tuple_painter = MTuplePainter()

dark_gray = QColor(100, 100, 100)
light_gray = QColor(140, 140, 140)
very_light_gray = QColor(160, 160, 160)
red = QColor(200, 44, 44)

def m_paint_visual(q_painter: QPainter, v_n: VisualNote):
    inner = v_n.inner
    inner_type = type(inner)
    
    maybe = [p for p in painter_data_list if p.t == inner_type and p.d == inner.base_duration]
    
    dot = v_n.inner.dotting
    
    dot_str = ""
    dptr = [dptr2 for dptr2 in dot_painters if dptr2[0] == dot]
    if dptr:
        dot_str = dptr[0][1]
        
    if len(maybe) == 0:
        return
    
    p_d = maybe[0]
    
    transform = Transform2D(v_n.point[0] + 115, v_n.point[1])
    if inner.is_selected:
        q_painter.setPen(red)
        q_painter.setBrush(red)
        
    head_painter.paint(t=transform, q_painter=q_painter, s=p_d.head_str + " " + dot_str)
    if p_d.stemed:
        beam_painter.paint(t=transform, q_painter=q_painter, s=p_d.stem_str)
    if p_d.flagged:
        flag_painter.paint(t=transform, q_painter=q_painter, s=p_d.flag_str)
    
    if inner.is_selected:
        q_painter.setPen(light_gray)
        q_painter.setBrush(light_gray)
        
        
        
def m_paint_tuple(q_painter: QPainter, v_notes: list[VisualNote]):
    tuple_painter.paint(q_painter, v_notes)