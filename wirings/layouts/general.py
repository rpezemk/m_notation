
from PyQt5.QtWidgets import QLabel

from wirings.test_methods import quit_csound, save_file, start_CSOUND, play_ding, static_play_file
from widgets.basics.my_button import AsyncButton
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
