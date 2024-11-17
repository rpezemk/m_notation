from typing import Tuple
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

def emit_central_pair(parent_widget: QMainWindow = None, type = None) -> Tuple[QWidget, QVBoxLayout]:
    widget = QWidget(parent_widget)
    layout = type(widget)
    parent_widget.setCentralWidget(widget)
    layout.setSpacing(0)  
    layout.setContentsMargins(0, 0, 0, 0)  
    parent_widget.setStyleSheet("background-color: black;")
    return widget, layout
