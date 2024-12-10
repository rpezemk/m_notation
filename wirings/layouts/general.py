
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


def get_left_pane_buttons():
    devices = list_audio_devices()   
    devcs_combo = ComboBox(devices, lambda s: print(s), dict_to_str_func=lambda d: d["name"])
    rates_combo = ComboBox(["44100", "48000", "96000"], lambda s: print(s))


    left_pane_buttons = [
        AsyncButton("CSOUND START", start_CSOUND), 
        AsyncButton("beep", play_ding), 
        AsyncButton("play file", play_file),
        AsyncButton("CSOUND STOP", quit_csound), 
        AsyncButton("GENERATE CSD", save_file),
        Label("devices"),
        devcs_combo,
        Label("rates"),
        rates_combo
        ]
    
    return left_pane_buttons

def get_left_pane_buttons2():
    devices = list_audio_devices()   
    devcs_combo = ComboBox(devices, lambda s: print(s), dict_to_str_func=lambda d: d["name"])
    rates_combo = ComboBox(["44100", "48000", "96000"], lambda s: print(s))


    left_pane_buttons = [
        AsyncButton("CSOUND START", start_CSOUND), 
        AsyncButton("beep", play_ding), 
        AsyncButton("play file", play_file),
        AsyncButton("CSOUND STOP", quit_csound), 
        AsyncButton("GENERATE CSD", save_file),
        Label("devices"),
        devcs_combo,
        Label("rates"),
        rates_combo
        ]
    
    return left_pane_buttons

