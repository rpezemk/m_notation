from model.structure import Measure, Note, Part, Piece

def generate_sample_piece(n_parts: int, n_measures: int):
    piece = Piece()
    
    for part_no in range(0, n_parts):
        part = Part(piece=piece)
        for measure_no in range(0, n_measures):
            notes = [Note(0, 0), Note(0, 7), Note(0, 0), Note(0, 7)]
            measure = Measure(parent=part, notes=notes)
            for note in notes:
                note.measure = measure
                
            part.measures.append(measure)
        part.parent=piece
        piece.parts.append(part)
        
    return piece