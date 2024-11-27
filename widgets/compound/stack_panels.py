from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from widgets.compound.base_compound import MyCompound


class HStack(MyCompound):
    def __init__(self, 
                 margin: tuple|list = None, 
                 spacing: int = None,
                 children: list[MyCompound] = None, 
                 black_on_white = False, 
                 stretch = False):
        super().__init__(QHBoxLayout, 
                         margin=margin, 
                         spacing=spacing, 
                         children=children, 
                         stretch=stretch, 
                         black_on_white=black_on_white)

class VStack(MyCompound):
    def __init__(self, 
                 margin: tuple|list = None, 
                 spacing: int = None,
                 children: list[MyCompound] = None, 
                 black_on_white = False, 
                 stretch = False,
                 fixed_width=-1):
        super().__init__(QVBoxLayout, 
                         margin=margin, 
                         spacing=spacing, 
                         children=children, 
                         stretch=stretch, 
                         black_on_white=black_on_white)
        if fixed_width >= 0:
            self.widget.setFixedWidth(fixed_width)  
            