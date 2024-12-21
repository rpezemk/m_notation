from model.duration import Duration
from model.structure import ConductorPart, Measure, Note, Part, Piece, TempoMark
from utils.musical_layout.precise_aftermath import Ratio

def generate_sample_piece(n_parts: int, n_measures: int):
    piece = Piece(conductor_part=ConductorPart(TempoMark(90, Duration.QUARTER, 0, Ratio(t=(0, 4)))))
    
    for part_no in range(0, n_parts):
        part = Part(piece=piece)
        for measure_no in range(0, n_measures):
            if (part_no + measure_no) % 2 == 0:
                notes = [Note(0, 0), Note(0, 7), Note(0, 0), Note(0, 7)]
                measure = Measure(parent=part, notes=notes)
                for note in notes:
                    note.measure = measure
            else:
                notes = [
                    Note(0, 0, duration=Duration.QUARTER), 
                    Note(0, 7, duration=Duration.EIGHTH), 
                    Note(0, 0, duration=Duration.EIGHTH), 
                    Note(0, 0, duration=Duration.SIXTEENTH), 
                    Note(0, 0, duration=Duration.SIXTEENTH), 
                    Note(0, 0, duration=Duration.SIXTEENTH), 
                    Note(0, 0, duration=Duration.SIXTEENTH), 
                    Note(0, 7, duration=Duration.THIRTY_SECOND), 
                    Note(0, 7, duration=Duration.THIRTY_SECOND), 
                    Note(0, 7, duration=Duration.THIRTY_SECOND), 
                    Note(0, 7, duration=Duration.THIRTY_SECOND), 
                    Note(0, 0, duration=Duration.EIGHTH), 
                    ]
                measure = Measure(parent=part, notes=notes)
                for note in notes:
                    note.measure = measure
            
            part.measures.append(measure)
        part.parent=piece
        piece.parts.append(part)
        
    return piece