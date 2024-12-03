import time
from typing import Any, Callable, Tuple
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
my_set = [Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt]

class KbdResolver():
    def __init__(self):
        self.curr_keys = []

    def is_machine_time(self, t1, t2):
        diff = t1 - t2
        return abs(diff) < 0.01
    
    def try_resolve_new_kbd_press(self, event: QKeyEvent):
        key = event.key()  
        if key not in self.curr_keys:
            self.curr_keys.append(key)
        if event.isAutoRepeat():
            return False, self.curr_keys
        return True, self.curr_keys
        
    def try_resolve_new_kbd_release(self, event: QKeyEvent):
        key = event.key()
        if key in self.curr_keys:
            self.curr_keys.remove(key)
        if event.isAutoRepeat():
            return False, self.curr_keys
        return True, self.curr_keys

        