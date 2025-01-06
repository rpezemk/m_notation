from PyQt5.QtGui import QPainter, QColor

from model.musical.structure import Rest
from model.ratio import Ratio
from widgets.painters.painter_definitions import get_dotting_painters, get_painter_definitions
from widgets.note_widgets.VisualNote import VisualNote
from widgets.painters.elementary_painter import ElementaryPainter
from utils.geometry.transform2d import T2D
painter_data_list = get_painter_definitions()
dot_painters = get_dotting_painters()

el_painter = ElementaryPainter()


dark_gray = QColor(100, 100, 100)
light_gray = QColor(140, 140, 140)
very_light_gray = QColor(160, 160, 160)
red = QColor(200, 44, 44)

def m_paint_visual(q_painter: QPainter, v_n: VisualNote):
    el_painter.paint_visual_note(q_painter, v_n)
        
        
        
def m_paint_tuple(q_painter: QPainter, v_notes: list[VisualNote]):
    el_painter.paint_tuple(q_painter, v_notes)