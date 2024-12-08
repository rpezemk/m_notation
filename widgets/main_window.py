
from PyQt5.QtWidgets import QComboBox, QLabel
from PyQt5.QtCore import Qt

from model.piece import Piece, generate_sample_piece
from widgets.base_window import MyStyledWindow
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


    
class MainWindow(MyStyledWindow):
    def __init__(self):
        super().__init__()
        global Log
        Log = MLogger(lambda msg: self.status_bar.append_log(msg))
        self.part_widgets = []
        self.status_bar = TextBox(read_only=True, set_fixed_height=200)    
        
        scores_stack = VStack(stretch=True)
        top_tools = [SyncButton("load piece", self.load_piece_click), SyncButton("load DAW", self.load_daw)]
        horizontal_toolbar = HStack((0, 0, 0, 0), spacing=0, children=top_tools, stretch=True)
        central_v_stack = VStack(
                children=[
                    horizontal_toolbar, 
                    HStack(
                        children=[
                            VStack(fixed_width=120, 
                                   children=general.get_left_pane_buttons(), 
                                   stretch=True), 
                            scores_stack],
                        spacing=0, 
                        margin=(0, 0, 0, 0)),
                    Stretch(),
                    self.status_bar]
                )
        
        self.setCentralWidget(central_v_stack.widget)

        self.stack_panel = scores_stack.layout

    def load_piece_click(self):
        piece = generate_sample_piece(4, 8)
        self.load_piece(piece)
            
    def load_daw(self):
        w_utils.clear_layout(self.stack_panel)
        self.part_widgets.clear()
        
        part_widget = PartWidget(widget_type=ConductorWidget)
        part_widget.staff_widget.set_content(None)
        part_widget.staff_widget.update()
        self.stack_panel.addWidget(part_widget)
        self.part_widgets.append(part_widget)
        
        for track_no in range(0, 5):
            part_widget = PartWidget(widget_type=AudioWidget)
            part_widget.staff_widget.set_content(None)
            part_widget.staff_widget.update()
            self.stack_panel.addWidget(part_widget)
            self.part_widgets.append(part_widget)
                
        self.stack_panel.addStretch()
        self.stack_panel.parentWidget().update()
        self.stack_panel.update()
        
    def load_piece(self, piece: Piece):
        w_utils.clear_layout(self.stack_panel)
        self.part_widgets.clear()
        
        for part in piece.parts:
            part_widget = PartWidget(widget_type=StaffWidget)
            part_widget.staff_widget.set_content(part.measures[:4])
            part_widget.staff_widget.update()
            self.stack_panel.addWidget(part_widget)
            self.part_widgets.append(part_widget)
                
        self.stack_panel.addStretch()
        self.stack_panel.parentWidget().update()
        self.stack_panel.update()
                

            

    
