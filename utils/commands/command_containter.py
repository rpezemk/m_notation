from enum import Enum
from typing import Any, Callable, TypeVar, Generic
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton

from utils.commands.command import CompoundCommand

class BindCmd():
    def __init__(self, v_type: type[QWidget], c_cmd: CompoundCommand, func: Callable[[QWidget], None]):
        self.v_type = v_type
        self.c_cmd = c_cmd
        self.func = func

    def run(self, view: QWidget):
        self.func(view)

class ViewBindingCollection():
    def __init__(self):
        self.widget_type: type[QWidget] = None
        self.binding_commands: list[BindCmd] = []
        self.view_mode: Enum = None
        
    def for_widget(self, widget_type: type[QWidget]):
        self.widget_type = widget_type
        return self
    
    def for_mode(self, view_mode: Enum):
        self.view_mode = view_mode
        return self
        
    def define_bindings(self, binding_commands: list[tuple[CompoundCommand, Callable[[QWidget], None]]]):
        self.binding_commands = [BindCmd(self.widget_type, *t) for t in binding_commands]
        # BindCmd
        return self
    

class CommandContainer():
    builders = []
    
    @staticmethod
    def for_widget(widget_type: type[QWidget]) -> ViewBindingCollection:
        cmd_collection = ViewBindingCollection().for_widget(widget_type)
        CommandContainer.builders.append(cmd_collection)
        return cmd_collection
    



