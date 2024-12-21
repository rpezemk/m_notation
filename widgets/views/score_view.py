from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFrame, QWidget

from model.piece import generate_sample_piece
from widgets.basics.my_button import StateButton, SyncButton
from widgets.compound.stretch import Stretch
from widgets.lanes.StaffWidget import StaffWidget
from widgets.compound.stack_panels import HStack, VStack
from widgets.musical.PartWidget import PartWidget
from widgets.lanes.ConductorWidget import RulerWidget

class ScoreView(VStack):
    def __init__(self, margin = None, spacing = None, children = None, stretch=False, fixed_width=-1):
        super().__init__(margin, spacing, children, stretch, fixed_width)
        piece = generate_sample_piece(4, 8)

        self.back = QWidget(self.widget)
        
        ruler_widget = PartWidget(widget_type=RulerWidget)
        ruler_widget.staff_widget.set_content(piece.parts[0].measures[:4])
        self.layout.addWidget(ruler_widget)

        for part in piece.parts:
            part_widget = PartWidget(widget_type=StaffWidget)
            part_widget.staff_widget.set_content(part.measures[:4])
            part_widget.staff_widget.update()
            self.layout.addWidget(part_widget)

        self.layout.addStretch()

        ruler_widget = PartWidget(widget_type=RulerWidget)
        self.layout.addWidget(ruler_widget)

        bottom_panel = HStack(
                    children=
                    [
                        Stretch(),
                        SyncButton("<<", None), 
                        SyncButton("<", None), 
                        StateButton("PLAY", None, color_hex_off="#334477", color_hex_on="#4477FF"),
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
        self.timer.timeout.connect(self.update_counter)  # Call update_counter every interval
        self.timer.start(100)  # Interval set to 1000ms (1 second)
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