from datetime import datetime
from typing import override
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt


from model.musical.structure import Chunk
from model.ratio import Ratio
from widgets.lanes.BarrableWidget import BarrableWidget
import time

class RulerPlayer(QThread):
    signal = pyqtSignal(int, int)
    def __init__(self, chunk: Chunk):
        super().__init__()
        self.ruler_bars = chunk.to_ruler_bars()
        self.is_running = False
        self.e_no = 0
        self.curr_e_no = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_counter)

        self.dt = 20 # 1/50 sec
        self.timer.start(self.dt)
        self.counter = 0

    def update_counter(self):
        self.counter += 1

    def run(self):
        self.is_running = True

        filtered = [(e_p_idx, *gr)
                       for e_p_idx, gr
                       in enumerate(
                           [
                               (b_idx, gr_idx, gr) for b_idx, bar
                               in enumerate(self.ruler_bars)
                               for gr_idx, gr in enumerate(bar)
                            ])
                    ][self.curr_e_no:]

        for abs_e_no, b_no, gr_idx, grp_evt in filtered:
            if not self.is_running:
                return
            self.curr_e_no = abs_e_no
            self.signal.emit(b_no, gr_idx)
            for th in grp_evt.inner_events:
                if not self.is_running:
                    return
            if not self.try_sleep(grp_evt.len_ratio.to_float()*4):
                return

    def stop(self):
        self.is_running = False

    def reset(self):
        self.is_running = False
        self.curr_e_no = 0

    def try_sleep(self, n_secs):
        cps = 1000//int(self.dt)
        cnt_end = self.counter + n_secs * cps
        cnt_now = self.counter
        while cnt_now < cnt_end:
            time.sleep(self.dt/1000)
            cnt_now = self.counter
            if not self.is_running:
                return False
        return True


class RulerWidget(BarrableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(40)
        self.ruler_bars = []
        self.chunk = None
        self.m_no = 0
        self.e_no = 0
        self.player = None

    def mark_at(self, m_no: int, e_no: int):
        self.m_no = m_no
        self.e_no = e_no

    def start(self):
        self.player.start()

    def stop(self):
        self.player.stop()

    def reset(self):
        if self.player:
            if self.player.is_running:
                self.player.stop()
            self.player.reset()
        self.mark_at(0, 0)

    @override
    def paintEvent(self, event):
        self.no_of_measures = len(self.chunk.h_chunks[0].measures)
        self.get_x_offsets()
        self.draw_content()
        self.update()

    @override
    def set_content(self, chunk: Chunk):
        self.chunk = chunk
        self.ruler_bars = chunk.to_ruler_bars()
        self.player = RulerPlayer(self.chunk)
        self.player.signal.connect(lambda m_no, e_no: self.mark_at(m_no, e_no))

    def draw_content(self):
        painter = QPainter(self)
        painter.setFont(self.bravura_font)
        painter.setPen(self.dark_gray)
        painter.setBrush(self.black)
        pen = QPen(self.very_light_gray)
        painter.setPen(pen)
        self.draw_frame(painter)
        pen = QPen(QColor(255, 255, 255, 80))
        painter.setPen(pen)
        bar_segments = self.get_h_segments()
        self.visual_notes = []

        for m_no, ruler_bar in enumerate(self.ruler_bars):
            seg_start = bar_segments[m_no][0]
            seg_end = bar_segments[m_no][1]
            if seg_end - seg_start < 10:
                continue
            curr_x = 0
            for r_e in ruler_bar.events:
                curr_x = r_e.offset_ratio.to_float() * (seg_end - seg_start) + seg_start
                self.draw_bar_frame(painter, int(curr_x), int(curr_x) + 1)

        pen.setWidth(3)
        painter.setPen(pen)
        painter.setPen(self.light_gray)
        painter.setBrush(self.light_gray)
        self.draw_marked(painter)
        painter.end()


    def draw_frame(self, painter: QPainter):
        w = self.width()
        h = self.height()
        rect = QRect(0, 0, w-1, h-1)
        painter.drawRect(rect)

    def draw_bar_frame(self, painter: QPainter, x0, x1):
        w = self.width()
        h = self.height() - 5
        rect = QRect(x0, 2, x1 - x0, h-3)
        painter.drawRect(rect)

    def draw_marked(self, painter: QPainter):
        e = self.ruler_bars[self.m_no].events[self.e_no]
        seg = self.get_h_segments()[self.m_no]
        seg_start = seg[0]
        seg_end = seg[1]
        curr_x = e.offset_ratio.to_float() * (seg_end - seg_start) + seg_start
        self.draw_bar_frame(painter, int(curr_x)-5, int(curr_x) + 5)

