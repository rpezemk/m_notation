import threading
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QFont
from typing import Callable
from enum import Enum
from utils.async_utils import WrappedJob


class AsyncBlockingButton(QPushButton):
    def __init__(self, text, sync_click_func=None):
        super().__init__(text)
        self.setStyleSheet("color: white;")
        font = QFont("Courier New") 
        font.setStyleHint(QFont.Monospace)  
        self.setFont(font)
        self.setFixedHeight(30)
        self.wrapped_job = WrappedJob(job_func=sync_click_func)
        self.clicked.connect(self.wrapped_job.try_run)
    
    def run_sync(self, func: Callable[[], None]):
        pass        
        t1 = threading.Thread(target=self.sync_click_func, args=[])
        t1.start()