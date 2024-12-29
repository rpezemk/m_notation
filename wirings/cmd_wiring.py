from PyQt5.QtCore import Qt
from utils.commands.command import CompoundCommand, SubCmd
from utils.commands.kbd_resolver import KbdResolver
from utils.logger import MLogger

A = SubCmd("A", [Qt.Key_A])
CTRL_T = SubCmd("CTRL_T", [Qt.Key_Control, Qt.Key_T])
CTRL_X = SubCmd("CTRL_X", [Qt.Key_Control, Qt.Key_X])
CTRL_Q = SubCmd("CTRL_Q", [Qt.Key_Control, Qt.Key_Q])
CTRL_R = SubCmd("CTRL_R", [Qt.Key_Control, Qt.Key_R])
SPACE = SubCmd("PLAY", [Qt.Key_Space])
RETURN = SubCmd("PLAY", [Qt.Key_Return])
ARROW_LEFT = SubCmd("ARROW_LEFT", [Qt.Key_Left]) #16777236
ARROW_RIGHT = SubCmd("ARROW_RIGHT", [Qt.Key_Right]) 
ARROW_UP = SubCmd("ARROW_UP", [Qt.Key_Up])
ARROW_DOWN = SubCmd("ARROW_DOWN", [Qt.Key_Down])
# ALL = CompoundCommand("ALL", [A], lambda: print("A-ALL")),
# ALL = CompoundCommand("RENAME", [CTRL_R, CTRL_R], lambda: print("RENAME")),
# ALL = CompoundCommand("DELETE", [CTRL_T, CTRL_X], lambda: print("DELETE")),
# ALL = CompoundCommand("CLOSE", [CTRL_T, CTRL_Q], lambda: print("CLOSE")),
# ALL = CompoundCommand("SPACE", [SPACE], lambda: print("SPACE")),
# ALL = CompoundCommand("RETURN", [RETURN], lambda: print("RETURN")),
PREV = CompoundCommand("ARROW_LEFT", [ARROW_LEFT])
NEXT = CompoundCommand("ARROW_RIGHT", [ARROW_RIGHT])
UP = CompoundCommand("ARROW_UP", [ARROW_UP])
DOWN = CompoundCommand("ARROW_DOWN", [ARROW_DOWN])

my_wirings = [
    NEXT,
    PREV,
    UP,
    DOWN
]

Log = MLogger(print)
root_kbd_resolver = KbdResolver(my_wirings, lambda s: Log.log(s))