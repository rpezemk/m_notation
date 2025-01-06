
from PyQt5.QtWidgets import QComboBox, QLabel
from PyQt5.QtCore import Qt

from model.sample_piece_gen import generate_sample_piece
from widgets.lanes.AudioWidget import AudioWidget
from widgets.lanes.RulerWidget import RulerWidget
from widgets.lanes.StaffWidget import VirtualStaff
from wirings.test_methods import quit_csound, save_file, start_CSOUND, play_ding, static_play_file
from utils.logger import MLogger
from widgets.compound.stack_panels import HStack, VStack
from widgets.compound.stretch import Stretch
from widgets.basics.my_button import AsyncButton, SyncButton
from widgets.lanes.PartWidget import PartWidget
from widgets.basics.text_box import TextBox
import utils.widget_utils as w_utils
from widgets.basics.comboBox import ComboBox
from utils.audio.audio_utils import list_audio_devices


def get_left_pane_buttons():
    devices = list_audio_devices()
    devcs_combo = ComboBox(devices, lambda s: print(s), dict_to_str_func=lambda d: d["name"])
    rates_combo = ComboBox(["44100", "48000", "96000"], lambda s: print(s))


    left_pane_buttons = [
        AsyncButton("CSOUND START", start_CSOUND),
        AsyncButton("beep", play_ding),
        AsyncButton("play file", static_play_file),
        AsyncButton("CSOUND STOP", quit_csound),
        AsyncButton("GENERATE CSD", save_file),
        QLabel("devices"),
        devcs_combo,
        QLabel("rates"),
        rates_combo
        ]

    return left_pane_buttons
