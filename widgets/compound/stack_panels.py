from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton

from widgets.compound.base_compound import MyCompound


class HStack(MyCompound):
    def __init__(self, margin: tuple|list = None, spacing: int=None, children: list[MyCompound] = None):
        super().__init__(QHBoxLayout)
        if margin is not None:
            self.set_content_margins(margin[0], margin[1], margin[2], margin[3])
        if spacing is not None:
            self.set_spacing(spacing)
        if children is not None:
            for c in children:
                if isinstance(c, MyCompound):
                    self.layout.addWidget(c.widget)
                elif isinstance(c, QWidget):
                    self.layout.addWidget(c)
                    
    def set_spacing(self, spacing: int):
        self.layout.setSpacing(spacing)
        return self
    
    def set_content_margins(self, l, t, r, b):
        self.layout.setContentsMargins(l, t, r, b)
        return self
    
class VStack(MyCompound):
    def __init__(self, margin: tuple|list = None, children: list[MyCompound] = None, black_on_white=False):
        super().__init__(QVBoxLayout)
        if margin is not None:
            self.set_content_margins(margin[0], margin[1], margin[2], margin[3])
        if children is not None:
            for c in children:
                if isinstance(c, MyCompound):
                    self.layout.addWidget(c.widget)
                elif isinstance(c, QWidget):
                    self.layout.addWidget(c)
        if black_on_white:
            self.widget.setStyleSheet("background-color: lightgray; border-right: 1px solid black;")
            
    def fixed_width(self, width: int):
        self.widget.setFixedWidth(width)  
        return self
    
    def add_stretch(self):
        self.layout.addStretch()  
        return self
    
    def set_content_margins(self, l, t, r, b):
        self.layout.setContentsMargins(l, t, r, b)
        return self