from model.pitch import Pitch

class Clef():
    def __init__(self, base_line_pitch, line_no, default_glyph):
        self.base_line_pitch = base_line_pitch
        self.line_no = line_no
        self.vis_pitch = Pitch.from_midi_pitch(base_line_pitch).vis_height() + line_no
        ...

class AllClefs():
    TREBLE_CLEF = Clef(60, 2, "g")

class SampleFamily():
    ...

class InstrInfo():
    def __init__(self, name: str, clef: Clef, sample_family: SampleFamily, lowest, highest):
        ...