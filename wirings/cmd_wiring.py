from PyQt5.QtCore import Qt
from utils.commands.command import CompoundCommand, SubCmd

A = SubCmd("A", [Qt.Key_A])
CTRL_T = SubCmd("CTRL_T", [Qt.Key_Control, Qt.Key_T])
CTRL_X = SubCmd("CTRL_X", [Qt.Key_Control, Qt.Key_X])
CTRL_Q = SubCmd("CTRL_Q", [Qt.Key_Control, Qt.Key_Q])
CTRL_R = SubCmd("CTRL_R", [Qt.Key_Control, Qt.Key_R])
SPACE = SubCmd("PLAY", [Qt.Key_Space])
RETURN = SubCmd("PLAY", [Qt.Key_Return])
ARROW_RIGHT = SubCmd("ARROW_RIGHT", [Qt.Key_Right]) #16777236

my_wirings = [
    CompoundCommand("ALL", [A], lambda: print("A-ALL")),
    CompoundCommand("RENAME", [CTRL_R, CTRL_R], lambda: print("RENAME")),
    CompoundCommand("DELETE", [CTRL_T, CTRL_X], lambda: print("DELETE")),
    CompoundCommand("CLOSE", [CTRL_T, CTRL_Q], lambda: print("CLOSE")),
    CompoundCommand("SPACE", [SPACE], lambda: print("SPACE")),
    CompoundCommand("RETURN", [RETURN], lambda: print("RETURN")),
    CompoundCommand("ARROW_RIGHT", [ARROW_RIGHT], lambda: print("ARROW_RIGHT"))
]
