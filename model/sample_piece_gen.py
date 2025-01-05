from model.musical.structure import ConductorPart, MTuple, Measure, Note, Part, Piece, TempoMark
from model.ratio import Ratio

def generate_sample_piece(n_parts: int, n_measures: int):
    piece = Piece(conductor_part=ConductorPart(TempoMark(90, Ratio.QUARTER(), 0, Ratio(t=(0, 4)))))
    
    for part_no in range(0, n_parts):
        part = Part(piece=piece)
        for measure_no in range(0, n_measures):
            if (part_no + measure_no) % 2 == 0:
                notes = [Note(0, Ratio(t=(1, 4))), 
                         Note(7, Ratio(t=(1, 4))), 
                         *MTuple.apply(scale = Ratio(t=(2, 3)),
                           notes=[
                                Note(0, base_duration=Ratio.EIGHTH()), 
                                Note(0, base_duration=Ratio.EIGHTH()), 
                                Note(0, base_duration=Ratio.EIGHTH()), 
                               ]),
                         *MTuple.apply(scale = Ratio(t=(2, 3)),
                           notes=[
                                Note(0, base_duration=Ratio.EIGHTH()), 
                                Note(0, base_duration=Ratio.EIGHTH()), 
                                Note(0, base_duration=Ratio.EIGHTH()), 
                               ]),
                         ]
                
                measure = Measure(part_no=part_no, m_no=measure_no, parent=part, notes=notes)
                for note in notes:
                    note.measure = measure
            else:
                # notes = [Note(0, 0), Note(0, 7), Note(0, 0), Note(0, 7)]
                notes = [
                    Note(0, base_duration=Ratio.QUARTER()), 
                    *MTuple.apply(scale = Ratio(t=(2, 3)),
                           notes=[
                                Note(0, base_duration=Ratio.EIGHTH()), 
                                Note(0, base_duration=Ratio.EIGHTH()), 
                                Note(0, base_duration=Ratio.EIGHTH()), 
                               ]), 
                    Note(0, base_duration=Ratio.SIXTEENTH()), 
                    Note(0, base_duration=Ratio.SIXTEENTH()), 
                    Note(0, base_duration=Ratio.SIXTEENTH()), 
                    Note(0, base_duration=Ratio.SIXTEENTH()), 
                    Note(0, base_duration=Ratio.THIRTY_SECOND()), 
                    Note(0, base_duration=Ratio.THIRTY_SECOND()), 
                    Note(0, base_duration=Ratio.THIRTY_SECOND()), 
                    Note(0, base_duration=Ratio.THIRTY_SECOND()), 
                    Note(0, base_duration=Ratio.SIXTEENTH()), 
                    Note(0, base_duration=Ratio.SIXTEENTH()), 
                    ]
                measure = Measure(part_no=part_no, m_no=measure_no, parent=part, notes=notes)
                for note in notes:
                    note.measure = measure
            
            part.measures.append(measure)
        part.parent=piece
        piece.parts.append(part)
        
    return piece