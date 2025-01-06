from functools import cmp_to_key
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

import fonts.loader
from fonts.glyphs import Glyphs
from model.sample_piece_gen import Measure
from model.musical.structure import HorizontalChunk, MTuple, Note, Rest, TimeHolder
from utils.musical_layout.space import get_single_ruler, map_to
from widgets.lanes.BarrableWidget import BarrableWidget
from widgets.note_widgets.VisualNote import VisualNote
from widgets.painters.paint_manager import m_paint_visual, m_paint_tuple



class VirtualStaff():
    def __init__(self, parent=None, y_offset:int = None):
        super().__init__()
        self.parent = parent
        self.res_mtuples: list[list[VisualNote]] = []
        self.staff_offset = 30
        res, self.bravura_font = fonts.loader.try_get_music_font()
        self.very_dark_gray = QColor(40, 40, 40)
        self.dark_gray = QColor(100, 100, 100)
        self.light_gray = QColor(140, 140, 140)
        self.very_light_gray = QColor(160, 160, 160)
        self.light_black = QColor(13, 13, 13)
        self.clef_margin = 30
        self.visual_notes: list[VisualNote] = []
        self.notes = []
        self.note_size = 120
        self.line_spacing = 10
        self.bar_left_margin = 25
        self.bar_right_margin = 5
        self.x_offsets = None
        self.y_offset = y_offset if y_offset else 0

    def set_content(self, h_chunk: HorizontalChunk):
        self.measures = h_chunk.measures

    def get_h_segments(self):
        l_mar = self.bar_left_margin
        r_mar = self.bar_right_margin
        areas = [self.x_offsets[idx:idx+2] for idx in range(0, len(self.x_offsets)-1)]
        areas_2 = [[a[0] + l_mar, a[1] - r_mar] for a in areas]
        return areas_2


    def get_x_offsets(self, width: int) -> list[int]:
        av_space = width - self.clef_margin
        if av_space < 10:
            return [0, 10]
        measure_width = int(av_space/self.no_of_measures)
        infos = []
        for i in range(0, self.no_of_measures + 1):
            infos.append(self.clef_margin + measure_width * i)
        self.x_offsets = infos



    def draw_content(self, painter: QPainter, width: int):
        painter.translate(0, self.y_offset)
        self.no_of_measures = len(self.measures)
        self.get_x_offsets(width)
        if width < 30 :
            return
        self.calculate_vis_notes()
        painter.setFont(self.bravura_font)
        painter.setPen(self.dark_gray)
        painter.setBrush(self.dark_gray)

        self.draw_clef(painter)
        self.draw_staff_lines(painter, width)
        self.draw_bar_lines(painter)
        painter.setPen(self.light_gray)
        painter.setBrush(self.light_gray)
        for v_n in self.visual_notes:
            m_paint_visual(painter, v_n)

        for mt in self.res_mtuples:
            m_paint_tuple(painter, mt)

    def draw_clef(self, painter: QPainter):
        painter.drawText(QRect(0, -23, 40, 200), Qt.AlignTop, Glyphs.G_Clef)

    def calculate_vis_notes(self):
        bar_segments = self.get_h_segments()
        self.visual_notes = []
        self.res_mtuples: list[list[VisualNote]] = []
        new_mtuple: list[VisualNote] = []
        mtuple_opened = False
        for m_no, bar in enumerate(self.measures):
            seg_start = bar_segments[m_no][0]
            seg_end = bar_segments[m_no][1]
            clef = bar.get_clef()

            if seg_end - seg_start < 10:
                return
            width_in_beats = sum(th.real_duration().to_float() for th in bar.time_holders)
            for note in bar.time_holders:
                curr_x = int(note.ruler_event.offset_ratio.to_float() * (seg_end - seg_start)/width_in_beats + seg_start)
                if isinstance(note, Note):
                    res_y = int(((-note.pitch.vis_height() + clef.vis_pitch) * self.line_spacing) / 2) + self.line_spacing * 7
                elif isinstance(note, Rest):
                    res_y = int( (0) / 2) + self.line_spacing * 8

                vis_note = VisualNote(note, (curr_x, res_y))
                self.visual_notes.append(vis_note)


                if note.tuple_start:
                    mtuple_opened = True

                if mtuple_opened:
                    new_mtuple.append(vis_note)

                if note.tuple_end:
                    self.res_mtuples.append(new_mtuple)
                    new_mtuple = []
                    mtuple_opened = False


    def draw_staff_lines(self, painter: QPainter, width: int):
        for y_offset in self.get_staff_line_offsets():
            painter.drawRect(QRect(0, y_offset, width, 1))

    def draw_bar_lines(self, painter: QPainter):
        painter.drawRect(QRect(0, self.staff_offset, 1, 4*self.line_spacing))
        for x in self.x_offsets[1:]:
            painter.drawRect(QRect(x, self.staff_offset, 1, 4*self.line_spacing))

    def mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            click_pos = event.pos()
            x0 = click_pos.x()
            y0 = click_pos.y() - self.y_offset
            maybe = [v_n for v_n in self.visual_notes if abs(v_n.point[0] - x0) < 7 and abs(v_n.point[1] - y0) < 7]
            if not maybe:
                return

            self.select_note(maybe[0])

    def select_note(self, v_n: VisualNote):
        v_n.inner.is_selected = True
        if self.parent:
            self.parent.deselect_notes_but([v_n])
        else:
            self.deselect_notes_but([v_n])


    def select_all(self):
        selected = [d for d in self.visual_notes]
        if not selected:
            return

        for s in selected:
            s.inner.is_selected = True


    def delete_selected_notes(self):
        selected = [v_n for v_n in self.visual_notes if v_n.inner.is_selected]
        if not selected:
            return
        self.remove_note(selected[0])


    def deselect_notes_but(self, v_notes: list[VisualNote]):
        deselected = [d for d in self.visual_notes if d not in v_notes]
        if not deselected:
            return

        for d in deselected:
            d.inner.is_selected = False


    def remove_note(self, v_n: VisualNote):
        rest = v_n.inner.clone_as_rest().set_selected()
        v_n.inner.measure.replace_note(v_n.inner, rest)
        v_n.inner = rest

    def get_staff_line_offsets(self):
        offsets = []
        for i in range(0, 5):
            offsets.append(self.staff_offset + i*self.line_spacing)
        return offsets

    def get_last_selected_note(self):
        selected = [v_n for v_n in self.visual_notes if v_n.inner.is_selected][-1:]
        return selected

    def get_first_selected_note(self):
        selected = [v_n for v_n in self.visual_notes if v_n.inner.is_selected][:1]
        return selected



    """
    COMMAND METHODS
    """

    def rotate_selected_notes(self):
        selected = [v_n for v_n in self.visual_notes if v_n.inner.is_selected]
        for v_n in selected:
            v_n.inner.flip_orientation()

    def select_prev_note(self):
        selected = self.get_first_selected_note()
        if not selected:
            return

        sel = selected[0]


        idx = self.visual_notes.index(sel)

        if idx == 0:
            return

        if self.parent:
            self.parent.deselect_notes_but([])
        else:
            self.deselect_notes_but([])

        nxt = self.visual_notes[idx - 1]
        nxt.inner.is_selected = True


    def select_next_note(self):
        selected = self.get_last_selected_note()
        if not selected:
            return

        sel = selected[0]


        idx = self.visual_notes.index(sel)

        if idx == len(self.visual_notes) - 1:
            return

        if self.parent:
            self.parent.deselect_notes_but([])
        else:
            self.deselect_notes_but([])

        nxt = self.visual_notes[idx + 1]
        nxt.inner.is_selected = True


    def select_next_note_in_next_measure(self):
        selected = self.get_last_selected_note()
        if not selected:
            return

        sel = selected[0]
        m = sel.inner.measure
        if m not in self.measures:
            return

        idx = self.measures.index(m)

        if idx == len(self.measures) - 1:
            return

        if self.parent:
            self.parent.deselect_notes_but([])
        else:
            self.deselect_notes_but([])

        m_to_sel = self.measures[idx+1]
        m_to_sel.time_holders[0].is_selected = True;


    def select_prev_note_in_prev_measure(self):
        selected = self.get_first_selected_note()
        if not selected:
            return

        sel = selected[0]
        m = sel.inner.measure
        if m not in self.measures:
            return

        idx = self.measures.index(m)
        if idx == 0:
            return

        if self.parent:
            self.parent.deselect_notes_but([])
        else:
            self.deselect_notes_but([])

        m_to_sel = self.measures[idx-1]
        m_to_sel.time_holders[0].is_selected = True;
