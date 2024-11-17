import random
from typing import Any
from PyQt5.QtGui import QColor
from model.duration import Duration

class ParentOf():
    def __init__(self, children:list['ChildOf'] = []):
        self.children = children

class ChildOf():
    def __init__(self, parent:ParentOf = None):
        self.parent = parent

class ParentAndChild(ParentOf, ChildOf):
    def __init__(self, children=None, parent=None):
        ParentOf.__init__(self, children=children)  # Directly calling ParentOf's __init__
        ChildOf.__init__(self, parent=parent)  
    
    
class TimeHolder():
    def __init__(self, duration: Duration = Duration.QUARTER):
        self.duration = duration
    
    
class Rest(TimeHolder):
    def __init__(self, duration = Duration.QUARTER):
        super().__init__(duration=duration)
    
    
class Note(TimeHolder):
    def __init__(self, x, y, color, duration = Duration.QUARTER):
        super().__init__(duration=duration)
        self.time = x
        self.pitch = y
        self.color = color