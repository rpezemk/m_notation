import random
from typing import Any, Callable
from PyQt5.QtGui import QColor
from fonts.glyphs import Glyphs
from model.ratio import Dotting, Ratio
from model.pitch import Pitch, NoteName

def to_moving_sum_with_zero(len_ratios: list[Ratio]) -> list[Ratio]:
    curr = Ratio.zero()
    offset_ratios = []
    for l_r in len_ratios:
        offset_ratios.append(curr)
        curr = curr + l_r
    return offset_ratios

def to_moving_sum(len_ratios: list[Ratio]) -> list[Ratio]:
    curr = Ratio.zero()
    offset_ratios = []
    for l_r in len_ratios:
        curr = curr + l_r
        offset_ratios.append(curr)
    return offset_ratios

class TimeHolder():
    def __init__(self, base_duration: Ratio = None, measure: 'Measure' = None, dotting: Ratio = None):
        self.base_duration = base_duration if base_duration is not None else Ratio.QUARTER
        self.dotting = dotting if dotting is not None else Ratio.zero()
        self.measure = measure
        self.offset_ratio = Ratio.zero()
        self.is_selected = False
        self.scale = Ratio(t=(1, 1))
        self.tuple_start = False
        self.tuple_end = False
        self.orientation_up = True
        self.ruler_event: RulerEvent = None
        self.visual_note: VisualNote = None
    
    def try_get_prev_note(self):
        m = self.measure
        idx = m.time_holders.index(self)
        if idx > 0:
            prev = m.time_holders[idx-1]
            return isinstance(prev, Note), prev
            
        p = m.part
        idx = p.measures.index(m)
        if idx == 0:
            return False, None
        
        prev_m = p.measures[idx - 1]
        if not prev_m.time_holders:
            return False, None
        
        prev = prev_m.time_holders[-1:][0]
        return isinstance(prev, Note), prev
        
    def try_get_next_note(self):
        m = self.measure
        idx = m.time_holders.index(self)
        max_idx = len(m.time_holders) - 1
        if idx < max_idx:
            nxt = m.time_holders[idx+1]
            return isinstance(nxt, Note), nxt
            
        p = m.part
        idx = p.measures.index(m)
        max_idx = len(p.measures) - 1
        if idx == max_idx:
            return False, None
        
        next_m = p.measures[idx + 1]
        if not next_m.time_holders:
            return False, None
        
        nxt = next_m.time_holders[0]
        return isinstance(nxt, Note), nxt
    
    
    def flip_orientation(self):
        ...

    def is_first_in_measure(self):
        if not self.measure.time_holders:
            return False
        
        res = self.measure.time_holders[0] == self
        return res

    def real_duration(self):
        res = (self.base_duration + self.base_duration * self.dotting) * self.scale
        return res

    def dot(self, n: int = 1):
        self.dotting = Ratio(t=(1, 2))
        return self

    def double_dot(self):
        self.dotting = Ratio(t=(3, 4))
        return self

    def __str__(self):
        return f"d: {self.base_duration}"

    def clone_as_rest(self):
        rest = Rest(base_duration=self.base_duration, measure=self.measure, dotting=self.dotting)
        rest.scale = self.scale
        rest.tuple_start = self.tuple_start
        rest.tuple_end = self.tuple_end
        rest.offset_ratio = self.offset_ratio
        rest.ruler_event = self.ruler_event
        return rest

    def set_selected(self):
        self.is_selected = True
        return self
    
    def change_duration(self, base_duration: Ratio):
        self.base_duration = base_duration
        return self

    def r1(self): return self.change_duration(Ratio(t=(1, 1)))
    def r2(self): return self.change_duration(Ratio(t=(1, 2)))
    def r4(self): return self.change_duration(Ratio(t=(1, 4)))
    def r8(self): return self.change_duration(Ratio(t=(1, 8)))
    def r16(self): return self.change_duration(Ratio(t=(1, 16)))
    def r32(self): return self.change_duration(Ratio(t=(1, 32)))
    
class Rest(TimeHolder):
    def __init__(self, base_duration: Ratio = None, measure: 'Measure' = None, dotting: Dotting = None):
        super().__init__(base_duration, measure, dotting)
        self.measure = measure

    def __str__(self):
        return f"d: {self.base_duration}"


class MTuple():
    def apply(scale: Ratio, notes: list[TimeHolder]):
        if not notes:
            return notes

        for n in notes:
            n.scale = scale.clone()

        notes[:1][0].tuple_start = True
        notes[-1:][0].tuple_end = True
        return notes

class Note(TimeHolder):
    def __init__(self, pitch: Pitch, base_duration = None, measure: 'Measure' = None, dotting: Dotting = None):
        super().__init__(base_duration, measure, dotting)
        self.measure = measure
        self.pitch = pitch
        self.orientation_up = True
        self.tied = False
        
    def __str__(self):
        return f"d: {self.base_duration}"

    def flip_orientation(self):
        self.orientation_up = not self.orientation_up

    def add_oct(self, octaves: int = 0):
        self.pitch.oct_no += octaves
        return self

    def add_alter(self, alter: int = 0):
        self.pitch.alter += alter
        return self
        
        
    def C(): return Note(Pitch(NoteName.C))
    def D(): return Note(Pitch(NoteName.D))
    def E(): return Note(Pitch(NoteName.E))
    def F(): return Note(Pitch(NoteName.F))
    def G(): return Note(Pitch(NoteName.G))
    def A(): return Note(Pitch(NoteName.A))
    def B(): return Note(Pitch(NoteName.B))
    
    def sharp(self):
        self.pitch.alter = 1
        return self
    
    def double_sharp(self):
        self.pitch.alter = 2
        return self
    
    def flat(self):
        self.pitch.alter = -1
        return self
    
    def double_flat(self):
        self.pitch.alter = -2
        return self
    
    def o_up(self): 
        return self.add_oct(1)
    
    def o_dwn(self): 
        return self.add_oct(-1)

    def tie(self):
        self.tied = True
        return self
    
class Measure():
    def __init__(self, part_no: int, m_no: int, notes: list[TimeHolder]=None, parent: 'Part'=None):
        self.part = parent
        self.m_no = m_no
        self.part_no = part_no
        self.time_holders = [] if notes is None else notes
        self.calc_offsets()
        self.ruler_bar: RulerBar = None
        
    def replace_note(self, old: TimeHolder, new: TimeHolder):
        if not old in self.time_holders:
            return

        idx = self.time_holders.index(old)
        self.time_holders[idx] = new

    def get_clef(self):
        res = self.part.clef
        return res
    
    def calc_offsets(self):
        curr_pos = Ratio.zero()
        for th in self.time_holders:
            th.offset_ratio = curr_pos
            curr_pos += th.real_duration()
    
    def validate(self):
        for th in self.time_holders:
            if not isinstance(th, Note):
                continue
            n: Note = th
            if not n.tied:
                continue
            
            nxt_is_note, nxt = n.try_get_next_note()
            
            if not nxt_is_note:
                n.tied = False
                continue
            
            # validate tie -- allow only same midi pitch ties
            if n.tied and n.pitch.midi_pitch() != nxt.pitch.midi_pitch():
                n.tied = False
    
class Part():
    def __init__(self, clef: 'Clef', measures: list[Measure]=None, piece: 'Piece'=None):
        self.clef = clef
        self.piece = piece
        self.measures = [] if measures is None else measures

    def validate(self):
        for m in self.measures:
            m.validate()        
        return self
    
class TempoMark():
    def __init__(self, bpm: float, bpm_base: Ratio, bar_no: int, bar_offset: Ratio):
        self.bar_no = 0
        self.bpm = bpm
        self.bmp_base = bpm_base
        self.bar_no = bar_no
        self.bar_offset = bar_offset


class ConductorPart():
    def __init__(self, initial_tempo_mark: TempoMark):
        self.base_tempo_mark = initial_tempo_mark
        self.tempo_marks: list[TempoMark] = [initial_tempo_mark]



class Piece():
    def __init__(self, parts: list[Part]=None, conductor_part: ConductorPart = None):
        self.parts = [] if parts is None else parts
        self.conductor_part = conductor_part if conductor_part is not None else ConductorPart()

    def to_chunk(self, m_no, m_count):
        lanes = self.filter_by_measures(m_no, m_count)
        v_chunks = [VerticalChunk([lane[m_idx] for lane in lanes]) for m_idx in range(m_count)]
        res_chunk = Chunk(v_chunks)
        return res_chunk

    def filter_by_measures(self, m_idx, m_count):
        filtered = [p.measures[m_idx:][:m_count] for p in self.parts]
        return filtered

    def n_measures(self):
        if not self.parts:
            return 0

        return len(self.parts[0].measures)

    def validate(self):
        for p in self.parts:
            p.validate()
        
        return self

class RulerEvent():
    def __init__(self, len_ratio: Ratio, offset_ratio: Ratio):
        self.len_ratio = len_ratio
        self.add_len = Ratio.zero()
        self.offset_ratio = offset_ratio
        self.add_offset = Ratio.zero()
        self.inner_events:list[TimeHolder] = []

    def __str__(self):
        return f"at: {self.offset_ratio}, d:{self.len_ratio}, i_es:{len(self.inner_events)}"

class RulerBar():
    def __init__(self, events: list[RulerEvent]):
        self.events = events
    
        self.calculate_super_lengths()
        
        curr = Ratio(t=(0, 1))
        for e in self.events:
            curr += e.len_ratio + e.add_len
        
        self.total_len_ratio = curr
        
    def calculate_super_lengths(self):
        for e in self.events:
            add = Ratio(t=(0, 1))
            for th in e.inner_events:
                if isinstance(th, Note):
                    n: Note = th
                    additional_place = Ratio(t=(abs(n.pitch.alter), 64))
                    if additional_place > add:
                        add = additional_place
            e.add_len = add        
                    
        add_offsets = to_moving_sum([a.add_len for a in self.events])
        
        for i, e in enumerate(self.events):
            e.add_offset = add_offsets[i]
            
class HorizontalChunk():
    """model for vertical one-measure length, n-parts height section.
    """
    def __init__(self, part: list[Measure] = None):
        self.measures = [] if part is None else part


class VerticalChunk():
    """model for vertical one-measure length, n-parts height section.
    """
    def __init__(self, one_measure_parts: list[Measure]):
        self.vertical_measures = one_measure_parts

    def ratio_lanes_to_ruler_bar(self) -> RulerBar:
        total: Ratio = VerticalChunk.to_sum(th.real_duration() for th in self.vertical_measures[0].time_holders)
        mov = sorted(set(
                    [
                        Ratio.zero(), 
                        *[th.offset_ratio for m in self.vertical_measures for th in m.time_holders],
                        total
                    ]) 
                , key=lambda r: r.to_float())

        ruler_events: list[RulerEvent] = [RulerEvent(mov[i+1] - mov[i], mov[i]) for i in range(len(mov) - 1)]
                
        for evt in ruler_events:
            time_holders = [th for m in self.vertical_measures for th in m.time_holders if th.offset_ratio == evt.offset_ratio]
            evt.inner_events = time_holders
            for th in time_holders:
                th.ruler_event = evt
                
        ruler_bar = RulerBar(ruler_events)
        for m in self.vertical_measures:
            m.ruler_bar = ruler_bar
        
        return ruler_bar

    def to_moving_sum(lane: list[Ratio]) -> list[Ratio]:
        curr = Ratio.zero()
        res = []
        for r in lane:
            curr = curr + r
            res.append(curr)
        return res
    
    def to_sum(ratios: list[Ratio]) -> list[Ratio]:
        curr = Ratio.zero()
        for r in ratios:
            curr = curr + r
        return curr

class Chunk:
    def __init__(self, v_chunks: list[VerticalChunk]):
        self.v_chunks = v_chunks
        self.duration_ratio = Ratio(t=(4,4))
        self.h_chunks = [HorizontalChunk() for _ in v_chunks[0].vertical_measures]

        for v_ch in v_chunks:
            for part_no, m in enumerate(v_ch.vertical_measures):
                self.h_chunks[part_no].measures.append(m)

    def to_ruler_bars(self) -> list[RulerBar]:
        lanes_data2 = [v_ch.ratio_lanes_to_ruler_bar() for v_ch in self.v_chunks]
        return lanes_data2

    def all_time_holders(self):
        time_holders = [th for v_ch in self.v_chunks for m in v_ch.vertical_measures for th in m.time_holders]
        return time_holders


    def get_last_by(self, func: Callable[[TimeHolder], bool]):
        time_holders = [th for v_ch in self.v_chunks for m in v_ch.vertical_measures for th in m.time_holders if func(th)]
        return time_holders


class PointObject():
    def __init__(self, note: Note):
        pass

class Staccato():
    def __init__(self, note: Note):
        pass

class Tenuto():
    def __init__(self, note: Note):
        pass

class Dynamics():
    def __init__(self, note: Note, offset: Ratio):
        ...

class WideThConstrainedObject():
    def __init__(self, note0: TimeHolder, note1: TimeHolder):
        self.note0 = note0
        self.note1 = note1

class Slur(WideThConstrainedObject):
    def __init__(self, start_note, end_note):
        super().__init__(start_note, end_note)
        
        
class LongFreeHObject():
    def __init__(self, start_note: Note, start_offset: Ratio, end_note: Note, end_offset: Ratio):
        ...

class FadeDynamics(LongFreeHObject):
    def __init__(self, start_note, start_offset, end_note, end_offset):
        super().__init__(start_note, start_offset, end_note, end_offset)

class FadeInDynamics(FadeDynamics):
    def __init__(self, start_note, start_offset, end_note, end_offset):
        super().__init__(start_note, start_offset, end_note, end_offset)

class FadeOutDynamics(FadeDynamics):
    def __init__(self, start_note, start_offset, end_note, end_offset):
        super().__init__(start_note, start_offset, end_note, end_offset)
        
class Clef():
    def __init__(self, base_line_pitch: Pitch, n_of_lines: int = 5, clef_str: str = Glyphs.G_Clef, clef_y_offset: int = 0):
        self.base_line_pitch = base_line_pitch
        self.n_of_lines = n_of_lines
        self.vis_pitch = base_line_pitch.vis_pitch()
        self.clef_str = clef_str
        self.clef_y_offset = clef_y_offset
        ...

class AllClefs():
    TREBLE_CLEF = Clef(Note.E().pitch, clef_str=Glyphs.G_Clef)
    BASS_CLEF = Clef(Note.G().o_dwn().o_dwn().pitch, clef_str=Glyphs.F_Clef, clef_y_offset=21)

class SampleFamily():
    ...

class InstrInfo():
    def __init__(self, name: str, clef: Clef, sample_family: SampleFamily, lowest, highest):
        ...
        
        
        
class VisualNote():
    def __init__(self, note: TimeHolder, point: tuple[float, float], seg_start: int, seg_end: int):
        self.inner = note
        self.inner.visual_note = self
        self.point = point
        self.is_selected = False
        self.seg_start = seg_start
        self.seg_end = seg_end

class VisualTuple():
    def __init__(self, v_notes: list[VisualNote]):
        self.notes = v_notes