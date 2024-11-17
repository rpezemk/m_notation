from typing import Tuple
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton

def emit_score_view(parent_widget: QMainWindow = None, type = None) -> Tuple[QWidget, QVBoxLayout]:
    widget = QWidget(parent_widget)
    layout = type(widget)
    layout.setSpacing(0)  
    layout.setContentsMargins(0, 0, 0, 0)  
    parent_widget.setStyleSheet("background-color: black;")
    return widget, layout


def emit_widget_with_pane(parent: QWidget, ) -> Tuple[QWidget, QVBoxLayout]:
    central_widget = QWidget(parent)
        
    # Create a horizontal layout
    h_layout = QHBoxLayout(central_widget)

    # Add some buttons to the layout
    btn_0 = QPushButton("Button 1")
    btn_0.setFixedWidth(100)
    h_layout.addWidget(btn_0)
    h_layout.addWidget(central_widget)
    return central_widget, h_layout