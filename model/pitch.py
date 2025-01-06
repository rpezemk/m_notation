from enum import Enum

class NoteName(Enum):
    C = (0, 0)
    D = (2, 1)
    E = (4, 2)
    F = (5, 3)
    G = (7, 4)
    A = (9, 5)
    B = (11, 6)
    
    def all_pitches():
        res = [NoteName.C, NoteName.D, NoteName.E, NoteName.F, NoteName.G, NoteName.A, NoteName.B]
        return res
    
    def find_pitch(semi: int):
        pitches = [p for p in NoteName.all_pitches() if p.value[0] == semi]
        
        return pitches[0] if pitches else None
        
    
class Pitch():
    def __init__(self, note_name: NoteName, alter: int = 0, oct_no: int = 5):
        self.oct_no = oct_no
        self.note_name = note_name
        self.alter = alter
    
    def res_pitch(self):
        """
        Returns:
            int: resulting MIDI pitch
        """
        res = max(self.oct_no * 12 + self.note_name.value[0] + self.alter, 0)
        return res
    
    def vis_height(self):
        res = max(self.oct_no * 7 + self.note_name.value[1], 0)
        return res
    
    def from_midi_pitch(midi_pitch: int):
        oct_no = midi_pitch // 12
        semi = midi_pitch % 12
        note_name = NoteName.find_pitch(semi) if semi in [0, 2, 4, 5, 7, 9, 11] else NoteName.find_pitch(semi - 1)
        alter = semi - note_name.value[0]
        res = Pitch(note_name, alter, oct_no)
        return res