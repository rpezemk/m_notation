from typing import Any, Callable
from PyQt5.QtCore import Qt

class MCmd():
    def __init__(self, name: str, keys: list[Qt.Key|str|Qt.MouseButton], func: Callable[[Any], Any]):
        self.name = name, 
        self.func = func
        self.keys = keys

    def check_match(self, keys) -> bool:
        for k in keys:
            ...

        return True
        
        

