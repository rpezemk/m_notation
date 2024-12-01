import threading
from PyQt5.QtWidgets import QMainWindow


from model.piece import Piece
import model.piece
from widgets.compound.stack_panels import HStack, VStack
from widgets.my_button import AsyncBlockingButton
from widgets.note_widget import PartWidget
import widgets.widget_utils as w_utils
from csound_tweaking.examples.csound_py_test import run_example

class MyStyledWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stacked Panels")
        self.setStyleSheet("background-color: black;")

class MainWindow(MyStyledWindow):
    def __init__(self):
        super().__init__()
        self.part_widgets = []
        
        left_pane_buttons = [
                MyButton("CSOUND_TEST", self.button_click), 
                MyButton("top button", self.button_click)
            ]
        
        scores_stack = VStack(stretch=True)
        self.setCentralWidget(
            VStack(
                children=[
                    AsyncBlockingButton("top button", self.button_click), 
                    HStack(
                        children=[
                            VStack(fixed_width=120, 
                                   children=left_pane_buttons, 
                                   stretch=True), 
                            scores_stack],
                        spacing=0, 
                        margin=(0, 0, 0, 0))]
                ).widget)
        # sdf
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
        
    def csound_test(self):
        t1 = threading.Thread(target=run_example, args=[])
        t1.start()