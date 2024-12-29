from model.musical.structure import Note, TimeHolder


from typing import Tuple


class VisualNote():
    def __init__(self, note: TimeHolder, point: Tuple[float, float]):
        self.inner = note
        self.point = point
        self.is_selected = False
        pass