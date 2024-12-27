from enum import Enum
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from utils.commands.command import CompoundCommand, SubCmdState
from typing import Callable

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

def merge_comds_to_dictionary(commands: list[CompoundCommand], notify_func: Callable = None):
    root = {}
    curr_d = root
    for c in commands:
        for sub in c.sub_commands:
            curr_d[sub.keys] = {}
            curr_d = curr_d[sub]
        curr_d["name"] = c.name
        curr_d["func"] = c.func
        curr_d = root
    return root

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
                win_cmd.func()
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
    def __init__(self, commands: list[CompoundCommand], notify_func: Callable):
        self.curr_keys = []
        self.notify_func = notify_func
        self.state = None
        self.automaton = Automaton(commands, notify_func)
        self.curr_keys = set()
        self.curr_modifiers = set()
        self.prev_keys = set()
        
    def clear(self):
        self.curr_keys = set()
        self.automaton.reset()
        
    def accept_token(self, option: KbdOption, keys: list[int]):
        ...
        
        success, cmd = self.automaton.try_resolve(keys)
        ... # TODO passing cmds 
                
    def accept_press(self, key: int, autorepeat: bool = False):
        if autorepeat:
            return
        if key not in self.curr_keys: 
            self.curr_keys.add(key)
        
        for ck in self.curr_keys:
            print(ck)
        
        if is_modifier(key):
            return
        
        self.accept_token(KbdOption.PRESS, self.curr_keys)     
            
    def accept_release(self, key: int, autorepeat: bool = False):
        if autorepeat:
            return
        
        if key in self.curr_keys: 
            self.curr_keys.remove(key)
            # self.notify_func(f"removed: {key}")
        