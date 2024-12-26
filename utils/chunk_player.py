import time
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

from model.chunk import CsEvent
from model.chunk import RulerEvent
from model.chunk import Chunk

class RulerPlayer(QThread):
    def __init__(self, chunk: Chunk):
        super().__init__()
        self.ruler_bars = chunk.to_ruler_bars()
    
    def __call__(self, *args, **kwds):
        self.signal = pyqtSignal(RulerEvent)
        return super().__call__(*args, **kwds)

    def run(self):
        for ruler_bar in self.ruler_bars:
            for evt in ruler_bar:
                for e in evt.inner_events:
                    ...
        # for i in range(5):
        #     time.sleep(1)  # Simulate a time-consuming task
        #     print(i)
            # self.signal.emit(f"Step {i + 1} completed")
        # self.signal.emit("Task finished")
    
    
    def play_group(self, time_group: RulerEvent):
        ...
        
    def play(self):
        self.worker.start()
    
    
        
    def set_chunk(self, chunk: Chunk):
        self.ruler_bars = chunk.to_ruler_bars()

    



