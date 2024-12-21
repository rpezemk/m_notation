import random
from typing import Any
from PyQt5.QtGui import QColor
from model.duration import Duration
from utils.musical_layout.precise_aftermath import Ratio

    
    
class TimeHolder():
    def __init__(self, duration: Duration = None, measure: 'Measure' = None):
        self.duration = duration if duration is not None else Duration.QUARTER
        self.measure = measure
    
class Rest(TimeHolder):
    def __init__(self, duration: Duration = None, measure: 'Measure' = None):
        self.duration = duration if duration is not None else Duration.QUARTER
        self.measure = measure

class Triplet(TimeHolder):
    def __init__(self, duration: Duration = None, measure: 'Measure' = None, notes: list[TimeHolder]=None, parent=None):
        self.duration = duration if duration is not None else Duration.QUARTER
        self.notes = notes if notes is not None else []
        self.measure = measure
    
class Note():
    def __init__(self, time, pitch, duration = None, measure: 'Measure' = None):
        self.duration = duration if duration is not None else Duration.QUARTER
        self.measure = measure
        self.time = time
        self.__pitch = pitch
        
    def set_pitch(self, p):
        self.__pitch = p
        # self.assure_pitch()
    
    def get_pitch(self):
        res = self.__pitch
        # self.assure_pitch()
        return self.__pitch
    
    def assure_pitch(self):
        if -100 <= self.__pitch <= 100:
            pass
        else:
            abdfsdf = 234
          
            
class Measure():
    def __init__(self, notes: list[TimeHolder]=None, parent=None):
        self.time_holders = [] if notes is None else notes

class Part():
    def __init__(self, measures: list[Measure]=None, piece=None):
        self.piece = piece
        self.measures = [] if measures is None else measures

class TempoMark():
    def __init__(self, bpm: float, bpm_base: Duration, bar_no: int, bar_offset: Ratio):
        self.bar_no = 0
        self.bpm = bpm
        self.bmp_base = bpm_base
        self.bar_no = bar_no
        self.bar_offset = bar_offset

class ConductorPart():
    def __init__(self, initial_tempo_mark: TempoMark):
        self.base_tempo_mark = initial_tempo_mark
        self.tempo_marks: list[TempoMark] = [initial_tempo_mark]
        pass
    
class Piece():
    def __init__(self, parts: list[Part]=None, conductor_part: ConductorPart = None):
        self.parts = [] if parts is None else parts
        self.conductor_part = conductor_part if conductor_part is not None else ConductorPart()