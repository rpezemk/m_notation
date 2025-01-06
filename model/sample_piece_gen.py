from model.musical.structure import ConductorPart, MTuple, Measure, Note, Part, Piece, TempoMark
from model.ratio import Ratio
from model.pitch import Pitch, NoteName
from model.musical.part_info import *

def generate_sample_piece(n_parts: int, n_measures: int):
    piece = Piece(conductor_part=ConductorPart(TempoMark(90, Ratio.QUARTER(), 0, Ratio(t=(0, 4)))))

    for part_no in range(0, n_parts):
        part = Part(AllClefs.TREBLE_CLEF, piece=piece)
        for measure_no in range(0, n_measures):
            if (part_no + measure_no) % 2 == 0:
                notes = [Note.C().r4(),
                         Note.C().r4(),
                         *MTuple.apply(scale = Ratio(t=(2, 3)),
                           notes=[
                                Note.C().r8(),
                                Note.C().o_up().r8(),
                                Note.C().sharp().r8(),
                               ]),
                         *MTuple.apply(scale = Ratio(t=(2, 3)),
                           notes=[
                                Note.D().r8(),
                                Note.E().r8(),
                                Note.F().sharp().r8(),
                               ]),
                         ]

                measure = Measure(part_no=part_no, m_no=measure_no, parent=part, notes=notes)
                for note in notes:
                    note.measure = measure
            else:
                # notes = [Note(Pitch(NoteName.C), 0), Note(Pitch(NoteName.C), 7), Note(Pitch(NoteName.C), 0), Note(Pitch(NoteName.C), 7)]
                notes = [
                    Note.C().r4(), 
                    *MTuple.apply(scale = Ratio(t=(2, 3)),
                           notes=[
                                Note.C().r8(),
                                Note.C().r8(),
                                Note.C().o_up().r8(),
                               ]),
                    Note.C().r16(),
                    Note.D().r16(),
                    Note.E().r16(),
                    Note.F().sharp().r16(),
                    Note.G().r32(),
                    Note.A().r32(),
                    Note.B().r32(),
                    Note.C().o_up().r32(),
                    Note.D().o_up().r16(),
                    Note.E().o_up().r16(),
                    ]
                measure = Measure(part_no=part_no, m_no=measure_no, parent=part, notes=notes)
                for note in notes:
                    note.measure = measure

            part.measures.append(measure)
        part.parent=piece
        piece.parts.append(part)

    return piece


def generate_sample_piece2(n_parts: int, n_measures: int):
    piece = Piece(conductor_part=ConductorPart(TempoMark(90, Ratio.QUARTER(), 0, Ratio(t=(0, 4)))))

    for part_no in range(0, n_parts):
        part = Part(piece=piece)
        for measure_no in range(0, n_measures):
            
            notes = [
                Note(Pitch(NoteName.C), Ratio(t=(1, 4))),
                Note(Pitch(NoteName.C), Ratio(t=(1, 4))),
                Note(Pitch(NoteName.D), base_duration=Ratio.EIGHTH()),
                Note(Pitch(NoteName.E), base_duration=Ratio.EIGHTH()),
                Note(Pitch(NoteName.A), base_duration=Ratio.EIGHTH()),
                Note(Pitch(NoteName.B), base_duration=Ratio.EIGHTH()),
            ]

            measure = Measure(part_no=part_no, m_no=measure_no, parent=part, notes=notes)
            for note in notes:
                note.measure = measure

            part.measures.append(measure)
        part.parent=piece
        piece.parts.append(part)

    return piece