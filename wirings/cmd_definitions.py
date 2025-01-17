from PyQt5.QtCore import Qt
from utils.commands.command import CompoundCommand, SubCmd
from utils.commands.command_containter import BindCmd, CommandContainer
from utils.commands.kbd_resolver import KbdResolver

######## KEYS ##########


def cmd(defs: list[list[int]]):
    res = CompoundCommand("", [SubCmd("", keys) for keys in defs])
    return res


    