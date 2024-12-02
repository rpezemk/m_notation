import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt

from model.piece import Piece
import model.piece
from widgets.compound.stack_panels import HStack, VStack
from widgets.compound.stretch import Stretch
from widgets.my_button import AsyncBlockingButton, GuiButton
from widgets.note_widget import PartWidget
from widgets.text_box import TextBox, Label
import widgets.widget_utils as w_utils
from csound_tests.test_methods import quit_csound, run_example_start_CSOUND
from utils.logger import Log, MLogger
from utils.commands.kbd_resolver import KbdResolver    
    


class MyStyledWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stacked Panels")
        self.setStyleSheet("background-color: black;")

        
class MainWindow(MyStyledWindow):
    def __init__(self):
        super().__init__()
        self.kbd_resolver = KbdResolver()
        
        global Log
        Log = MLogger(lambda msg: self.status_bar.append_log(msg))
        self.part_widgets = []
        self.status_bar = TextBox(read_only=True)
        self.status_bar.setFixedHeight(80)
        self.status_bar.setStyleSheet("color: white;")
        left_pane_buttons = [
                AsyncBlockingButton("CSOUND START", run_example_start_CSOUND), 
                AsyncBlockingButton("CSOUND STOP", quit_csound)
                ]
        
        scores_stack = VStack(stretch=True)
        central_v_stack = VStack(
                children=[
                    GuiButton("top button", self.button_click), 
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
    
    def button_click(self):
        piece = model.piece.generate_sample_piece(4, 8)
        self.load_piece(piece)
        
    def resizeEvent(self, event):
        size = event.size()  
        self.setWindowTitle(f"Window resized to: {size.width()} x {size.height()}")
        super().resizeEvent(event)  
    
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
        
    def csound_start(self):
        t1 = threading.Thread(target=run_example_start_CSOUND, args=[])
        t1.start()
    
    def keyPressEvent(self, event: QKeyEvent):
        res, keys = self.kbd_resolver.try_resolve_new_kbd_press(event)
        self.report_kbd(res, keys, "press:")

        
    def keyReleaseEvent(self, event: QKeyEvent):
        res, keys = self.kbd_resolver.try_resolve_new_kbd_release(event)
        self.report_kbd(res, keys, "rel:  ")
    
    def report_kbd(self, res, keys, op_name):
        ms = [str(k) for k in keys]
        msg =  op_name + ", ".join(ms) 
        if res:
            Log.log(msg)
        