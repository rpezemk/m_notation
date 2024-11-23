from PyQt5.QtGui import QPainter

from model.duration import Duration
from widgets.painters.painter_definitions import get_painter_definitions
from widgets.widget_utils import VisualNote
from model.structure import TimeHolder
from widgets.painters.elementary_painter import ElementaryPainter, HeadPainter, StemPainter, FlagPainter
from utils.transform2d import Transform2D
painter_data_list = get_painter_definitions()

head_painter = HeadPainter()
beam_painter = StemPainter()
flag_painter = FlagPainter()

def m_paint_visual(q_painter: QPainter, vn: VisualNote):
    inner = vn.inner_note
    t = type(inner)
    maybe = [p for p in painter_data_list if p.t == t and p.d == inner.duration]
    
    if len(maybe) == 0:
        return
    
    p_d = maybe[0]
    
    if p_d.d == Duration.EIGHTH:
        abc = 234
    # vis_note.point[0] - self.note_size, vis_note.point[1] - self.note_size, self.note_size * 2, self.note_size * 2
    transform = Transform2D(vn.point[0], vn.point[1])
    head_painter.paint(t=transform, q_painter=q_painter, s=p_d.head_str)
    if p_d.stemed:
        beam_painter.paint(t=transform, q_painter=q_painter, s=p_d.stem_str)
    if p_d.flagged:
        flag_painter.paint(t=transform, q_painter=q_painter, s=p_d.flag_str)
    