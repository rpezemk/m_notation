from widgets.widget_utils import VisualNote
from model.structure import TimeHolder, Note, Rest
from model.duration import Duration

def fill_or_default(maybe_filled, default_value):
    filled = default_value if maybe_filled is None else maybe_filled
    return filled

class PainterData():
    def __init__(self, t: type, d: Duration):
        self.t = t
        self.d = d
        self.beamed = False
        self.flagged = False
        self.flag_str = None
        self.head_str = None
        self.beam_str = None
    
    @staticmethod    
    def emit(t: type, d: Duration):
        return PainterData(t, d)    
    
    
    def head(self, h_str = None):
        self.head_str = fill_or_default(h_str, "X")
        return self
    
    def beam(self, b_str = None):
        self.b_str = fill_or_default(b_str, "|")
        self.beamed = True
        return self
    
    def flag(self, f_str: str = None):
        self.flagged = True
        self.flag_str = fill_or_default(f_str, "\\")
        return self
    
    
    
def get_painter_definitions() -> list[PainterData]:
    painters = [
        PainterData.emit(Note, Duration.LONGA).head(),
        PainterData.emit(Note, Duration.BREVE).head(),
        PainterData.emit(Note, Duration.WHOLE).head(),
        PainterData.emit(Note, Duration.HALF).head().beam(),
        PainterData.emit(Note, Duration.QUARTER).head().beam(),
        PainterData.emit(Note, Duration.EIGHTH).head().beam().flag(),
        PainterData.emit(Note, Duration.SIXTEENTH).head().beam().flag(),
        PainterData.emit(Note, Duration.THIRTY_SECOND).head().beam().flag(),
        PainterData.emit(Note, Duration.SIXTY_FOURTH).head().beam().flag(),
        
        PainterData.emit(Rest, Duration.LONGA).head(),
        PainterData.emit(Rest, Duration.BREVE).head(),
        PainterData.emit(Rest, Duration.WHOLE).head(),
        PainterData.emit(Rest, Duration.HALF).head(),
        PainterData.emit(Rest, Duration.QUARTER).head(),
        PainterData.emit(Rest, Duration.EIGHTH).head(),
        PainterData.emit(Rest, Duration.SIXTEENTH).head(),
        PainterData.emit(Rest, Duration.THIRTY_SECOND).head(),
        PainterData.emit(Rest, Duration.SIXTY_FOURTH).head(),
    ]
    
    return painters
    
get_painter_definitions()
