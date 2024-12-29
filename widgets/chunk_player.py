import time
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

from model.musical.structure import Chunk

class RulerPlayer(QThread):
    signal = pyqtSignal(int, int)
    def __init__(self, chunk: Chunk):
        super().__init__()
        self.ruler_bars = chunk.to_ruler_bars()

    def run(self):
        for bar_no,ruler_bar in enumerate(self.ruler_bars):
            for e_no,evt in enumerate(ruler_bar):
                print(f"{evt}")
                self.signal.emit(bar_no, e_no)
                for th in evt.inner_events:
                    ...
                    
                time.sleep(evt.len_ratio.to_float()*4)
                    
    def set_chunk(self, chunk: Chunk):
        self.ruler_bars = chunk.to_ruler_bars()

    



