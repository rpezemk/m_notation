from widgets.painters.painter_definitions import get_painter_definitions
from widgets.widget_utils import VisualNote
from model.structure import TimeHolder
from widgets.painters.elementary_painter import ElementaryPainter, HeadPainter, BeamPainter, FlagPainter
    
painter_data_list = get_painter_definitions()



def m_paint_visual(vn: VisualNote):
    ...