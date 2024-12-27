from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFrame, QWidget

from model.sample_piece_gen import generate_sample_piece
from widgets.chunk_player import RulerPlayer
from widgets.basics.my_button import StateButton, SyncButton
from widgets.compound.stretch import Stretch
from widgets.lanes.StaffWidget import StaffWidget
from widgets.compound.stack_panels import HStack, VStack
from widgets.lanes.PartWidget import PartWidget
from widgets.lanes.RulerWidget import RulerWidget
from widgets.note_widgets.VisualNote import VisualNote


class ScoreView(VStack):
    def __init__(self, margin = None, spacing = None, children = None, stretch=False, fixed_width=-1):
        super().__init__(margin, spacing, children, stretch, fixed_width)
        self.back = QWidget(self.widget)
        
        self.piece = generate_sample_piece(4, 8)
        self.chunk = self.piece.to_chunk(0, 4)
        
        ruler_widget = PartWidget(widget_type=RulerWidget, parent=self)
        ruler_widget.staff_widget.set_content(self.chunk)
        self.layout.addWidget(ruler_widget)
        
        self.player = RulerPlayer(self.chunk)
        self.player.signal.connect(lambda m_no, e_no: ruler_widget.staff_widget.mark_at(m_no, e_no))
           
        self.part_widgets: list[PartWidget] = []                
        for h_chunk in self.chunk.h_chunks:
            part_widget = PartWidget(parent=self, widget_type=StaffWidget)
            part_widget.staff_widget.set_content(h_chunk.measures)
            part_widget.staff_widget.update()
            self.part_widgets.append(part_widget)
            self.layout.addWidget(part_widget)

        self.layout.addStretch()


        bottom_panel = HStack(
                    children=
                    [
                        Stretch(),
                        SyncButton("<<", None), 
                        SyncButton("<", None), 
                        StateButton("PLAY", self.player.start, color_hex_off="#334477", color_hex_on="#4477FF"),
                        SyncButton("STOP", None),
                        SyncButton(">", None),
                        SyncButton(">>", None),
                    ],
                    stretch=False)
        self.layout.addWidget(bottom_panel.widget)
        
        self.layout.parentWidget().update()
        self.layout.update()
        self.delta = 1
        self.widget.resizeEvent = self.resizeEvent
    
    def select_all(self):
        for p in self.part_widgets:
            p.staff_widget.select_all()
            
    def deselect_notes_but(self, v_notes: list[VisualNote]):
        for p in self.part_widgets:
            p.staff_widget.deselect_notes_but(v_notes)
                          
    def resizeEvent(self, event):
        h = self.widget.height()
        w = self.widget.width()
        if w - 100 > 0:
            self.back.setGeometry(0, 0, w, h)