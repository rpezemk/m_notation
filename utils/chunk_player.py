import time
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

from model.chunk import CsEvent
from model.chunk import EventTimeGroup
from model.chunk import Chunk

class ChunkPlayer(QThread):
    def __init__(self, chunk: Chunk):
        super().__init__()
        
        self.chunk = chunk
        self.groups_by_h_idx: list[list[EventTimeGroup]] = []
        self.process_chunk()
    
    def __call__(self, *args, **kwds):
        self.signal = pyqtSignal(EventTimeGroup)
        return super().__call__(*args, **kwds)

    def run(self):
        for bar_time_group in self.groups_by_h_idx:
            lengths = [bar_time_group[idx + 1].offset_ratio - bar_time_group[idx].offset_ratio for idx in range(len(bar_time_group))]
            # last_len =
            # for a in bar_time_group:
            #     time.sleep(a.len)
            #     for e in a.events:
                    
        for i in range(5):
            time.sleep(1)  # Simulate a time-consuming task
            print(i)
            # self.signal.emit(f"Step {i + 1} completed")
        # self.signal.emit("Task finished")
    
    
    def play_group(self, time_group: EventTimeGroup):
        ...
        
    def play(self):
        self.worker.start()
    
    
        
    def set_chunk(self, chunk: Chunk):
        self.chunk = chunk
        self.process_chunk()
    
    def process_chunk(self):
        ruler_bars = self.chunk.to_ruler_bars()
        self.groups_by_h_idx = []
        for h_idx, ruler_bar in enumerate(ruler_bars):
            measure_groups: list[EventTimeGroup] = []
            for evt in ruler_bar:
                v_chunk = self.chunk.v_chunks[h_idx]
                maybe = [th for m in v_chunk.vertical_measures for th in m.time_holders if th.offset_ratio == evt.offset_ratio]
                if not maybe:
                    continue
                group = EventTimeGroup()
                group.offset_ratio = evt.offset_ratio

                for th in maybe:
                    cs_evt = CsEvent(1, 0.0, th.duration.to_ratio().to_float())
                    group.events.append(cs_evt)
                measure_groups.append(group)
                
            self.groups_by_h_idx.append(measure_groups)



