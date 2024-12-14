from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFrame, QWidget

from model.piece import generate_sample_piece
from widgets.compound.stack_panels import VStack
from widgets.note_widget import PartWidget, StaffWidget

class ScoreView(VStack):
    def __init__(self, margin = None, spacing = None, children = None, stretch=False, fixed_width=-1):
        super().__init__(margin, spacing, children, stretch, fixed_width)
        piece = generate_sample_piece(4, 8)

        self.back = QWidget(self.widget)

        for part in piece.parts:
            part_widget = PartWidget(widget_type=StaffWidget)
            part_widget.staff_widget.set_content(part.measures[:4])
            part_widget.staff_widget.update()
            self.layout.addWidget(part_widget)

        self.layout.addStretch()
        self.layout.parentWidget().update()
        self.layout.update()
        self.delta = 1
        self.line_x0 = 100
        self.line_pos = self.line_x0
        self.timer = QTimer(self.widget)
        self.timer.timeout.connect(self.update_counter)  # Call update_counter every interval
        self.timer.start(2)  # Interval set to 1000ms (1 second)
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