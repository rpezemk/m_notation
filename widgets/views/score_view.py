from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QFrame, QWidget

from model.musical.structure import Chunk
from model.sample_piece_gen import generate_sample_piece
from widgets.basics.my_button import StateButton, SyncButton
from widgets.compound.stretch import Stretch
from widgets.lanes.StaffWidget import StaffWidget
from widgets.compound.stack_panels import HStack, VStack
from widgets.lanes.PartWidget import PartWidget
from widgets.lanes.RulerWidget import RulerWidget
from widgets.note_widgets.VisualNote import VisualNote
from widgets.views.score_view_modes import ScoreViewModeEnum
from widgets.views.view import View

class ScoreView(View):
    def __init__(self, margin = None, spacing = None, children = None, stretch=False, fixed_width=-1):
        super().__init__(margin, spacing, children, stretch, fixed_width)
        self.back = QWidget(self.widget)
        self.widget.setFocusPolicy(Qt.NoFocus)
        self.piece = generate_sample_piece(4, 8)
        self.chunk: Chunk = self.piece.to_chunk(0, 4)
        self.mode = ScoreViewModeEnum.UNDEFINED
        
        self.cursor_pos = (0, 0)
        
        self.ruler_widget = PartWidget(widget_type=RulerWidget, parent=self)
        self.ruler_widget.staff_widget.set_content(self.chunk)
        self.layout.addWidget(self.ruler_widget)
           
        self.part_widgets: list[PartWidget] = []                
        for h_chunk in self.chunk.h_chunks:
            part_widget = PartWidget(parent=self, widget_type=StaffWidget)
            part_widget.staff_widget.set_content(h_chunk)
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
                        StateButton(
                            "PLAY", 
                            state_on_func=self.ruler_widget.staff_widget.start, 
                            state_off_func=self.ruler_widget.staff_widget.stop, 
                            color_hex_off="#334477", 
                            color_hex_on="#4477FF"
                            ),
                        SyncButton("STOP", self.ruler_widget.staff_widget.stop),
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
            
    def set_cursor_at(self, m_no, e_no):
        self.ruler_widget.staff_widget.mark_at(m_no, e_no)
    

    
    """COMMANDS' methods
    """

    def select_next_note(self):
        print("select next note (ScoreView)")
        for pt in self.part_widgets:
            pt.staff_widget.select_next_note()
            
    def select_next_note_in_next_measure(self):
        print("select next note (ScoreView)")
        for pt in self.part_widgets:
            pt.staff_widget.select_next_note_in_next_measure()
            
    def select_prev_note_in_prev_measure(self):
        print("select next note (ScoreView)")
        for pt in self.part_widgets:
            pt.staff_widget.select_prev_note_in_prev_measure()
            
    def select_prev_note(self):
        print("select prev note (ScoreView)")
        for pt in self.part_widgets:
            pt.staff_widget.select_prev_note()
            
    def select_note_above(self):
        maybe = self.order_notes_by_part_no()[:1]
        if not maybe:
            return
        
        src_m = maybe[0].inner.measure
        p_no, m_no = src_m.part_no, src_m.m_no
        if p_no == 0:
            return
        
        piece = maybe[0].inner.measure.part.piece
        
        part = piece.parts[p_no-1]
        inner = maybe[0].inner
        th_to_sel = sorted(part.measures[m_no].time_holders, key=lambda t: abs((t.offset_ratio - inner.offset_ratio).to_float()))[:1]
        if not th_to_sel:
            return
        self.deselect_notes_but([th_to_sel[0]])
        th_to_sel[0].is_selected = True
        self.update()

        
    def select_note_below(self):
        maybe = self.order_notes_by_part_no()[-1:]
        if not maybe:
            return
        
        src_m = maybe[0].inner.measure
        parts = src_m.part.piece.parts
        p_no, m_no = src_m.part_no, src_m.m_no
        if len(parts) -1 == p_no:
            return
        
        part = parts[p_no + 1]
        
        inner = maybe[0].inner
        th_to_sel = [th for th in part.measures[m_no].time_holders][:1]
        th_to_sel = sorted(part.measures[m_no].time_holders, key= lambda t: abs((t.offset_ratio - inner.offset_ratio).to_float()))[:1]
        if not th_to_sel:
            return
        
        self.deselect_notes_but([th_to_sel[0]])
        th_to_sel[0].is_selected = True
        self.update()
        
    def delete_selected_notes(self):
        for pt in self.part_widgets:
            pt.staff_widget.delete_selected_notes()
        
        
    def order_notes_by_part_no(self):
        maybe: list[VisualNote] = [n for pt in self.part_widgets for n in pt.staff_widget.get_last_selected_note()]
        maybe = sorted(maybe, key=lambda x: x.inner.measure.m_no)
        maybe = sorted(maybe, key=lambda x: x.inner.measure.part_no)
        return maybe
    
    