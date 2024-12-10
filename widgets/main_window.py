
from typing import Callable
from PyQt5.QtWidgets import QComboBox, QLabel, QFrame, QWidget
from PyQt5.QtCore import Qt, QRect, QTimer

from model.piece import Piece, generate_sample_piece
from widgets.base_window import MyStyledWindow
from widgets.compound.base_compound import MyCompound
from wirings.test_methods import quit_csound, save_file, start_CSOUND, play_ding, play_file
from utils.logger import MLogger
from widgets.compound.stack_panels import HStack, VStack
from widgets.compound.stretch import Stretch
from widgets.my_button import AsyncButton, SyncButton
from widgets.note_widget import AudioWidget, PartWidget, StaffWidget, ConductorWidget
from widgets.text_box import TextBox
import widgets.widget_utils as w_utils
from widgets.comboBox import ComboBox
from widgets.label import Label
from utils.audio_utils import list_audio_devices
import wirings.layouts.general as general


class ScoreView(VStack):
    def __init__(self, margin = None, spacing = None, children = None, black_on_white=False, stretch=False, fixed_width=-1):
        super().__init__(margin, spacing, children, black_on_white, stretch, fixed_width)
        piece = generate_sample_piece(4, 8)
        
        # self.back = QWidget(self.widget)
        
        for part in piece.parts:
            part_widget = PartWidget(widget_type=StaffWidget)
            part_widget.staff_widget.set_content(part.measures[:4])
            part_widget.staff_widget.update()
            self.layout.addWidget(part_widget)
                
        self.layout.addStretch()
        self.layout.parentWidget().update()
        self.layout.update()
        self.delta = 2
        # self.line_x0 = 100
        # self.line_pos = self.line_x0
        # self.timer = QTimer(self.widget)
        # self.timer.timeout.connect(self.update_counter)  # Call update_counter every interval
        # self.timer.start(100)  # Interval set to 1000ms (1 second)
        # self.line = QFrame(self.back)
        # self.widget.resizeEvent = self.resizeEvent
        # self.draw_line(0)

    # def draw_line(self, x0):
    #     h = self.widget.height()
    #     self.line.setFrameShape(QFrame.HLine)  # Horizontal line
    #     self.line.setGeometry(QRect(x0, 0, 1, h))  # Set position and size
    #     self.line.setStyleSheet("background-color: gray;")
        
    # def update_counter(self):
    #     w = self.widget.width()
    #     self.line_pos = (self.line_pos + self.delta) % (w - self.line_x0)
    #     self.draw_line(self.line_pos + self.line_x0)
    
    # def resizeEvent(self, event):
    #     h = self.widget.height()
    #     w = self.widget.width()
    #     if w - 100 > 0:
    #         self.back.setGeometry(0, 0, w, h)
        
        
class DawView(VStack):
    def __init__(self, margin = None, spacing = None, children = None, black_on_white=False, stretch=False, fixed_width=-1):
        super().__init__(margin, spacing, children, black_on_white, stretch, fixed_width)
        
        for track_no in range(0, 5):
            part_widget = PartWidget(widget_type=AudioWidget)
            part_widget.staff_widget.set_content(None)
            part_widget.staff_widget.update()
            self.layout.addWidget(part_widget)

        self.layout.addStretch()
        self.layout.parentWidget().update()
        self.layout.update()
      

def get_buttons(defs: list[tuple[str, Callable]]):
    res = []
    for d in defs:
        b = AsyncButton(d[0])    
        b.setFixedWidth(100)
        res.append(b)
        
    return res
            
class MainWindow(MyStyledWindow):
    def __init__(self):
        super().__init__()

        
        self.score_view = ScoreView()
        self.daw_view = DawView()
        
        self.set_central(self.score_view)
    
    def set_central(self, compound: MyCompound):

        
        status_panel = HStack(
            children=[SyncButton("load piece", self.load_piece), SyncButton("load DAW", self.load_daw)], 
            stretch=True)
        
        top_tools = [SyncButton("load piece", self.load_piece), SyncButton("load DAW", self.load_daw)]
        horizontal_toolbar = HStack(spacing=0, children=top_tools)
        central_v_stack = VStack(
                children=[
                    horizontal_toolbar, 
                    HStack(
                        children=[
                            VStack(fixed_width=120, 
                                   children=general.get_left_pane_buttons(), 
                                   stretch=True), 
                            compound],
                        spacing=0),
                    SyncButton("load piece", self.load_piece),
                    status_panel, 
                    ]
                )
        
        self.setCentralWidget(central_v_stack.widget)

    def load_piece(self):
        self.daw_view.widget.setParent(None)
        self.set_central(ScoreView())
            
    def load_daw(self):
        self.score_view.widget.setParent(None)
        self.set_central(DawView())
        

            

    
