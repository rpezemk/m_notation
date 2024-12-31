from typing import override
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QMainWindow

from utils.commands.kbd_resolver import KbdResolver

from utils.osc_udp.heartbeat_checker import HeartbeatChecker
from utils.osc_udp.m_osc_server import MOscServer
from widgets.basics.indicator_button import IndicatorButton
from wirings.csd_instr_numbers import cs_to_py_port, local_ip
from wirings.test_methods import quit_csound
from widgets.styles import style
from wirings.cmd_wirings import root_kbd_resolver

class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("m_notator")
        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet(style)        
        self.mosc_server = MOscServer(local_ip, cs_to_py_port,
                                       [("/heartbeat", lambda addr, args: self.heartbeat_checker.handle_flag(args))]
                                      ).start_async()
        self.indicator = IndicatorButton("<>", ..., )
        self.heartbeat_checker = HeartbeatChecker(0.5).bind_to(self.indicator).start()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.root_kbd_resolver: KbdResolver = root_kbd_resolver
        
    @override
    def resizeEvent(self, event):
        self.root_kbd_resolver.clear_curr_input()
        size = event.size()
        self.setWindowTitle(f"m_notator")
        super().resizeEvent(event)

    @override
    def closeEvent(self, event):
        self.heartbeat_checker.stop()
        self.mosc_server.very_gently_close()
        quit_csound()
        return super().closeEvent(event)

    @override
    def keyPressEvent(self, event: QKeyEvent):
        self.root_kbd_resolver.accept_press(self, event)

    @override
    def keyReleaseEvent(self, event: QKeyEvent):
        self.root_kbd_resolver.accept_release(self, event)