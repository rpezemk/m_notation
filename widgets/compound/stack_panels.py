from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from widgets.compound.base_compound import MyCompound


class HStack(MyCompound):
    def __init__(self, 
                 margin: tuple|list = None, 
                 spacing: int = 0,
                 children: list[MyCompound] = None,
                 stretch = True, 
                 fixed_height = -1):
        super().__init__(QHBoxLayout, 
                         margin=margin, 
                         spacing=spacing, 
                         children=children, 
                         stretch=stretch)
        if fixed_height >= 0:
            self.widget.setFixedHeight(fixed_height)  
            


class VStack(MyCompound):
    def __init__(self, 
                 margin: tuple|list = None, 
                 spacing: int = 0,
                 children: list[MyCompound] = None,
                 stretch = True,
                 fixed_width=-1):
        super().__init__(QVBoxLayout, 
                         margin=margin, 
                         spacing=spacing, 
                         children=children, 
                         stretch=stretch)
        if fixed_width >= 0:
            self.widget.setFixedWidth(fixed_width)  
    

        