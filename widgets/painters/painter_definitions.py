from model.ratio import Ratio
from utils.geometry.transform2d import T2D
from widgets.note_widgets.VisualNote import VisualNote
from model.musical.structure import Note, Rest, TimeHolder
from fonts.glyphs import Glyphs

def get_default_if_none(maybe_filled, default_value):
    filled = default_value if maybe_filled is None else maybe_filled
    return filled

class PainterData():
    def __init__(self, t: type, d: Ratio, orientation_up: bool = True):
        self.t = t
        self.d = d
        self.stemed = False
        self.flagged = False
        self.flag_str = None
        self.head_str = None
        self.stem_str = None
        self.orientation_up = orientation_up

    @staticmethod
    def emit(t: type, d: Ratio, orientation_up: bool = True):
        return PainterData(t, d, orientation_up)


    def head(self, h_str = None):
        self.head_str = get_default_if_none(h_str, "X")
        return self

    def beam(self, b_str = None):
        self.stemed = True
        self.stem_str = get_default_if_none(b_str, "!")
        return self

    def flag(self, f_str: str = None):
        self.flagged = True
        self.flag_str = get_default_if_none(f_str, "\\")
        return self



def get_painter_definitions() -> list[PainterData]:
    all_durations = Ratio.get_all_durations()
    simple_durations = [Ratio.LONGA(), Ratio.BREVE(), Ratio.WHOLE()]
    only_stemed_durations = [Ratio.HALF(), Ratio.QUARTER()]
    flagged = all_durations[5:]

    heads = [Glyphs.LongaNote, Glyphs.BreveNote, Glyphs.WholeNote, Glyphs.Notehead_Half, Glyphs.Notehead_Black]
    flags_up = [Glyphs.Flag_EighthUp, Glyphs.Flag_SixteenthUp, Glyphs.Flag_ThirtySecondUp, Glyphs.Flag_SixtyFourthUp]
    flags_down = [Glyphs.Flag_EighthDown, Glyphs.Flag_SixteenthDown, Glyphs.Flag_ThirtySecondDown, Glyphs.Flag_SixtyFourthDown]

    simple_painters = [PainterData.emit(Note, d).head(heads[i]) for i, d in enumerate(simple_durations)]
    stem_only_painters_up = [PainterData
                            .emit(Note, d)
                            .head(Glyphs.Notehead_Black)
                            .beam(Glyphs.StemUp)
                        for d in only_stemed_durations]

    stem_only_painters_down = [PainterData
                            .emit(Note, d, False)
                            .head(Glyphs.Notehead_Black)
                            .beam(Glyphs.StemUp)
                        for d in only_stemed_durations]

    flagged_painters_up = [PainterData
                            .emit(Note, d)
                            .head(Glyphs.Notehead_Black)
                            .beam(Glyphs.StemUp)
                            .flag(flags_up[i])
                        for i, d in enumerate(flagged)]

    flagged_painters_down = [PainterData
                            .emit(Note, d, False)
                            .head(Glyphs.Notehead_Black)
                            .beam(Glyphs.StemUp)
                            .flag(flags_down[i])
                        for i, d in enumerate(flagged)]

    note_painters = [*simple_painters, *stem_only_painters_up, *stem_only_painters_down, *flagged_painters_up, *flagged_painters_down]

    all_rest_glyphs = [
        Glyphs.Rest_Longa,
        Glyphs.Rest_Maxima,
        Glyphs.Rest_Whole,
        Glyphs.Rest_Half,
        Glyphs.Rest_Quarter,
        Glyphs.Rest_Eighth,
        Glyphs.Rest_Sixteenth,
        Glyphs.Rest_ThirtyTwo,
        Glyphs.Rest_SixtyFour,]


    rest_painters = [PainterData.emit(Rest, d).head(all_rest_glyphs[i]) for i, d in enumerate(all_durations)]

    painters = [*note_painters, *rest_painters]
    return painters

def get_dotting_painters() -> list[PainterData]:
    dotting_painters = [
        (Ratio(t=(1, 2)), Glyphs.AugDot),
        (Ratio(t=(3, 4)), Glyphs.AugDot + " " + Glyphs.AugDot),
        ]
    return dotting_painters

def get_accidental_painters() -> list[tuple[int, str, T2D, T2D]]:
    acc_painters = [
        (-2, Glyphs.Accidental_DoubleFlat, T2D(-8, 2), T2D(-2, 2)),
        (-1, Glyphs.Accidental_Flat, T2D(-2, 2), T2D(-2, 2)),
        (1, Glyphs.Accidental_Sharp, T2D(-2, 2), T2D(-2, 2)),
        (2, Glyphs.Accidental_DoubleSharp, T2D(-8, 2), T2D(-8, 2)),
    ]
    return acc_painters