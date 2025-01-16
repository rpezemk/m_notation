from model.musical.structure import ConductorPart, MTuple, Measure, Note, Part, Piece, Slur, TempoMark, AllClefs
from model.ratio import Ratio
from model.pitch import Pitch, NoteName

def generate_sample_piece(n_treble_parts: int, n_bass_parts, n_measures: int):
    piece = Piece(conductor_part=ConductorPart(TempoMark(90, Ratio.QUARTER(), 0, Ratio(t=(0, 4)))))
    no_of_funcs = len(g_clef_generators)
    for part_no in range(0, n_treble_parts):
        part = Part(AllClefs.TREBLE_CLEF, piece=piece)
        for measure_no in range(0, n_measures):
            func_idx = (part_no + measure_no) % (no_of_funcs - (part_no % (no_of_funcs-1)))
            notes = g_clef_generators[func_idx]()
            measure = Measure(part_no=part_no, m_no=measure_no, parent=part, notes=notes)
            for note in notes:
                note.measure = measure
        
            part.measures.append(measure)
        part.parent=piece
        piece.parts.append(part)
        
    no_of_funcs = len(f_clef_generators)
    for part_no in range(0, n_bass_parts):
        part = Part(AllClefs.BASS_CLEF, piece=piece)
        for measure_no in range(0, n_measures):
            notes = f_clef_generators[0]()
            measure = Measure(part_no=part_no, m_no=measure_no, parent=part, notes=notes)
            for note in notes:
                note.measure = measure
        
            part.measures.append(measure)
        part.parent=piece
        piece.parts.append(part)

    if piece.parts:
        apply_slurs(piece.parts[0])
    
    return piece.validate()


def apply_slurs(part: Part):
    for m_idx in range(0, 2*(len(part.measures)//2), 2):
        ok1, note1 = part.measures[m_idx].time_holders[0].try_get_next_note()
        ok2, note2 = part.measures[m_idx+1].time_holders[0].try_get_next_note()
        
        if not (ok1 and ok2):
            continue
        
        slur = Slur(note1, note2)
    


def get_some_notes_01():
    notes = [Note.A().o_dwn().r1().tie()]
    return notes


def get_some_notes_02():
    notes = [
        Note.G().o_dwn().r2().tie(),
        Note.G().o_dwn().r2(),
        ]
    return notes

def get_some_notes_03():
    notes = [Note.C().r4(),
                         Note.C().r4(),
                         *MTuple.apply(scale = Ratio(t=(2, 3)),
                           notes=[
                                Note.A().o_up().r8().tie(),
                                Note.A().o_up().r8(),
                                Note.C().o_up().o_up().r8(),
                               ]),
                         *MTuple.apply(scale = Ratio(t=(2, 3)),
                           notes=[
                                Note.D().r8(),
                                Note.E().r8(),
                                Note.F().double_sharp().r8(),
                               ]),
                         ]
    return notes


def get_some_notes_04():
    notes = [
                    Note.A().o_dwn().r4(), 
                    *MTuple.apply(scale = Ratio(t=(2, 3)),
                           notes=[
                                Note.B().o_dwn().r8(),
                                Note.C().r8(),
                                Note.C().o_up().r8(),
                               ]),
                    Note.C().double_flat().r16(),
                    Note.D().r16(),
                    Note.E().o_up().r16(),
                    Note.F().o_up().double_flat().r16(),
                    Note.G().o_up().r16(),
                    Note.A().o_up().r16(),
                    Note.D().o_up().r16(),
                    Note.E().o_up().r16(),
                    ]
    return notes



def get_some_bass_notes_01():
    notes = [Note.A().o_dwn().o_dwn().r1().tie()]
    return notes



g_clef_generators = [
    get_some_notes_01,
    get_some_notes_02,
    get_some_notes_03,
    get_some_notes_04,
]

f_clef_generators = [
    get_some_bass_notes_01,
]

