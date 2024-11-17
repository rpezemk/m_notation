from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from widgets.note_widget import PartWidget

import widgets.widget_utils as w_utils



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stacked Panels")
        self.note_widgets = []
        
        
        all_widget = QWidget()
        all_layout = QVBoxLayout(all_widget)
        
        top_button = QPushButton("top button")
        top_button.setFixedHeight(30)
        all_layout.addWidget(top_button)
        
        pane_and_scores_widget = QWidget()
        pane_and_scores_widget.setStyleSheet("background-color: black;")
        pane_and_scores_layout =  QHBoxLayout(pane_and_scores_widget)
        pane_and_scores_layout.setSpacing(0)
        pane_and_scores_layout.setContentsMargins(0, 0, 0, 0)

        left_pane_widget = QWidget()
        left_pane_widget.setFixedWidth(120)  
        
        scores_widget = QWidget()
        scores_layout = QVBoxLayout(scores_widget)
        
        for i in range(0, 5):
            note_widget = PartWidget()
            note_widget.setFixedHeight(120)  
            scores_layout.addWidget(note_widget)
            self.note_widgets.append(note_widget)
            
        scores_layout.addStretch()
        
        pane_and_scores_layout.addWidget(left_pane_widget)
        pane_and_scores_layout.addWidget(scores_widget)
        
        all_layout.addWidget(pane_and_scores_widget)        
        self.setCentralWidget(all_widget)
    
    def resizeEvent(self, event):
        new_size = event.size()  
        self.setWindowTitle(f"Window resized to: {new_size.width()} x {new_size.height()}")
        super().resizeEvent(event)  
        self.show()

    def show(self):
        super().show()
        for widget in self.note_widgets:
           widget.draw()