from enum import Enum

class NoteName(Enum):
    C = 0
    D = 2
    E = 4
    F = 5
    G = 7
    A = 9
    B = 11
    
class Pitch():
    def __init__(self, note_name: NoteName, alter: int = 0, oct_no: int = 0):
        self.oct_no = oct_no
        self.note_name = note_name
        self.alter = alter
    
    def res_pitch(self):
        """
        Returns:
            int: resulting MIDI pitch
        """
        res = max(self.oct_no * 12 + self.note_name.value + self.alter, 0)
        return res