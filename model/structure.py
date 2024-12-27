import random
from typing import Any
from PyQt5.QtGui import QColor
from model.duration import Dotting, DurationBase
from model.ratio import Ratio

    
class TimeHolder():
    def __init__(self, duration: DurationBase = None, measure: 'Measure' = None, dotting: Ratio = None):
        self.base_duration = duration if duration is not None else DurationBase.QUARTER
        self.dotting = dotting if dotting is not None else Ratio(t=(0, 1))
        self.real_duration = self.base_duration + self.base_duration * self.dotting
        self.measure = measure
        self.offset_ratio = Ratio(t=(0, 1))
        self.is_selected = False
        
    def __str__(self):
        return f"d: {self.base_duration}"
    
    def dot(self):
        self.dotting = Ratio(t=(1, 2))
        self.real_duration = self.base_duration + self.base_duration * self.dotting
        return self
          
    def double_dot(self):
        self.dotting = Ratio(t=(3, 4))
        self.real_duration = self.base_duration + self.base_duration * self.dotting
        return self    
    
    
class Rest(TimeHolder):
    def __init__(self, duration: DurationBase = None, measure: 'Measure' = None, dotting: Dotting = None):
        super().__init__(duration, measure, dotting)
        self.measure = measure

    def __str__(self):
        return f"d: {self.base_duration}"
    
    
class Triplet(TimeHolder):
    def __init__(self, duration: DurationBase = None, measure: 'Measure' = None, notes: list[TimeHolder]=None, parent=None):
        super().__init__(duration, measure)
        self.notes = notes if notes is not None else []
        self.measure = measure
    
    def __str__(self):
        return f"d: {self.base_duration}"
    
class Note(TimeHolder):
    def __init__(self, time, pitch, duration = None, measure: 'Measure' = None, dotting: Dotting = None):
        super().__init__(duration, measure, dotting)
        self.measure = measure
        self.time = time
        self.pitch = pitch
                          
    def __str__(self):
        return f"d: {self.base_duration}"
    
                
class Measure():
    def __init__(self, notes: list[TimeHolder]=None, parent=None):
        self.time_holders = [] if notes is None else notes


class Part():
    def __init__(self, measures: list[Measure]=None, piece=None):
        self.piece = piece
        self.measures = [] if measures is None else measures


class TempoMark():
    def __init__(self, bpm: float, bpm_base: DurationBase, bar_no: int, bar_offset: Ratio):
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
    
    
