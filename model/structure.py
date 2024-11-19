import random
from typing import Any
from PyQt5.QtGui import QColor
from model.duration import Duration

    
    
class TimeHolder():
    def __init__(self, duration: Duration = Duration.QUARTER, measure: 'Measure' = None):
        self.measure = measure
        self.duration = duration
    
class Rest(TimeHolder):
    def __init__(self, duration: Duration = Duration.QUARTER, measure: 'Measure' = None):
        self.measure = measure
        self.duration = duration
    
class Note():
    def __init__(self, time, pitch, duration = Duration.QUARTER, measure: 'Measure' = None):
        self.duration = duration
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
    def __init__(self, notes: list[Note]=None, parent=None):
        self.notes = [] if notes is None else notes

class Part():
    def __init__(self, measures: list[Measure]=None, piece=None):
        self.piece = piece
        self.measures = [] if measures is None else measures
    
class Piece():
    def __init__(self, parts: list[Part]=None):
        self.parts = [] if parts is None else parts
