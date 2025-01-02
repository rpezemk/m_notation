from enum import Enum
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from utils.commands.command import CompoundCommand, SubCmdState
from typing import Callable
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton

from utils.commands.command_containter import ViewBindingCollection
from widgets.compound.base_compound import MyCompound
from widgets.views.view import View

modifiers = [Qt.Key_Shift, Qt.Key_Control, Qt.Key_Alt, Qt.Key_Meta]

def is_modifier(key: int):
    res = key in modifiers
    return res

class CmdState(Enum):
    ResetNoAction = 0
    CmdFired = 1
    CmdCanGoFurther = 2

class KbdOption(Enum):
    RELEASE = 0
    PRESS = 0
    

class KbdEvent():
    def __init__(self, ):
        pass
        self.key: int

class Node():
    def __init__(self, ):
        pass

class Automaton():
    def __init__(self, commands: list[CompoundCommand], notify_func: Callable):
        self.commands = commands
        self.notify_func = notify_func
        self.level = 0
        self.filtered = list(commands)

    def reset(self):
        self.notify_func("RESET")
        self.filtered = list(self.commands)
        self.level = 0
    
    def inc_state(self):
        self.level +=1
        self.notify_func(f"inc: state now: {self.level}")
    
    def dec_state(self):
        self.level -=1
        self.notify_func(f"dec: state now: {self.level}")    
        
    def filter_by_keys(self, commands: list[CompoundCommand], keys: list[int], level) -> tuple[bool,list[CompoundCommand]]:
        res_list = [c for c in commands 
                    if  (len(c.sub_commands) > level ) 
                    and (c.sub_commands[level].check_sub(keys) != SubCmdState.FAIL)]
        
        return len(res_list) > 0, res_list
    
    def try_resolve(self, keys: list[int]) -> tuple[bool, CompoundCommand]:
        ok, lst = self.filter_by_keys(self.filtered, keys, self.level)
        if not ok:
            self.notify_func("NOT OK --> reset")
            self.reset()
            return False, None
        
        maybe_total = [c for c in lst if c.sub_commands[self.level].check_sub(keys) == SubCmdState.TOTAL_MATCH]
        if maybe_total:
            self.notify_func("some totals")
            win_cmd = maybe_total[0]
            if len(win_cmd.sub_commands) == self.level + 1:
                self.notify_func("WIN!!!")
                # win_cmd.func()
                self.reset()
                return True, win_cmd
            else:
                self.notify_func("INC STATE")
                self.filtered = list(lst)
                self.inc_state()
                return False, None
            
        
        self.notify_func("recalc filtered")
        self.filtered = list(lst)
        return False, None
    
    def __str__(self):
        f = "AUTOMATON:" + "".join(["\n  " + str(f) for f in self.filtered])
        return f
    
    
class KbdResolver():
    def __init__(self, bind_commands: list[ViewBindingCollection], notify_func: Callable = None):
        self.curr_keys = []
        self.notify_func = notify_func if notify_func is not None else print
        self.state = None
        self.bind_commands = bind_commands
        self.curr_keys = set()
        self.curr_modifiers = set()
        self.prev_keys = set()
        self.control = None
        self.automaton: Automaton = None
        
    def set_view(self, widget: View):
        self.control = widget
        commands = [c.c_cmd for bc in self.bind_commands for c in bc.binding_commands if bc.widget_type == type(widget) and bc.view_mode == self.control.mode]
        if not commands:
            self.automaton = None
            return
        
        self.automaton = Automaton(commands, self.notify_func)
        
    def clear_curr_input(self):
        self.curr_keys = set()
        if self.automaton:
            self.automaton.reset()
        
    def accept_token(self, option: KbdOption, keys: list[int]):
        ...
        if not self.automaton:
            return
        
        success, cmd = self.automaton.try_resolve(keys)
        if not success:
            return
        
        commands = [c for bc in self.bind_commands for c in bc.binding_commands if c.c_cmd == cmd]
        if not commands: 
            return
        commands[0].func(self.control)
                
    def accept_press(self, src_widget: QWidget, event):
        key, autorepeat = event.key(), event.isAutoRepeat()
        if autorepeat:
            return
        if key not in self.curr_keys: 
            self.curr_keys.add(key)
        
        if is_modifier(key):
            return
        
        self.accept_token(KbdOption.PRESS, self.curr_keys)     
            
    def accept_release(self, src_widget: QWidget, event):
        key, autorepeat = event.key(), event.isAutoRepeat()
        if autorepeat:
            return
        
        if key in self.curr_keys: 
            self.curr_keys.remove(key)
            # self.notify_func(f"removed: {key}")
        