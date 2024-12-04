from PyQt5.QtCore import Qt
from utils.commands.command import CompoundCommand, SubCmd

CTRL_T = SubCmd("CTRL_T", [Qt.Key_Control, Qt.Key_T])
CTRL_X = SubCmd("CTRL_X", [Qt.Key_Control, Qt.Key_X])
CTRL_Q = SubCmd("CTRL_Q", [Qt.Key_Control, Qt.Key_Q])
CTRL_R = SubCmd("CTRL_R", [Qt.Key_Control, Qt.Key_Q])


my_wirings = [
    CompoundCommand("RENAME", [CTRL_R, CTRL_R], lambda: print("DO_STH WORKING")),
    CompoundCommand("DELETE", [CTRL_T, CTRL_X], lambda: print("DO_STH WORKING")),
    CompoundCommand("CLOSE", [CTRL_T, CTRL_Q], lambda: print("DO_STH WORKING"))
]
