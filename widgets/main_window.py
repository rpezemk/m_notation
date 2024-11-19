from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from model.piece import Piece
import model.piece
from widgets.note_widget import PartWidget

import widgets.widget_utils as w_utils



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stacked Panels")
        self.part_widgets = []
        self.setStyleSheet("background-color: black;")
        
        all_widget = QWidget()
        all_layout = QVBoxLayout(all_widget)
        
        top_button = QPushButton("top button")
        top_button.clicked.connect(self.button_click)
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
        self.part_layouts = QVBoxLayout(scores_widget)
                    
        self.part_layouts.addStretch()
        
        pane_and_scores_layout.addWidget(left_pane_widget)
        pane_and_scores_layout.addWidget(scores_widget)
        
        all_layout.addWidget(pane_and_scores_widget)        
        self.setCentralWidget(all_widget)
    
    def button_click(self):
        piece = model.piece.generate_sample_piece(4, 8)
        self.load_piece(piece)
        
    def resizeEvent(self, event):
        new_size = event.size()  
        self.setWindowTitle(f"Window resized to: {new_size.width()} x {new_size.height()}")
        super().resizeEvent(event)  
        self.show()
    
    def load_piece(self, piece: Piece):
        w_utils.clear_layout(self.part_layouts)
        self.part_widgets.clear()
        
        for part in piece.children:
            part_widget = PartWidget()
            part_widget.setFixedHeight(120)  
            self.part_layouts.addWidget(part_widget)
            self.part_widgets.append(part_widget)
            # part_widget.staff_widget.load_part(part)
            part_widget.staff_widget.set_bars(part.children[:4])
            part_widget.staff_widget.update()
                
        self.part_layouts.addStretch()
        self.part_layouts.parentWidget().update()
        self.part_layouts.update()
        
        # self.show()
        # for widget in self.note_widgets:
        #    widget.draw()
        # self.repaint()
        # super().show()
    
