from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from widgets.note_widget import PartWidget

import widgets.widget_utils as w_utils

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stacked Panels")
        _, self.stack_layout = w_utils.emit_central_pair(self, QVBoxLayout)
        self.note_widgets = []

    def add_child_to_stack(self, widget: QWidget = None):
        if widget is None:
            return
        widget.setFixedHeight(120)  
        self.stack_layout.addWidget(widget)
        self.note_widgets.append(widget)
        
    def resizeEvent(self, event):
        new_size = event.size()  
        self.setWindowTitle(f"Window resized to: {new_size.width()} x {new_size.height()}")
        super().resizeEvent(event)  
        self.show()

    def show(self):
        super().show()
        for widget in self.note_widgets:
            widget.draw()