from model.ratio import Ratio
from utils.geometry.transform2d import T2D
from widgets.note_widgets.VisualNote import VisualNote
from model.musical.structure import Note, Rest, TimeHolder
from fonts.glyphs import Glyphs

def get_default_if_none(maybe_filled, default_value):
    filled = default_value if maybe_filled is None else maybe_filled
    return filled


def get_note_painters() -> list[tuple]:
    res = [
        (Ratio.MAXIMA(), Glyphs.Notes.Maxima, False, False, [], []),
        (Ratio.LONGA(), Glyphs.Notes.Longa, False, False, [], []),
        (Ratio.BREVE(), Glyphs.Notes.Breve, False, False, [], []),
        (Ratio.WHOLE(), Glyphs.Heads.Whole, False, False, [], []),
        (Ratio.HALF(), Glyphs.Heads.Half, True, False, 
            [Glyphs.StemUp, Glyphs.StemDown], []),
        (Ratio.QUARTER(), Glyphs.Heads.Black, True, False, 
            [Glyphs.StemUp, Glyphs.StemDown], []),
        (Ratio.EIGHTH(), Glyphs.Heads.Black, True, True, 
            [Glyphs.StemUp, Glyphs.StemDown], [Glyphs.Flag_EighthUp, Glyphs.Flag_EighthDown]),
        (Ratio.SIXTEENTH(), Glyphs.Heads.Black, True, True, 
            [Glyphs.StemUp, Glyphs.StemDown], [Glyphs.Flag_SixteenthUp, Glyphs.Flag_SixteenthDown]),
        (Ratio.THIRTY_SECOND(), Glyphs.Heads.Black, True, True, 
            [Glyphs.StemUp, Glyphs.StemDown], [Glyphs.Flag_ThirtySecondUp, Glyphs.Flag_ThirtySecondDown]),
        (Ratio.SIXTY_FOURTH(), Glyphs.Heads.Black, True, True, 
            [Glyphs.StemUp, Glyphs.StemDown], [Glyphs.Flag_SixtyFourthUp, Glyphs.Flag_SixtyFourthDown]),
    ]
    return res


def get_rest_painters() -> list[tuple]:
    res = [
        (Ratio.MAXIMA(), Glyphs.Rests.Maxima),
        (Ratio.LONGA(), Glyphs.Rests.Longa),
        (Ratio.BREVE(), Glyphs.Rests.Breve),
        (Ratio.WHOLE(), Glyphs.Rests.Whole),
        (Ratio.HALF(), Glyphs.Rests.Half),
        (Ratio.QUARTER(), Glyphs.Rests.Quarter),
        (Ratio.EIGHTH(), Glyphs.Rests.Eighth),
        (Ratio.SIXTEENTH(), Glyphs.Rests.Sixteenth),
        (Ratio.THIRTY_SECOND(), Glyphs.Rests.ThirtyTwo),
        (Ratio.SIXTY_FOURTH(), Glyphs.Rests.SixtyFour),
    ]
    return res

def get_dotting_painters() -> list[tuple]:
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
        (2, Glyphs.Accidental_DoubleSharp, T2D(-4, 1), T2D(-4, 1)),
    ]
    return acc_painters