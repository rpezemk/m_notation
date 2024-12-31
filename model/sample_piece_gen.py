from model.duration import DurationBase
from model.musical.structure import ConductorPart, Measure, Note, Part, Piece, TempoMark
from model.ratio import Ratio

def generate_sample_piece(n_parts: int, n_measures: int):
    piece = Piece(conductor_part=ConductorPart(TempoMark(90, DurationBase.QUARTER, 0, Ratio(t=(0, 4)))))
    
    for part_no in range(0, n_parts):
        part = Part(piece=piece)
        for measure_no in range(0, n_measures):
            if (part_no + measure_no) % 2 == 0:
                notes = [Note(0, Ratio(t=(1, 4))).dot(), 
                         Note(7, Ratio(t=(1, 8))), 
                         Note(0, Ratio(t=(1, 4))).double_dot(), 
                         Note(7, Ratio(t=(1, 16)))]
                
                measure = Measure(part_no=part_no, m_no=measure_no, parent=part, notes=notes)
                for note in notes:
                    note.measure = measure
            else:
                # notes = [Note(0, 0), Note(0, 7), Note(0, 0), Note(0, 7)]
                notes = [
                    Note(0, base_duration=DurationBase.QUARTER), 
                    Note(7, base_duration=DurationBase.EIGHTH), 
                    Note(0, base_duration=DurationBase.EIGHTH), 
                    Note(0, base_duration=DurationBase.SIXTEENTH), 
                    Note(0, base_duration=DurationBase.SIXTEENTH), 
                    Note(0, base_duration=DurationBase.SIXTEENTH), 
                    Note(0, base_duration=DurationBase.SIXTEENTH), 
                    Note(7, base_duration=DurationBase.THIRTY_SECOND), 
                    Note(7, base_duration=DurationBase.THIRTY_SECOND), 
                    Note(7, base_duration=DurationBase.THIRTY_SECOND), 
                    Note(7, base_duration=DurationBase.THIRTY_SECOND), 
                    Note(0, base_duration=DurationBase.SIXTEENTH), 
                    Note(7, base_duration=DurationBase.SIXTEENTH), 
                    ]
                measure = Measure(part_no=part_no, m_no=measure_no, parent=part, notes=notes)
                for note in notes:
                    note.measure = measure
            
            part.measures.append(measure)
        part.parent=piece
        piece.parts.append(part)
        
    return piece