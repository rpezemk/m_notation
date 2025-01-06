import random
from typing import Any, Callable
from PyQt5.QtGui import QColor
from model.ratio import Dotting, Ratio
from model.pitch import Pitch, NoteName
from model.musical.part_info import Clef

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

    def flip_orientation(self):
        ...

    def real_duration(self):
        res = (self.base_duration + self.base_duration * self.dotting) * self.scale
        return res

    def dot(self, n: int = 1):
        self.dotting = [a for a in range(n)]
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
    
    def flat(self):
        self.pitch.alter = -1
        return self
    
    def o_up(self): 
        return self.add_oct(1)
    
    def o_dwn(self): 
        return self.add_oct(-1)

    
    
class Measure():
    def __init__(self, part_no: int, m_no: int, notes: list[TimeHolder]=None, parent: 'Part'=None):
        self.part = parent
        self.m_no = m_no
        self.part_no = part_no
        self.time_holders = [] if notes is None else notes

    def replace_note(self, old: TimeHolder, new: TimeHolder):
        if not old in self.time_holders:
            return

        idx = self.time_holders.index(old)
        self.time_holders[idx] = new

    def get_clef(self):
        res = self.part.clef
        return res
    
    
class Part():
    def __init__(self, clef: Clef, measures: list[Measure]=None, piece: 'Piece'=None):
        self.clef = clef
        self.piece = piece
        self.measures = [] if measures is None else measures


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



class RulerEvent():
    def __init__(self, len_ratio: Ratio, offset_ratio: Ratio):
        self.len_ratio = len_ratio
        self.offset_ratio = offset_ratio
        self.inner_events:list[TimeHolder] = []

    def __str__(self):
        return f"at: {self.offset_ratio}, d:{self.len_ratio}, i_es:{len(self.inner_events)}"

class CsEvent():
    def __init__(self, i_no: int, start_offset: float, duration: float):
        ...


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

    def ratio_lanes_to_ruler(self) -> list[RulerEvent]:
        lanes = [[th.real_duration() for th in m.time_holders] for m in self.vertical_measures]
        for v_m in self.vertical_measures:
            curr_pos = Ratio.zero()
            for th in v_m.time_holders:
                th.offset_ratio = curr_pos
                curr_pos += th.real_duration()
        moving_sum_lanes: list[tuple[list[Ratio], list[Ratio]]] = [(lane, VerticalChunk.to_moving_sum(lane)) for lane in lanes]
        mov_ordered_list =[Ratio.zero(), *sorted(set([r for bar_ratios in moving_sum_lanes for r in bar_ratios[1]]), key=lambda r: r.to_float())]
        ruler_events: list[RulerEvent] = []


        for idx, offset_ratio in enumerate(mov_ordered_list[:-1]):
            len_ratio = mov_ordered_list[idx+1] - offset_ratio
            evt = RulerEvent(len_ratio, offset_ratio)
            ruler_events.append(evt)

        for evt in ruler_events:
            time_holders = [th for m in self.vertical_measures for th in m.time_holders if th.offset_ratio == evt.offset_ratio]
            evt.inner_events = time_holders

        return ruler_events

    def to_moving_sum(lane: list[Ratio]) -> list[Ratio]:
        curr = Ratio.zero()
        res = []
        for r in lane:
            curr = curr + r
            res.append(curr)
        return res

class Chunk:
    def __init__(self, v_chunks: list[VerticalChunk]):
        self.v_chunks = v_chunks
        self.duration_ratio = Ratio(t=(4,4))
        self.h_chunks = [HorizontalChunk() for _ in v_chunks[0].vertical_measures]

        for v_ch in v_chunks:
            for part_no, m in enumerate(v_ch.vertical_measures):
                self.h_chunks[part_no].measures.append(m)

    def to_ruler_bars(self) -> list[list[RulerEvent]]:
        lanes_data2 = [v_ch.ratio_lanes_to_ruler() for v_ch in self.v_chunks]
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

class Ligature():
    def __init__(self, start_note: Note, end_note: Note):
        ...

class LongHObject():
    def __init__(self, start_note: Note, start_offset: Ratio, end_note: Note, end_offset: Ratio):
        ...

class FadeDynamics(LongHObject):
    def __init__(self, start_note, start_offset, end_note, end_offset):
        super().__init__(start_note, start_offset, end_note, end_offset)

class FadeInDynamics(FadeDynamics):
    def __init__(self, start_note, start_offset, end_note, end_offset):
        super().__init__(start_note, start_offset, end_note, end_offset)

class FadeOutDynamics(FadeDynamics):
    def __init__(self, start_note, start_offset, end_note, end_offset):
        super().__init__(start_note, start_offset, end_note, end_offset)

class Legato(LongHObject):
    def __init__(self, start_note, start_offset, end_note, end_offset):
        super().__init__(start_note, start_offset, end_note, end_offset)