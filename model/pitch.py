from enum import Enum

class NoteName(Enum):
    C = (0, 0, "c")
    D = (2, 1, "d")
    E = (4, 2, "e")
    F = (5, 3, "f")
    G = (7, 4, "g")
    A = (9, 5, "a")
    B = (11, 6,"b")
    
    def all_pitches():
        res = [NoteName.C, NoteName.D, NoteName.E, NoteName.F, NoteName.G, NoteName.A, NoteName.B]
        return res
    
    def find_pitch(semi: int):
        pitches = [p for p in NoteName.all_pitches() if p.value[0] == semi]
        
        return pitches[0] if pitches else None
        
    
class Pitch():
    accs = ["bb", "b", "", "#", "x"]
    def __init__(self, note_name: NoteName, alter: int = 0, oct_no: int = 5):
        self.oct_no = oct_no
        self.note_name = note_name
        self.alter = alter
        
    def vis_pitch(self) -> int:
        res = max(self.oct_no * 7 + self.note_name.value[1], 0)
        return res
    
    def from_midi_pitch(midi_pitch: int) -> 'Pitch':
        oct_no = midi_pitch // 12
        semi = midi_pitch % 12
        note_name = NoteName.find_pitch(semi) if semi in [0, 2, 4, 5, 7, 9, 11] else NoteName.find_pitch(semi - 1)
        alter = semi - note_name.value[0]
        res = Pitch(note_name, alter, oct_no)
        return res
    
    def midi_pitch(self):
        res = self.oct_no * 12 + self.note_name.value[0] + self.alter
        return res
    
    def __str__(self):
        alt = Pitch.accs[self.alter + 2]
        res = f"{self.note_name.value[2]}{alt}{self.oct_no}"
        return res