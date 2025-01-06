class Clef():
    def __init__(self, base_line_pitch, default_glyph):
        self.base_line_pitch = base_line_pitch
        ...

treble_cleff = Clef(43, "g")

class SampleFamily():
    ...

class InstrInfo():
    def __init__(self, name: str, clef: Clef, sample_family: SampleFamily, lowest, highest):
        ...