from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QKeyEvent


from model.piece import Piece
import model.piece
from widgets.compound.stack_panels import HStack, VStack
from widgets.compound.stretch import Stretch
from widgets.my_button import AsyncBlockingButton, GuiButton
from widgets.note_widget import PartWidget
from widgets.text_box import TextBox, Label
import widgets.widget_utils as w_utils
from instr_logic.test_methods import quit_csound, save_file, start_CSOUND, beep
from utils.logger import Log, MLogger
from utils.commands.kbd_resolver import KbdResolver    
from widgets.cmd_wiring import my_wirings

class MyStyledWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stacked Panels")
        self.setStyleSheet("background-color: black;")
        
    def closeEvent(self, event):
            quit_csound()
            
class MainWindow(MyStyledWindow):
    def __init__(self):
        super().__init__()
        global Log
        
        self.part_widgets = []
        self.status_bar = TextBox(read_only=True)
        self.status_bar.setFixedHeight(200)
        self.status_bar.setStyleSheet("color: white;")
        Log = MLogger(lambda msg: self.status_bar.append_log(msg))
        self.kbd_resolver = KbdResolver(my_wirings, lambda s: Log.log(s))
        
        left_pane_buttons = [
                AsyncBlockingButton("CSOUND START", start_CSOUND), 
                AsyncBlockingButton("beep", beep), 
                AsyncBlockingButton("CSOUND STOP", quit_csound),
                AsyncBlockingButton("GENERATE CSD", save_file)
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
        self.kbd_resolver.clear()
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
        
            
    def keyPressEvent(self, event: QKeyEvent):
        self.kbd_resolver.accept_press(event.key(), event.isAutoRepeat())

    def keyReleaseEvent(self, event: QKeyEvent):
        self.kbd_resolver.accept_release(event.key(), event.isAutoRepeat())
    