from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QFont

from model.piece import Piece
import model.piece
from widgets.note_widget import PartWidget
import widgets.widget_utils as w_utils



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.part_widgets = []
        self.setWindowTitle("Stacked Panels")
        self.setStyleSheet("background-color: black;")
        
        all_widget = QWidget()
        all_layout = QVBoxLayout(all_widget)
        top_button = QPushButton("top button")
        top_button.setStyleSheet("color: white;")
        font = QFont("Courier New") 
        font.setStyleHint(QFont.Monospace)  
        top_button.setFont(font)
        top_button.clicked.connect(self.button_click)
        top_button.setFixedHeight(30)
        
        pane_and_scores_widget = QWidget()
        pane_and_scores_widget.setStyleSheet("background-color: black;")
        
        pane_and_scores_layout =  QHBoxLayout(pane_and_scores_widget)
        pane_and_scores_layout.setSpacing(0)
        pane_and_scores_layout.setContentsMargins(0, 0, 0, 0)

        left_pane_widget = QWidget()
        left_pane_widget.setFixedWidth(120)  
        
        scores_widget = QWidget()
        self.part_layouts = QVBoxLayout(scores_widget)
        self.part_layouts.addStretch()
                    
        pane_and_scores_layout.addWidget(left_pane_widget)
        pane_and_scores_layout.addWidget(scores_widget)
        
        all_layout.addWidget(top_button)
        all_layout.addWidget(pane_and_scores_widget)        
        self.setCentralWidget(all_widget)
    
    def button_click(self):
        piece = model.piece.generate_sample_piece(4, 8)
        self.load_piece(piece)
        
    def resizeEvent(self, event):
        size = event.size()  
        self.setWindowTitle(f"Window resized to: {size.width()} x {size.height()}")
        super().resizeEvent(event)  
    
    def load_piece(self, piece: Piece):
        w_utils.clear_layout(self.part_layouts)
        self.part_widgets.clear()
        
        for part in piece.parts:
            part_widget = PartWidget()
            part_widget.setFixedHeight(120)  
            self.part_layouts.addWidget(part_widget)
            self.part_widgets.append(part_widget)
            part_widget.staff_widget.set_bars(part.measures[:4])
            part_widget.staff_widget.update()
                
        self.part_layouts.addStretch()
        self.part_layouts.parentWidget().update()
        self.part_layouts.update()
        
