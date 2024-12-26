from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFrame, QWidget

from model.sample_piece_gen import generate_sample_piece
from widgets.chunk_player import RulerPlayer
from widgets.basics.my_button import StateButton, SyncButton
from widgets.compound.stretch import Stretch
from widgets.lanes.StaffWidget import StaffWidget
from widgets.compound.stack_panels import HStack, VStack
from widgets.lanes.PartWidget import PartWidget
from widgets.lanes.RulerWidget import RulerWidget


class ScoreView(VStack):
    def __init__(self, margin = None, spacing = None, children = None, stretch=False, fixed_width=-1):
        super().__init__(margin, spacing, children, stretch, fixed_width)
        self.back = QWidget(self.widget)
        
        self.piece = generate_sample_piece(4, 8)
        self.chunk = self.piece.to_chunk(0, 4)
        
        ruler_widget = PartWidget(widget_type=RulerWidget)
        ruler_widget.staff_widget.set_content(self.chunk)
        self.layout.addWidget(ruler_widget)
        
        self.player = RulerPlayer(self.chunk)
        self.player.signal.connect(lambda m_no, e_no: ruler_widget.staff_widget.mark_at(m_no, e_no))
                        
        for h_chunk in self.chunk.h_chunks:
            part_widget = PartWidget(widget_type=StaffWidget)
            part_widget.staff_widget.set_content(h_chunk.measures)
            part_widget.staff_widget.update()
            self.layout.addWidget(part_widget)

        self.layout.addStretch()


        bottom_panel = HStack(
                    children=
                    [
                        Stretch(),
                        SyncButton("<<", None), 
                        SyncButton("<", None), 
                        StateButton("PLAY", self.player.start, color_hex_off="#334477", color_hex_on="#4477FF"),
                        SyncButton("STOP", None),
                        SyncButton(">", None),
                        SyncButton(">>", None),
                    ],
                    stretch=False)
        self.layout.addWidget(bottom_panel.widget)
        
        self.layout.parentWidget().update()
        self.layout.update()
        self.delta = 1
        self.line_x0 = 100
        self.line_pos = self.line_x0
        self.timer = QTimer(self.widget)
        self.timer.timeout.connect(self.update_counter) 
        self.timer.start(100) 
        self.line = QFrame(self.back)
        self.widget.resizeEvent = self.resizeEvent
        
    def update_counter(self):
        w = self.widget.width()
        if w - self.line_x0 <= 0:
            return
        self.line_pos = (self.line_pos + self.delta) % (w - self.line_x0)
        self.draw_line(self.line_pos + self.line_x0)
        
    def draw_line(self, x0):
        h = self.widget.height()
        self.line.setFrameShape(QFrame.HLine)  # Horizontal line
        self.line.setGeometry(x0, 0, 1, h)  # Set position and size
        
    def resizeEvent(self, event):
        h = self.widget.height()
        w = self.widget.width()
        if w - 100 > 0:
            self.back.setGeometry(0, 0, w, h)