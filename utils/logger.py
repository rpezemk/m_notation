from typing import Callable
from enum import Enum

class LogLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    ERROR = 3
    CRITICAL = 4

class MLogger():
    def __init__(self, log_func: Callable[[str],None]):
        self.log_func = log_func
        pass
    
    def log(self, txt: str, level: LogLevel = LogLevel.INFO):
        if self.log_func is not None:
            self.log_func(txt)
            

Log: MLogger = None