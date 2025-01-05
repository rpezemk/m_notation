from typing import override
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QFrame, QWidget
from PyQt5.QtGui import QPainter

from model.musical.structure import Chunk
from model.sample_piece_gen import generate_sample_piece
from widgets.basics.my_button import StateButton, SyncButton
from widgets.compound.stretch import Stretch
from widgets.lanes.drawable_widget import DrawableWidget

from widgets.lanes.StaffWidget import VirtualStaff
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
        self.piece = generate_sample_piece(7, 11)
        self.max_n_measures = 4
        self.curr_range: tuple[int, int] = (0, self.max_n_measures)
        self.chunk: Chunk = self.piece.to_chunk(self.curr_range[0], self.curr_range[1])
        self.mode = ScoreViewModeEnum.UNDEFINED
                
        self.ruler_widget = RulerWidget(parent=self)
        self.ruler_widget.set_content(self.chunk)
        self.layout.addWidget(self.ruler_widget)
           
        self.part_widgets: list[VirtualStaff] = []
        
        for idx, h_chunk in enumerate(self.chunk.h_chunks):
            part_widget = VirtualStaff(parent=None, y_offset=idx * 130)
            self.part_widgets.append(part_widget)
            # self.layout.addWidget(part_widget)
        
        self.drawable = DrawableWidget(parent=None, redraw_func=self.paint_content, staffs=self.part_widgets)
        self.layout.addWidget(self.drawable)
        self.layout.setStretch(1, 1)
        self.refresh_parts()    
        self.layout.addStretch()
        

        self.play_button = StateButton(
                            "PLAY", 
                            state_on_func=self.ruler_widget.start, 
                            state_off_func=self.ruler_widget.stop, 
                            color_hex_off="#334477", 
                            color_hex_on="#4477FF"
                            )
        
        bottom_panel = HStack(
                    children=
                    [
                        Stretch(),
                        SyncButton("<<", lambda: self.move_by(-self.max_n_measures)), 
                        SyncButton("<", lambda: self.move_by(-1)), 
                        self.play_button,
                        SyncButton("STOP", self.stop),
                        SyncButton(">", lambda: self.move_by(1)),
                        SyncButton(">>",  lambda: self.move_by(self.max_n_measures)),
                    ],
                    stretch=False)
        
        self.layout.addWidget(bottom_panel.widget)
        
        self.layout.parentWidget().update()
        self.layout.update()
        self.delta = 1
        self.widget.resizeEvent = self.resizeEvent
    
    def paintEvent(self, event):
        # self.drawable.update()
        ...
    
    def paint_content(self, width: int, widget):
        for idx, h_chunk in enumerate(self.chunk.h_chunks):
            painter2 = QPainter(widget)
            self.part_widgets[idx].draw_content(painter2, width)
            painter2.end()

    def stop(self):
        self.ruler_widget.stop()
        self.play_button.set_state(False)
        
    def select_all(self):
        for p in self.part_widgets:
            p.select_all()
            
    def deselect_notes_but(self, v_notes: list[VisualNote]):
        for p in self.part_widgets:
            p.deselect_notes_but(v_notes)

    
    def move_by(self, k_msrs):
        next_start_idx = self.curr_range[0] + k_msrs
        next_end_idx = next_start_idx + self.max_n_measures - 1
        
        max_idx = self.piece.n_measures() - 1
        
        if next_start_idx > max_idx or next_end_idx < 0:
            return
        
        if k_msrs > 0 and self.curr_range[0] + self.curr_range[1] - 1 >= max_idx:
            return
        
        if k_msrs < 0 and self.curr_range[0] <= 0:
            return
        
        next_start_idx = max(0, next_start_idx)
        next_end_idx = min(next_end_idx, max_idx)
        next_len = next_end_idx - next_start_idx + 1
        self.curr_range = (next_start_idx, next_len)
        
        self.chunk: Chunk = self.piece.to_chunk(self.curr_range[0], self.curr_range[1])

        print(self.curr_range)
        self.ruler_widget.set_content(self.chunk)
        self.refresh_parts()

    def refresh_parts(self):
        for idx, h_chunk in enumerate(self.chunk.h_chunks):
            p = self.part_widgets[idx]
            p.set_content(h_chunk)
        self.update()
                    
    """COMMANDS' methods
    """

    def select_next_note(self):
        print("select next note (ScoreView)")
        for pt in self.part_widgets:
            pt.select_next_note()
        self.update()    
            
    def select_next_note_in_next_measure(self):
        print("select next note (ScoreView)")
        for pt in self.part_widgets:
            pt.select_next_note_in_next_measure()
        self.update()    
            
    def select_prev_note_in_prev_measure(self):
        print("select next note (ScoreView)")
        for pt in self.part_widgets:
            pt.select_prev_note_in_prev_measure()
        self.update()    
            
    def select_prev_note(self):
        print("select prev note (ScoreView)")
        for pt in self.part_widgets:
            pt.select_prev_note()
        self.update()    
        
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
            pt.delete_selected_notes()
        
        
    def order_notes_by_part_no(self):
        maybe: list[VisualNote] = [n for pt in self.part_widgets for n in pt.get_last_selected_note()]
        maybe = sorted(maybe, key=lambda x: x.inner.measure.m_no)
        maybe = sorted(maybe, key=lambda x: x.inner.measure.part_no)
        return maybe
    
    """
    OVERRIDEN
    """    
    @override                          
    def resizeEvent(self, event):
        h = self.widget.height()
        w = self.widget.width()
        if w - 100 > 0:
            self.back.setGeometry(0, 0, w, h)