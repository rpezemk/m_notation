import random
from typing import Any
from PyQt5.QtGui import QColor
from model.duration import Duration

class ParentOf():
    def __init__(self, children:list['ChildOf'] = []):
        self.children = children
        
    def append_child(self, child: 'ChildOf'):
        child.parent = self
        self.children.append(child)
        child.child_no = len(self.children)
    
class ChildOf():
    def __init__(self, parent:ParentOf = None):
        self.parent = parent
        self.child_no = 0
        
class ParentAndChild(ParentOf, ChildOf):
    def __init__(self, children=None, parent=None):
        ParentOf.__init__(self, children=children)  # Directly calling ParentOf's __init__
        ChildOf.__init__(self, parent=parent)  
    
    
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
        self.pitch = pitch