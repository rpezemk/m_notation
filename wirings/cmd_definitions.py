from PyQt5.QtCore import Qt
from utils.commands.command import CompoundCommand, SubCmd
from utils.commands.command_containter import BindCmd, CommandContainer
from utils.commands.kbd_resolver import KbdResolver

K_CTRL = Qt.Key_Control
K_A = Qt.Key_A
K_T = Qt.Key_T
K_X = Qt.Key_X
K_Q = Qt.Key_Q
K_R = Qt.Key_R
K_SP = Qt.Key_Space


A = SubCmd("A", [Qt.Key_A])
CTRL_A = SubCmd("CTRL_A", [K_CTRL, K_A])
CTRL_T = SubCmd("CTRL_T", [K_CTRL, K_T])
CTRL_X = SubCmd("CTRL_X", [K_CTRL, K_X])
CTRL_Q = SubCmd("CTRL_Q", [K_CTRL, K_Q])
CTRL_R = SubCmd("CTRL_R", [K_CTRL, K_R])

S_SPACE = SubCmd("PLAY", [Qt.Key_Space])
S_RETURN = SubCmd("PLAY", [Qt.Key_Return])
S_ARROW_LEFT = SubCmd("ARROW_LEFT", [Qt.Key_Left]) #16777236
S_ARROW_RIGHT = SubCmd("ARROW_RIGHT", [Qt.Key_Right]) 
S_ARROW_UP = SubCmd("ARROW_UP", [Qt.Key_Up])
S_ARROW_DOWN = SubCmd("ARROW_DOWN", [Qt.Key_Down])

C_SELECT_ALL = CompoundCommand("SELECT_ALL", [CTRL_A]),
C_RENAME = CompoundCommand("RENAME", [CTRL_R, CTRL_R]),
C_DELETE = CompoundCommand("DELETE", [CTRL_T, CTRL_X]),
C_PLAY = CompoundCommand("PLAY", [S_SPACE]),
C_PLAY_SPECIAL = CompoundCommand("PLAY_SPECIAL", [S_RETURN]),

CMD_PREV = CompoundCommand("ARROW_LEFT", [S_ARROW_LEFT])
CMD_NEXT = CompoundCommand("ARROW_RIGHT", [S_ARROW_RIGHT])
CMD_UP = CompoundCommand("ARROW_UP", [S_ARROW_UP])
CMD_DOWN = CompoundCommand("ARROW_DOWN", [S_ARROW_DOWN])

