import threading
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QFont
from typing import Callable
from enum import Enum
from utils.async_utils import WrappedJob
from utils.informable import Informable


class SyncButton(QPushButton):
    def __init__(self, text, sync_click_func=None):
        super().__init__(text)
        self.setStyleSheet("color: white;")
        font = QFont("Courier New") 
        font.setStyleHint(QFont.Monospace)  
        self.setFont(font)
        self.setFixedHeight(30)
        self.clicked.connect(sync_click_func)
    
    
class AsyncButton(QPushButton):
    def __init__(self, text, sync_click_func=None):
        super().__init__(text)
        self.setStyleSheet("color: white;")
        font = QFont("Courier New") 
        font.setStyleHint(QFont.Monospace)  
        self.setFont(font)
        self.setFixedHeight(30)
        self.wrapped_job = WrappedJob(job_func=sync_click_func)
        self.clicked.connect(self.wrapped_job.try_run)
    
class IndicatorButton(QPushButton, Informable):
    def __init__(self, text, sync_click_func=None, bool_func: Callable[[bool], None] = None):
        super().__init__(text)
        self.setStyleSheet("color: white;")
        font = QFont("Courier New") 
        font.setStyleHint(QFont.Monospace)  
        self.setFont(font)
        self.setFixedHeight(30)
        self.wrapped_job = WrappedJob(job_func=sync_click_func)
        self.clicked.connect(self.wrapped_job.try_run)
        self.bool_func = bool_func if bool_func is not None else ...
        self.state = False
        
    def set_state(self, state: bool):
        print(f"IndicatorButton.set_state: {state}")
        self.state = state
        if state:
            self.setStyleSheet("background: black;")
        else:
            self.setStyleSheet("background: red;")
        self.update()