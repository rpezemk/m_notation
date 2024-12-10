from typing import Callable
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QFont

class ComboBox(QComboBox):
    def __init__(self, values, func: Callable[[str], None], dict_to_str_func: Callable[[dict], str] = None):
        super().__init__()
        self.setStyleSheet("color: white;")
        font = QFont("Courier New", 12) 
        font.setStyleHint(QFont.Monospace)  
        self.setFont(font)
        self.func = func
        self.objects = values
        self.currentIndexChanged.connect(self.__sel_change__)  # Connect signal
        
        if len(values) == 0:
            return
        
        if isinstance(values[0], str):
            self.addItems(values)
        elif isinstance(values[0], dict) and dict_to_str_func:
            self.addItems([dict_to_str_func(val) for val in values])  # Add values
        
        
    def __sel_change__(self, idx: int) -> None:
        txt = self.objects[idx]
        self.func(txt)
    
    def get_curr_val(self):
        idx = self.currentIndex()
        val = self.objects[idx]
        return val
    

    