from model.musical.structure import ConductorPart, MTuple, Measure, Note, Part, Piece, TempoMark, AllClefs
from model.ratio import Ratio
from model.pitch import Pitch, NoteName

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
                                Note.A().o_up().r8(),
                                Note.B().o_up().r8(),
                                Note.C().o_up().o_up().r8(),
                               ]),
                         *MTuple.apply(scale = Ratio(t=(2, 3)),
                           notes=[
                                Note.D().r8(),
                                Note.E().r8(),
                                Note.F().double_sharp().r8(),
                               ]),
                         ]

                measure = Measure(part_no=part_no, m_no=measure_no, parent=part, notes=notes)
                for note in notes:
                    note.measure = measure
            else:
                # notes = [Note(Pitch(NoteName.C), 0), Note(Pitch(NoteName.C), 7), Note(Pitch(NoteName.C), 0), Note(Pitch(NoteName.C), 7)]
                notes = [
                    Note.A().o_dwn().r1(), 
                    # Note.A().o_dwn().r4(), 
                    # *MTuple.apply(scale = Ratio(t=(2, 3)),
                    #        notes=[
                    #             Note.B().o_dwn().r8(),
                    #             Note.C().r8(),
                    #             Note.C().o_up().r8(),
                    #            ]),
                    # Note.C().double_flat().r16(),
                    # Note.D().r16(),
                    # Note.E().o_up().r16(),
                    # Note.F().o_up().double_flat().r16(),
                    # Note.G().o_up().r16(),
                    # Note.A().o_up().r16(),
                    # Note.D().o_up().r16(),
                    # Note.E().o_up().r16(),
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
        part = Part(AllClefs.TREBLE_CLEF, piece=piece)
        for measure_no in range(0, n_measures):
            
            notes = [
                Note.C().r4(),
                Note.C().double_flat().r4(),
                Note.C().r4(),
                Note.C().r4(),
            ]

            measure = Measure(part_no=part_no, m_no=measure_no, parent=part, notes=notes)
            for note in notes:
                note.measure = measure

            part.measures.append(measure)
        part.parent=piece
        piece.parts.append(part)

    return piece