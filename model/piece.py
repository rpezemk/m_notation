from model.structure import Note, ParentOf, ParentAndChild



class Measure(ParentAndChild):
    def __init__(self, children: list[Note]=None, parent=None):
        super().__init__(children, parent)

class Part(ParentAndChild):
    def __init__(self, children: list[Measure]=None, parent=None):
        super().__init__(children, parent)

class Piece(ParentOf):
    def __init__(self, children: list[Part]=None):
        super().__init__(children)



def generate_sample_piece(n_parts: int, n_measures: int):
    piece = Piece()
    
    for part_no in range(0, n_parts):
        part = Part(children=[], parent=piece)
        for measure_no in range(0, n_measures):
            notes = [Note(0, 0), Note(1, 1), Note(2, 6), Note(3, 7)]
            measure = Measure(parent=part, children=notes)
        piece.children.append(part)
        part.parent=piece
    return piece