from typing import Any, Callable
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QWidget

class SubCmdState(Enum):
    FAIL = 0
    PART_OK = 1
    TOTAL_MATCH = 2



class SubCmd():
    def __init__(self, name: str, keys: list[Qt.Key|str|Qt.MouseButton]):
        self.name = name
        self.keys = keys

    def check_sub(self, keys) -> SubCmdState:
        if len(keys) > len(self.keys):
            return SubCmdState.FAIL

        for idx, k in enumerate(keys):
            i = idx
            el = k

        maybe_matching = [k in self.keys for idx, k in enumerate(keys)]
        is_match = all(maybe_matching)

        if not is_match:
            return SubCmdState.FAIL
        elif len(keys) == len(self.keys):
            return SubCmdState.TOTAL_MATCH
        else:
            return SubCmdState.PART_OK

    def __str__(self):
        abc = ", ".join([str(k) for k in self.keys])
        return self.name + ":  " + abc


class CompoundCommand():
    def __init__(self, name: str, sub_commands: list[SubCmd]):
        self.name = name
        self.sub_commands = sub_commands
        self.sub_no = 0
        self.curr_sub_cmd = sub_commands[0]

    def reset(self):
        self.sub_no = 0
        self.curr_sub_cmd = self.sub_commands[0]


    def check_match(self, keys) -> SubCmdState:
        sub_res = self.curr_sub_cmd.check_sub(keys)
        if sub_res == SubCmdState.FAIL:
            self.reset()
            return SubCmdState.FAIL
        elif sub_res == SubCmdState.TOTAL_MATCH:
            self.sub_no += 1
            self.curr_sub_cmd = self.sub_commands[self.sub_no]
            if self.sub_no == len(self.sub_commands) - 1:
                return SubCmdState.TOTAL_MATCH
            else:
                return SubCmdState.PART_OK
        elif sub_res == SubCmdState.PART_OK:
            return SubCmdState.PART_OK


    def __str__(self):
        abc = "".join(["\n    " + str(k) for k in self.sub_commands])
        return self.name + abc


