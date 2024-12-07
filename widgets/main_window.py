from typing import override

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt

from model.piece import Piece, generate_sample_piece
from instr_logic.test_methods import quit_csound, save_file, start_CSOUND, play_ding
from instr_logic.csd_instr_numbers import cs_to_py_port, local_ip
from utils.logger import Log, MLogger
from utils.osc_udp.heartbeat_checker import HeartbeatChecker
from utils.osc_udp.m_osc_server import MOscServer
from utils.commands.kbd_resolver import KbdResolver    
from widgets.compound.stack_panels import HStack, VStack
from widgets.compound.stretch import Stretch
from widgets.my_button import AsyncButton, SyncButton, IndicatorButton
from widgets.note_widget import PartWidget
from widgets.text_box import TextBox
import widgets.widget_utils as w_utils
from wirings.cmd_wiring import my_wirings

class MyStyledWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stacked Panels")
        self.setStyleSheet("background-color: black;")
        
    @override
    def closeEvent(self, event):
            quit_csound()
            
class MainWindow(MyStyledWindow):
    def __init__(self):
        super().__init__()
        global Log
        Log = MLogger(lambda msg: self.status_bar.append_log(msg))
        self.part_widgets = []
        self.status_bar = TextBox(read_only=True, set_fixed_height=200)    
        self.indicator = IndicatorButton("<>", ..., )
        
        left_pane_buttons = [AsyncButton("CSOUND START", start_CSOUND), AsyncButton("beep", play_ding), 
                             AsyncButton("CSOUND STOP", quit_csound), AsyncButton("GENERATE CSD", save_file),
                             self.indicator]
        
        scores_stack = VStack(stretch=True)
        
        central_v_stack = VStack(
                children=[
                    SyncButton("top button", self.button_click), 
                    HStack(
                        children=[
                            VStack(fixed_width=120, 
                                   children=left_pane_buttons, 
                                   stretch=True), 
                            scores_stack],
                        spacing=0, 
                        margin=(0, 0, 0, 0)),
                    Stretch(),
                    self.status_bar]
                )
        
        self.setCentralWidget(central_v_stack.widget)

        self.stack_panel = scores_stack.layout
        self.wire_up()
        
    def wire_up(self):
        self.mosc_server = MOscServer(local_ip, cs_to_py_port, 
                                       [("/heartbeat", lambda addr, args: self.heartbeat_checker.handle_flag(args))]
                                      ).start_async()
        self.heartbeat_checker = HeartbeatChecker(0.5).bind_to(self.indicator).start()
        self.kbd_resolver = KbdResolver(my_wirings, lambda s: Log.log(s))

    def button_click(self):
        piece = generate_sample_piece(4, 8)
        self.load_piece(piece)
        
    def load_piece(self, piece: Piece):
        w_utils.clear_layout(self.stack_panel)
        self.part_widgets.clear()
        
        for part in piece.parts:
            part_widget = PartWidget()
            part_widget.setFixedHeight(120)  
            self.stack_panel.addWidget(part_widget)
            self.part_widgets.append(part_widget)
            part_widget.staff_widget.set_bars(part.measures[:4])
            part_widget.staff_widget.update()
                
        self.stack_panel.addStretch()
        self.stack_panel.parentWidget().update()
        self.stack_panel.update()
  
    @override
    def resizeEvent(self, event):
        self.kbd_resolver.clear()
        size = event.size()  
        self.setWindowTitle(f"Window resized to: {size.width()} x {size.height()}")
        super().resizeEvent(event)  
            
    @override
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            print("Space key pressed!")
        self.kbd_resolver.accept_press(event.key(), event.isAutoRepeat())

    @override
    def keyReleaseEvent(self, event: QKeyEvent):
        self.kbd_resolver.accept_release(event.key(), event.isAutoRepeat())
    
    @override
    def closeEvent(self, event):
        self.heartbeat_checker.stop()
        self.mosc_server.very_gently_close()
        return super().closeEvent(event)