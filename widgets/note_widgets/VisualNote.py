from model.structure import Note


from typing import Tuple


class VisualNote():
    def __init__(self, note: Note, point: Tuple[float, float]):
        self.inner_note = note
        self.point = point
        pass