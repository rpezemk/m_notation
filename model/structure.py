import random
from typing import Any
from PyQt5.QtGui import QColor
from model.duration import Duration

class ParentOf():
    def __init__(self, children:list['ChildOf'] = None):
        self.children = [] if children is None else children
        
    def append_child(self, child: 'ChildOf'):
        child.parent = self
        child.child_no = len(self.children)
        self.children.append(child)
    
class ChildOf():
    def __init__(self, parent:ParentOf = None):
        self.parent = parent
        self.child_no = 0
        
class ParentAndChild(ParentOf, ChildOf):
    def __init__(self, children=None, parent=None):
        self.children = [] if children is None else children
        self.parent=parent
    
    
class TimeHolder(ChildOf):
    def __init__(self, duration: Duration = Duration.QUARTER, parent: ParentOf = None):
        super().__init__(parent=parent)
        self.duration = duration
    
    
class Rest(TimeHolder):
    def __init__(self, duration = Duration.QUARTER, parent: ParentOf = None):
        super().__init__(duration=duration, parent=parent)
    
    
class Note(TimeHolder):
    def __init__(self, time, pitch, duration = Duration.QUARTER, parent: ParentOf = None):
        super().__init__(duration=duration, parent=parent)
        self.time = time
        self.__pitch = pitch
        
    def set_pitch(self, p):
        self.__pitch = p
        self.assure_pitch()
    
    def get_pitch(self):
        res = self.__pitch
        self.assure_pitch()
        return self.__pitch
    
    def assure_pitch(self):
        if -100 <= self.__pitch <= 100:
            pass
        else:
            abdfsdf = 234