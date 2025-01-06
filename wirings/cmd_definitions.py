from PyQt5.QtCore import Qt
from utils.commands.command import CompoundCommand, SubCmd
from utils.commands.command_containter import BindCmd, CommandContainer
from utils.commands.kbd_resolver import KbdResolver

######## KEYS ##########

K_CTRL = Qt.Key_Control
K_A = Qt.Key_A
K_T = Qt.Key_T
K_V = Qt.Key_V
K_H = Qt.Key_H
K_X = Qt.Key_X
K_Q = Qt.Key_Q
K_R = Qt.Key_R
K_SP = Qt.Key_Space
K_DEL = Qt.Key_Delete
K_ESC = Qt.Key_Escape

K_LEFT = Qt.Key_Left
K_RIGHT = Qt.Key_Right
K_UP = Qt.Key_Up
K_DOWN = Qt.Key_Down



######## PART COMMANDS ##########

A = SubCmd("A", [K_A])
S_CTRL_A = SubCmd("CTRL_A", [K_CTRL, K_A])
S_CTRL_T = SubCmd("CTRL_T", [K_CTRL, K_T])
S_CTRL_V = SubCmd("CTRL_T", [K_CTRL, K_V])
S_CTRL_H = SubCmd("CTRL_T", [K_CTRL, K_H])
S_CTRL_X = SubCmd("CTRL_X", [K_CTRL, K_X])
S_CTRL_Q = SubCmd("CTRL_Q", [K_CTRL, K_Q])
S_CTRL_R = SubCmd("CTRL_R", [K_CTRL, K_R])

S_SPACE = SubCmd("PLAY", [Qt.Key_Space])
S_RETURN = SubCmd("PLAY", [Qt.Key_Return])

S_ARROW_LEFT = SubCmd("ARROW_LEFT", [K_LEFT])
S_ARROW_RIGHT = SubCmd("ARROW_RIGHT", [K_RIGHT]) 
S_ARROW_UP = SubCmd("ARROW_UP", [K_UP])
S_ARROW_DOWN = SubCmd("ARROW_DOWN", [K_DOWN])

S_R = SubCmd("ROTATE", [K_R])

CTRL_ARROW_LEFT = SubCmd("sdf", [K_CTRL, K_LEFT])
CTRL_ARROW_RIGHT = SubCmd("sdf", [K_CTRL, K_RIGHT])
CTRL_ARROW_UP = SubCmd("sdf", [K_CTRL, K_UP])
CTRL_ARROW_DOWN = SubCmd("sdf", [K_CTRL, K_DOWN])

S_DEL = SubCmd("sdf", [K_DEL])
S_ESC = SubCmd("sdf", [K_ESC])



######### COMMANDS ##########

C_SELECT_ALL = CompoundCommand("SELECT_ALL", [S_CTRL_A]),
C_PLAY = CompoundCommand("PLAY", [S_SPACE]),
C_PLAY_SPECIAL = CompoundCommand("PLAY_SPECIAL", [S_RETURN]),

CMD_PREV = CompoundCommand("ARROW_LEFT", [S_ARROW_LEFT])
CMD_NEXT = CompoundCommand("ARROW_RIGHT", [S_ARROW_RIGHT])
CMD_UP = CompoundCommand("ARROW_UP", [S_ARROW_UP])
CMD_DOWN = CompoundCommand("ARROW_DOWN", [S_ARROW_DOWN])

CMD_CTRL_PREV = CompoundCommand("ARROW_LEFT", [CTRL_ARROW_LEFT])
CMD_CTRL_NEXT = CompoundCommand("ARROW_RIGHT", [CTRL_ARROW_RIGHT])
CMD_CTRL_UP = CompoundCommand("ARROW_UP", [CTRL_ARROW_UP])
CMD_CTRL_DOWN = CompoundCommand("ARROW_DOWN", [CTRL_ARROW_DOWN])


CMD_DEL = CompoundCommand("DEL", [S_DEL])
CMD_ROTATE = CompoundCommand("ROTATE", [S_R])
CMD_ESC = CompoundCommand("ESC", [S_ESC])

######## MEASURE COMMANDS #########

C_SEL_VERTICAL_MEASURE = CompoundCommand("SEL_VERT_MEASURE", [S_CTRL_T, S_CTRL_V])
C_SEL_HORIZONTAL_MEASURES = CompoundCommand("SEL_VERT_MEASURE", [S_CTRL_T, S_CTRL_H])