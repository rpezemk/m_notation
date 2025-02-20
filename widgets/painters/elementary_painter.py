from fonts.glyphs import Glyphs
from model.musical.structure import Note, VisualNote, VisualTuple
from utils.geometry.transform2d import T2D
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QPen
from widgets.painters.painter_definitions import get_dotting_painters, get_note_painters, get_accidental_painters, get_rest_painters
import math
note_painters = get_note_painters()
rest_painters = get_rest_painters()
dot_painters = get_dotting_painters()
acc_painters = get_accidental_painters()

transp = QColor(0, 0, 0, 0)
dark_gray = QColor(100, 100, 100)
light_gray = QColor(140, 140, 140)
very_dark_gray = QColor(50, 50, 50)
very_light_gray = QColor(160, 160, 160)
red = QColor(200, 44, 44)

box_w_half = 15
box_h_half = 50
offset = T2D()
head_offset: list[T2D] = [T2D(-4, 1), T2D(-4, 1)]
stem_offset: list[T2D] = [T2D(8, 0), T2D(-4, 37)]
flag_offset: list[T2D] = [T2D(8, -37), T2D(-4, 37)]

#### METHODS FOR EXTERNAL USE #### 

def paint_time_holders(q_painter: QPainter, visual_notes_by_measure: list[list[VisualNote]], v_note_spacing: int, base_y_offset: int):
    res_mtuples: list[list[VisualNote]] = []
    new_mtuple: list[VisualNote] = []
    mtuple_opened = False
    
    all_shown_notes = [vn.inner for m in visual_notes_by_measure for vn in m]

    for visual_notes in visual_notes_by_measure:
    
        for v_n in visual_notes:
            paint_time_holder(q_painter, v_n, v_note_spacing, base_y_offset)

        # build tuple groups
        for v_n in visual_notes:
            if v_n.inner.tuple_start:
                mtuple_opened = True
            if mtuple_opened:
                new_mtuple.append(v_n)
            if v_n.inner.tuple_end:
                res_mtuples.append(new_mtuple)
                new_mtuple = []
                mtuple_opened = False

        # draw bracket for each group
        for tuple_v_notes in res_mtuples:
                paint_tuple_bracket(q_painter, tuple_v_notes)

        # draw ties
        for v_n in visual_notes:
            if not isinstance(v_n.inner, Note):
                continue
            
            n: Note = v_n.inner
            
            if n.tied: 
                ok, nxt = n.try_get_next_note()   
                if not ok:
                    continue
                
                if nxt in all_shown_notes:
                    draw_tie(q_painter, v_n, nxt.visual_note)
                else:
                    draw_right_passing_tie(q_painter, v_n)
            
            ok, prev = n.try_get_prev_note()
            if not ok: 
                continue
            
            if prev in all_shown_notes:
                continue
            if prev.tied:
                draw_left_passing_tie(q_painter, v_n)
        
        
    #draw slurs
    all_visible_notes: list[Note] = [vn for vn in all_shown_notes if isinstance(vn, Note)]
    all_slur_starting = [sl for vn in all_visible_notes for sl in vn.slur_starts]
    all_slur_ending = [sl for vn in all_visible_notes for sl in vn.slur_ends]
    
    full_visible_slurs = [sl for sl in all_slur_starting if sl in all_slur_ending]
    
    for slur in full_visible_slurs:
        ...
        draw_tie(q_painter, slur.note0.visual_note, slur.note1.visual_note)
    
    
    left_passing_slurs = [sl for sl in all_slur_ending if sl not in all_slur_starting]
    right_passing_slurs = [sl for sl in all_slur_starting if sl not in all_slur_ending]
        
        
    for right_slur in left_passing_slurs:
        draw_left_passing_tie(q_painter, right_slur.note1.visual_note)    

        
    for right_slur in right_passing_slurs:
        draw_right_passing_tie(q_painter, right_slur.note0.visual_note)    
        
def paint_time_holder(q_painter: QPainter, v_n: VisualNote, v_note_spacing: int, base_y_offset: int):
    color = red if v_n.inner.is_selected else very_light_gray
    if isinstance(v_n.inner, Note):
        paint_visual_note(q_painter, v_n, v_note_spacing, base_y_offset, color)
    else:
        paint_visual_rest(q_painter, v_n, v_note_spacing, base_y_offset, color)
        
               

#### INTERNAL USAGE METHODS ####
        
def paint_visual_note(q_painter: QPainter, v_n: VisualNote, v_note_spacing: int, base_y_offset: int, color: QColor):
    inner = v_n.inner
    is_up = v_n.inner.orientation_up
    
    maybe = [p for p in note_painters if p[0] == inner.base_duration]

    dot = inner.dotting
    dot_str = ""
    dptr = [dptr2 for dptr2 in dot_painters if dptr2[0] == dot]
    if dptr:
        dot_str = dptr[0][1]

    if not maybe:
        return

    p_d = maybe[0]

    t2d = T2D(v_n.point[0], v_n.point[1])



    clef = inner.measure.get_clef()

    if isinstance(inner, Note):
        draw_ledger_lines(q_painter, v_note_spacing, base_y_offset, inner, t2d, color, clef)
        
                    
    plc_idx = 0 if is_up else 1
    paint_text(t2d + head_offset[plc_idx], q_painter, p_d[1] + " " + dot_str, color)
    if p_d[2][0]:
        paint_text(t2d + stem_offset[plc_idx], q_painter, p_d[2][1][0], color)
    if p_d[3][0]:
        paint_text(t2d + flag_offset[plc_idx], q_painter, p_d[3][1][plc_idx], color)

    if isinstance(inner, Note):
        return draw_accidentals(q_painter, v_n, t2d, color, plc_idx)
    
    
def paint_visual_rest(q_painter: QPainter, v_n: VisualNote, v_note_spacing: int, base_y_offset: int, color: QColor):
    inner = v_n.inner

    maybe = [p for p in rest_painters if p[0] == inner.base_duration]

    dot = v_n.inner.dotting
    dot_str = ""
    dptr = [dptr2 for dptr2 in dot_painters if dptr2[0] == dot]
    if dptr:
        dot_str = dptr[0][1]

    if not maybe:
        return

    p_d = maybe[0]

    t2d = T2D(v_n.point[0], v_n.point[1])

    paint_text(t2d + head_offset[0], q_painter, p_d[1] + " " + dot_str, color)
    

def draw_accidentals(q_painter, v_n, t2d, color, plc_idx):
    note: Note = v_n.inner
    maybe = [s for s in acc_painters if s[0] == note.pitch.alter]
    if not maybe:
        return
    ptr = maybe[0]
    s = ptr[1]
    t = (t2d + ptr[plc_idx + 2]).add_x(-14)
    paint_text(t, q_painter, s, color)


def draw_ledger_lines(q_painter, v_note_spacing, base_y_offset, inner, t2d, color, clef):
    clef_vis_pitch = clef.vis_pitch
    n_higher_than_base = inner.pitch.vis_pitch() - clef_vis_pitch
    n_below = max(-n_higher_than_base, 0) // 2
    
    low_base = T2D(t2d.x, base_y_offset)
        
    for n in range(n_below):
        paint_text(low_base.add_y(v_note_spacing * (n+1) * 2 + 1).add_x(-8), q_painter, Glyphs.LedgerLine, color)
        paint_text(low_base.add_y(v_note_spacing * (n+1) * 2 + 1).add_x(-4), q_painter, Glyphs.LedgerLine, color)
        
        
    higher_than_highest = max((n_higher_than_base - (clef.n_of_lines - 1) * 2), 0)
    n_above = higher_than_highest // 2
        
    high_base = T2D(t2d.x, base_y_offset - (clef.n_of_lines) * v_note_spacing * 2 + 1)
        
    for n in range(n_above):
        paint_text(high_base.add_x(-8).add_y(-n*2*v_note_spacing), q_painter, Glyphs.LedgerLine, color)
        paint_text(high_base.add_x(-4).add_y(-n*2*v_note_spacing), q_painter, Glyphs.LedgerLine, color)
        

def draw_tie(q_painter: QPainter, v_n1: VisualNote, v_n2: VisualNote):
    if not isinstance(v_n1.inner, Note) or not isinstance(v_n2.inner, Note):
        return
    
    clef = v_n1.inner.measure.get_clef()
    n1: Note = v_n1.inner
    diff = n1.pitch.vis_pitch() - clef.vis_pitch
    is_up = (diff) - clef.n_of_lines > 0
    
    if is_up:
        ...
    else:
        ...
    
    mul = -1 if is_up else 1
    x0, y0, x1, y1 = v_n1.point[0], v_n1.point[1], v_n2.point[0], v_n2.point[1]
    
    x_diff = x1 - x0
    
    dx = 5
    dy = mul * 7
    dyc = int(mul * 5 * (1 + math.sqrt(x_diff/10)))
    
    q_painter.setBrush(transp)
    control1_x, control1_y = x0 + 1/4*(x1-x0), y0 + dyc
    control2_x, control2_y = x0 + 3/4*(x1-x0), y0 + dyc

    path = QPainterPath()
    path.moveTo(x0 + dx, y0 + dy)
    path.cubicTo(control1_x, control1_y, control2_x, control2_y, x1 - dx, y1 + dy)

    q_painter.drawPath(path)
    
def draw_left_passing_tie(q_painter: QPainter, v_n1: VisualNote):
    clef = v_n1.inner.measure.get_clef()
    n1: Note = v_n1.inner
    diff = n1.pitch.vis_pitch() - clef.vis_pitch
    is_up = (diff) - clef.n_of_lines > 0
    
    if is_up:
        ...
    else:
        ...
    
    mul = -1 if is_up else 1
    x0, y0, x1, y1 = v_n1.seg_start-30, v_n1.point[1], v_n1.point[0], v_n1.point[1]
    
    x_diff = x1 - x0
    
    dx = 5
    dy = mul * 7
    dyc = int(mul * 5 * (1 + math.sqrt(x_diff/10)))
    
    y_end = mul * 15
    
    q_painter.setBrush(transp)
    control1_x, control1_y = x0 + 1/4*(x1-x0), y0 + dy + y_end
    control2_x, control2_y = x0 + 3/4*(x1-x0), y0 + dyc

    path = QPainterPath()
    path.moveTo(x0 + dx, y0 + dy + y_end)
    path.cubicTo(control1_x, control1_y, control2_x, control2_y, x1 - dx, y1 + dy)

    q_painter.drawPath(path)
    
    
def draw_right_passing_tie(q_painter: QPainter, v_n1: VisualNote):
    clef = v_n1.inner.measure.get_clef()
    n1: Note = v_n1.inner
    diff = n1.pitch.vis_pitch() - clef.vis_pitch
    is_up = (diff) - clef.n_of_lines > 0
    
    if is_up:
        ...
    else:
        ...
    
    mul = -1 if is_up else 1
    x0, y0, x1, y1 = v_n1.point[0], v_n1.point[1], v_n1.seg_end, v_n1.point[1]
    
    x_diff = x1 - x0
    
    dx = 5
    dy = mul * 7
    dyc = int(mul * 5 * (1 + math.sqrt(x_diff/10)))
    
    y_end = mul * 25
    
    q_painter.setBrush(transp)
    control1_x, control1_y = x0 + 1/4*(x1-x0), y0 + dyc
    control2_x, control2_y = x0 + 3/4*(x1-x0), y0 + dy + y_end

    path = QPainterPath()
    path.moveTo(x0 + dx, y0 + dy)
    path.cubicTo(control1_x, control1_y, control2_x, control2_y, x1 - dx, y1 + dy + y_end)

    q_painter.drawPath(path)

    
def paint_text(t: T2D, q_painter: QPainter, s: str, color: QColor, sel: bool = False):
    text_rect = QRect(t.x, t.y - box_h_half, box_w_half*2, box_h_half*2)

    if sel:
        q_painter.setBrush(transp)
        q_painter.setPen(very_dark_gray)
        q_painter.drawRect(text_rect)

    q_painter.setPen(color)
    q_painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, s)


def paint_tuple_bracket(q_painter: QPainter, v_notes: list[VisualNote]):
    p1 = v_notes[:1][0].point
    p2 = v_notes[-1:][0].point

    a = (p2[1] - p1[1])/(p2[0] - p1[0])
    inbetween = v_notes[1:][:-1]
    if inbetween:
        min_val, max_val = get_min_max_diff(a, p1[0], p1[1], v_notes[1:][:-1])
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

    
def get_min_max_diff(a: float, x_0: float, y_0, inbetween_notes: list[VisualNote]):
    diffs = get_diffs(a, x_0, y_0, inbetween_notes)
    min_val = min(diffs)
    max_val = max(diffs)
    return min_val, max_val

def get_diffs(a, x_0, y_0, inbetween_notes: list[VisualNote]):
    res = [(n.point[1] - a*(n.point[0] - x_0)) - y_0  for n in inbetween_notes]
    return res
    