from fonts.glyphs import Glyphs
from model.musical.structure import Note
from utils.geometry.transform2d import T2D
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor
from widgets.painters.painter_definitions import get_dotting_painters, get_painter_definitions, get_accidental_painters
from widgets.note_widgets.VisualNote import VisualNote

painter_data_list = get_painter_definitions()
dot_painters = get_dotting_painters()
acc_painters = get_accidental_painters()

transp = QColor(0, 0, 0, 0)
dark_gray = QColor(100, 100, 100)
light_gray = QColor(140, 140, 140)
very_dark_gray = QColor(50, 50, 50)
very_light_gray = QColor(160, 160, 160)
red = QColor(200, 44, 44)

class ElementaryPainter():
    def __init__(self):
        self.box_w_half = 15
        self.box_h_half = 50
        self.offset = T2D()
        self.head_offset: list[T2D] = [T2D(-4, 1), T2D(-4, 1)]
        self.stem_offset: list[T2D] = [T2D(8, 0), T2D(-4, 37)]
        self.flag_offset: list[T2D] = [T2D(8, -37), T2D(-4, 37)]
        # self.acc_offset: list[T2D] = [T2D(-2, 2), T2D(-2, 2)]
        
    def paint_visual_note(self, q_painter: QPainter, v_n: VisualNote, line_spacing: int):
        inner = v_n.inner
        inner_type = type(inner)
        is_up = v_n.inner.orientation_up
        maybe = [p for p in painter_data_list if p.t == inner_type and p.d == inner.base_duration and p.orientation_up == is_up]

        dot = v_n.inner.dotting
        dot_str = ""
        dptr = [dptr2 for dptr2 in dot_painters if dptr2[0] == dot]
        if dptr:
            dot_str = dptr[0][1]

        if not maybe:
            return

        p_d = maybe[0]

        t2d = T2D(v_n.point[0], v_n.point[1])

        color = red if inner.is_selected else very_light_gray

        clef = v_n.inner.measure.get_clef()

        if isinstance(inner, Note):
            clef_vis_pitch = clef.vis_pitch
            clef_n_lines = clef.n_of_lines
            inner.pitch.vis_pitch()
        
        plc_idx = 0 if is_up else 1
        self.paint_text(t2d + self.head_offset[plc_idx], q_painter, p_d.head_str + " " + dot_str, color)
        if p_d.stemed:
            self.paint_text(t2d + self.stem_offset[plc_idx], q_painter, p_d.stem_str, color)
        if p_d.flagged:
            self.paint_text(t2d + self.flag_offset[plc_idx], q_painter, p_d.flag_str, color)

        if isinstance(v_n.inner, Note):
            note: Note = v_n.inner
            maybe = [s for s in acc_painters if s[0] == note.pitch.alter]
            if not maybe:
                return
            ptr = maybe[0]
            s = ptr[1]
            t = (t2d + ptr[plc_idx + 2]).add_x(-14)
            self.paint_text(t, q_painter, s, color)
                
    def paint_text(self, t: T2D, q_painter: QPainter, s: str, color: QColor, sel: bool = False):
        text_rect = QRect(t.x, t.y - self.box_h_half, self.box_w_half*2, self.box_h_half*2)

        if sel:
            q_painter.setBrush(transp)
            q_painter.setPen(very_dark_gray)
            q_painter.drawRect(text_rect)

        q_painter.setPen(color)
        q_painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, s)
    
    def paint_tuple(self, q_painter: QPainter, v_notes: list[VisualNote]):
        p1 = v_notes[:1][0].point
        p2 = v_notes[-1:][0].point


        a = (p2[1] - p1[1])/(p2[0] - p1[0])
        inbetween = v_notes[1:][:-1]
        if inbetween:
            min_val, max_val = self.get_min_max_diff(a, p1[0], p1[1], v_notes[1:][:-1])
        else:
            min_val, max_val = (0, 0)
        fix = max(int(max_val), 0)
        v_h = 7
        d = v_h + fix
        h = 5
        w = 30
        q_painter.setPen(light_gray)
        q_painter.drawLine(p1[0], p1[1] + h, p1[0], p1[1] + h + d)
        q_painter.drawLine(p1[0], p1[1] + d + h, p2[0], p2[1] + h + d)
        q_painter.drawLine(p2[0], p2[1] + h, p2[0], p2[1] + h + d)
        x_m = int((p1[0] + p2[0])/2)
        y_m = int((p1[1] + p2[1])/2)
        text_rect = QRect(int(x_m - w/2), y_m + 10 + fix, w, w)
        q_painter.drawText(text_rect, Qt.AlignCenter | Qt.AlignVCenter, Glyphs.Tuplet_3)

    def get_min_max_diff(self, a: float, x_0: float, y_0, inbetween_notes: list[VisualNote]):
        diffs = self.get_diffs(a, x_0, y_0, inbetween_notes)
        min_val = min(diffs)
        max_val = max(diffs)
        return min_val, max_val

    def get_diffs(self, a, x_0, y_0, inbetween_notes: list[VisualNote]):
        res = [(n.point[1] - a*(n.point[0] - x_0)) - y_0  for n in inbetween_notes]
        return res

