from utils.async_utils import WrappedJob
from utils.hierarchy.informable import Informable


from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton


from typing import Callable


class IndicatorButton(QPushButton, Informable):
    def __init__(self, text, sync_click_func=None, bool_func: Callable[[bool], None] = None):
        super().__init__(text)
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
        self.update()