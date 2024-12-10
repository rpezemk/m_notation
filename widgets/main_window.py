
from typing import Callable
from PyQt5.QtWidgets import QComboBox, QLabel, QFrame, QWidget
from PyQt5.QtCore import Qt, QRect, QTimer

from model.piece import Piece
from widgets.views.daw_view import DawView
from widgets.views.score_view import ScoreView
from widgets.base_window import MyStyledWindow
from widgets.compound.base_compound import MyCompound
from wirings.test_methods import quit_csound, save_file, start_CSOUND, play_ding, play_file
from utils.logger import MLogger
from widgets.compound.stack_panels import HStack, VStack
from widgets.compound.stretch import Stretch
from widgets.my_button import AsyncButton, SyncButton
from widgets.note_widget import ConductorWidget
from widgets.text_box import TextBox
import widgets.widget_utils as w_utils
from widgets.comboBox import ComboBox
from widgets.label import Label
from utils.audio_utils import list_audio_devices
import wirings.layouts.general as general

     
class MainWindow(MyStyledWindow):
    def __init__(self):
        super().__init__()
        self.set_central(ScoreView())
    
    def set_central(self, compound: MyCompound):

        central_v_stack = VStack(
            children=[
                HStack(children=[SyncButton("load piece", self.load_piece), SyncButton("load DAW", self.load_daw)]), 
                HStack(
                    children=[
                        VStack(fixed_width=120, 
                                children=general.get_left_pane_buttons(), stretch=True), 
                        compound], stretch=False),
                HStack(children=[SyncButton("PLAY", None), SyncButton("STOP", None)]),
                ],
            stretch=False
        )

        self.setCentralWidget(central_v_stack.widget)

    def load_piece(self):
        self.set_central(ScoreView())
            
    def load_daw(self):
        self.set_central(DawView())
        

            

    
