from PyQt5.QtWidgets import QWidget

from widgets.compound.stretch import Stretch

class MyCompound():
    def __init__(self, 
                 t: type, 
                 margin: tuple|list = None, 
                 spacing: int=None, 
                 children: list['MyCompound'] = None,
                 black_on_white=False, 
                 stretch = None
                 ):
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color: black;")
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
        if black_on_white:
            self.widget.setStyleSheet("background-color: lightgray; border-right: 1px solid black;")

        
    def add_stretch(self, Stretch):
        self.layout.addStretch()   

    def add_widgets(self, widgets: list[QWidget]):
        for w in widgets:
            self.layout.addWidget(w)
        return self
            
