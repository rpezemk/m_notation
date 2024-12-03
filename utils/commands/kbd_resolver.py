from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt

class KbdResolver():
    def __init__(self):
        self.curr_keys = []
    
    def try_resolve_new_kbd_press(self, event: QKeyEvent):
        key = event.key()  
        if key not in self.curr_keys:
            self.curr_keys.append(key)
        return not event.isAutoRepeat(), self.curr_keys
        
    def try_resolve_new_kbd_release(self, event: QKeyEvent):
        key = event.key()
        if key in self.curr_keys:
            self.curr_keys.remove(key)
        return not event.isAutoRepeat(), self.curr_keys

        