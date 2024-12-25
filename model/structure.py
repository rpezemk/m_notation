import random
from typing import Any
from PyQt5.QtGui import QColor
from model.RulerBar import RulerBar, RulerEvent
from model.duration import Duration
from model.Ratio import Ratio

    
class TimeHolder():
    def __init__(self, duration: Duration = None, measure: 'Measure' = None):
        self.duration = duration if duration is not None else Duration.QUARTER
        self.measure = measure
        self.offset_ratio = Ratio(t=(0, 1))
        
class Rest(TimeHolder):
    def __init__(self, duration: Duration = None, measure: 'Measure' = None):
        self.duration = duration if duration is not None else Duration.QUARTER
        self.measure = measure

class Triplet(TimeHolder):
    def __init__(self, duration: Duration = None, measure: 'Measure' = None, notes: list[TimeHolder]=None, parent=None):
        self.duration = duration if duration is not None else Duration.QUARTER
        self.notes = notes if notes is not None else []
        self.measure = measure
    
class Note():
    def __init__(self, time, pitch, duration = None, measure: 'Measure' = None):
        self.duration = duration if duration is not None else Duration.QUARTER
        self.measure = measure
        self.time = time
        self.__pitch = pitch
        
    def set_pitch(self, p):
        self.__pitch = p
        # self.assure_pitch()
    
    def get_pitch(self):
        res = self.__pitch
        # self.assure_pitch()
        return self.__pitch
    
    def assure_pitch(self):
        if -100 <= self.__pitch <= 100:
            pass
        else:
            abdfsdf = 234
          
                
class Measure():
    def __init__(self, notes: list[TimeHolder]=None, parent=None):
        self.time_holders = [] if notes is None else notes


class Part():
    def __init__(self, measures: list[Measure]=None, piece=None):
        self.piece = piece
        self.measures = [] if measures is None else measures


class TempoMark():
    def __init__(self, bpm: float, bpm_base: Duration, bar_no: int, bar_offset: Ratio):
        self.bar_no = 0
        self.bpm = bpm
        self.bmp_base = bpm_base
        self.bar_no = bar_no
        self.bar_offset = bar_offset


class ConductorPart():
    def __init__(self, initial_tempo_mark: TempoMark):
        self.base_tempo_mark = initial_tempo_mark
        self.tempo_marks: list[TempoMark] = [initial_tempo_mark]
        pass
    
    
class VerticalChunk():
    """model for vertical one-measure length, n-parts height section.
    """
    def __init__(self, one_measure_parts: list[Measure]):
        self.vertical_measures = one_measure_parts



class HorizontalChunk():
    """model for vertical one-measure length, n-parts height section.
    """
    def __init__(self, part: list[Measure] = None):
        self.measures = [] if part is None else part

     
class Chunk:
    def __init__(self, v_chunks: list[VerticalChunk]):
        self.v_chunks = v_chunks
        self.duration_ratio = Ratio(t=(4,4))
        h_chunks = [HorizontalChunk() for _ in v_chunks[0].vertical_measures]
        
        for m_idx, v_ch in enumerate(v_chunks):
            for part_no, m in enumerate(v_ch.vertical_measures):
                h_chunks[part_no].measures.append(m)
                
        self.h_chunks = h_chunks
        
    def to_ruler_bars(self) -> list[RulerBar]:         
        lanes_data2 = [Chunk.ratio_lanes_to_ruler(v_ch) for v_ch in self.v_chunks]
        return lanes_data2
    
    def ratio_lanes_to_ruler(v_ch: VerticalChunk) -> RulerBar:
        lanes = [[th.duration.to_ratio() for th in m.time_holders] for m in v_ch.vertical_measures]
        curr_pos = Ratio(t=(0, 1))
        moving_sum_lanes: list[list[Ratio]] = [Chunk.to_moving_sum(lane) for lane in lanes]
                        
        ruler_events: list[RulerEvent] = []
        while True:
            curr_check: list[Ratio] = []
            mov = [[m for m in mov if m > curr_pos][:1] for mov in moving_sum_lanes]
            if not mov:
                break
            for m in mov:
                if m:
                    curr_check.append(m[0])
            
            ok, idxs, lowest = Ratio.get_lowest(curr_check)
            if not ok:
                break
            ratio: Ratio = lowest - curr_pos
            th = RulerEvent(ratio)
            ruler_events.append(th)
            curr_pos = lowest
            
            
        curr_pos = Ratio(t=(0, 1))
        for m in v_ch.vertical_measures:
            for e_idx, th in list(enumerate(m.time_holders))[:-1]:
                curr_pos += th.duration.to_ratio()
                m.time_holders[e_idx + 1].offset_ratio = curr_pos

        curr_pos = Ratio(t=(0, 1))
        for e_idx, th in list(enumerate(ruler_events))[:-1]:
            curr_pos += th.len_ratio
            ruler_events[e_idx + 1].offset_ratio = curr_pos

        return RulerBar(ruler_events)

    def to_moving_sum(lane: list[Ratio]) -> list[Ratio]:
        curr = Ratio(t=(0, 1))
        res = []
        for r in lane:
            curr = curr + r
            res.append(curr)
        return res
        
        
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
    
    def to_ratio_lanes(self, m_idx, m_count):
        shown_area = self.filter_by_measures(m_idx, m_count)
        lanes_data: list[list[Ratio]] = []
        for p in shown_area:
            new_lane: list[Ratio] = []
            for m in p:
                for th in m.time_holders:
                    new_lane.append(th.duration.to_ratio())
            lanes_data.append(new_lane)
        return lanes_data