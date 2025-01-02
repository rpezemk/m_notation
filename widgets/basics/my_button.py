import threading
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QFont
from enum import Enum
from utils.async_utils import WrappedJob


class SyncButton(QPushButton):
    def __init__(self, text, sync_click_func=None, color_hex: str=None):
        super().__init__(text)
        if color_hex:
            self.setStyleSheet(f"""
            QPushButton, AsyncButton, SyncButton {{
                border: 1px solid #999999;
                background-color: {color_hex};
                color: white;
                padding: 1px 12px 1px 12px;
            }}
                               """)
        font = QFont("Courier New") 
        font.setStyleHint(QFont.Monospace)  
        self.setFont(font)
        self.setFixedHeight(30)
        if sync_click_func:
            self.clicked.connect(sync_click_func)
    
    
class AsyncButton(QPushButton):
    def __init__(self, text, sync_click_func=None):
        super().__init__(text)
        font = QFont("Courier New") 
        font.setStyleHint(QFont.Monospace)  
        self.setFont(font)
        self.setFixedHeight(30)
        self.wrapped_job = WrappedJob(job_func=sync_click_func)
        self.clicked.connect(self.wrapped_job.try_run)
    
class StateButton(QPushButton):
    def __init__(self, text, state_on_func=None, state_off_func=None, color_hex_on: str=None, color_hex_off: str=None):
        super().__init__(text)
        self.state = False
        self.state_on_func = state_on_func
        self.state_off_func = state_off_func
        self.clicked.connect(self.flip_state)
        self.color_hex_on = "#AA2222" if color_hex_on is None else color_hex_on
        self.color_hex_off = "#332222" if color_hex_off is None else color_hex_off
        
        self.set_color(self.color_hex_off)

        
        font = QFont("Courier New") 
        font.setStyleHint(QFont.Monospace)  
        self.setFont(font)
        self.setFixedHeight(30)
    
    def flip_state(self):
        self.set_state(not self.state)

    def set_state(self, state: bool):
        self.state = state
        if self.state and self.state_on_func:
            self.state_on_func()
        elif not self.state and self.state_off_func:
            self.state_off_func()
    
        if self.state:
            self.set_color(self.color_hex_on)
        else:
            self.set_color(self.color_hex_off)
                    
    def set_color(self, color):
        self.setStyleSheet(f"""
            QPushButton, AsyncButton, SyncButton {{
                border: 1px solid #999999;
                background-color: {color};
                color: white;
                padding: 1px 12px 1px 12px;
            }}""")