from typing import Callable
from PyQt5.QtWidgets import QWidget, QLayout

from widgets.compound.stretch import Stretch
from utils.commands.command import CompoundCommand, SubCmd

class MyCompound(QWidget):
    def __init__(self, 
                 t: type[QLayout], 
                 margin: tuple|list = None, 
                 spacing: int=None, 
                 children: list['MyCompound'] = None,
                 stretch = None
                 ):
        self.widget = self
        super().__init__()
        self.layout = t(self.widget)
        if spacing is not None:
            self.layout.setSpacing(spacing)
        else:
            self.layout.setSpacing(0) 

        if children is not None:
            for c in children:
                if isinstance(c, MyCompound):
                    self.layout.addWidget(c.widget)
                elif isinstance(c, QWidget):
                    self.layout.addWidget(c)
                elif isinstance(c, Stretch):
                    self.add_stretch(c)
                    
        if stretch:
            self.layout.addStretch()   
            
        if margin is not None:
            self.layout.setContentsMargins(*margin)
        else:
            self.layout.setContentsMargins(0, 0, 0, 0)
            
        self.commands: list[tuple[CompoundCommand, Callable]] = []
                
    def add_stretch(self, Stretch):
        self.layout.addStretch()   

    def add_widgets(self, widgets: list[QWidget]):
        for w in widgets:
            self.layout.addWidget(w)
        return self
            
