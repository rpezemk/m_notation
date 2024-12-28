from typing import override
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QMainWindow

from utils.commands.kbd_resolver import KbdResolver
from utils.logger import MLogger
from utils.osc_udp.heartbeat_checker import HeartbeatChecker
from utils.osc_udp.m_osc_server import MOscServer
from widgets.basics.indicator_button import IndicatorButton
from wirings.cmd_wiring import my_wirings
from wirings.csd_instr_numbers import cs_to_py_port, local_ip
from wirings.test_methods import quit_csound
from widgets.styles import style



class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("m_notator")
        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet(style)
        Log = MLogger(print)
        self.kbd_resolver = KbdResolver(my_wirings, lambda s: Log.log(s))
        self.mosc_server = MOscServer(local_ip, cs_to_py_port,
                                       [("/heartbeat", lambda addr, args: self.heartbeat_checker.handle_flag(args))]
                                      ).start_async()
        self.indicator = IndicatorButton("<>", ..., )
        self.heartbeat_checker = HeartbeatChecker(0.5).bind_to(self.indicator).start()
        self.setWindowFlags(Qt.FramelessWindowHint)
        
    @override
    def resizeEvent(self, event):
        self.kbd_resolver.clear()
        size = event.size()
        self.setWindowTitle(f"Window resized to: {size.width()} x {size.height()}")
        super().resizeEvent(event)

    @override
    def closeEvent(self, event):
        self.heartbeat_checker.stop()
        self.mosc_server.very_gently_close()
        quit_csound()
        return super().closeEvent(event)

    @override
    def keyPressEvent(self, event: QKeyEvent):
        self.kbd_resolver.accept_press(event.key(), event.isAutoRepeat())

    @override
    def keyReleaseEvent(self, event: QKeyEvent):
        self.kbd_resolver.accept_release(event.key(), event.isAutoRepeat())