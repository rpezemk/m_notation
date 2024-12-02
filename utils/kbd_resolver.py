from typing import Any, Callable
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

my_set = [Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt]

class KbdResolver():
    def __init__(self):
        self.normal_keys = []
        self.modifiers = None
        

    def try_resolve_new_kbd_press(self, event: QKeyEvent):
        key = event.key()
        if key in my_set:
            print("from my_set")
        if key not in self.normal_keys:
            self.normal_keys.append(key)
            return True, self.normal_keys
        return False, []
        
    def try_resolve_new_kbd_release(self, event: QKeyEvent):
        key = event.key()
        if key in my_set:
            print("from my_set")
        self.modifiers = event.modifiers()
        self.modifiers & Qt.ControlModifier
        if key in self.normal_keys:
            self.normal_keys.remove(key)
            return True, self.normal_keys
        return False, []
        
        

        # Check for specific combinations