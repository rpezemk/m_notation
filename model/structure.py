import random
from typing import Any
from PyQt5.QtGui import QColor
from model.RulerBar import RulerBar, RulerEvent
from model.duration import Duration
from model.Ratio import Ratio
from utils.musical_layout.precise_aftermath import ratio_lanes_to_ruler

    
    
class TimeHolder():
    def __init__(self, duration: Duration = None, measure: 'Measure' = None):
        self.duration = duration if duration is not None else Duration.QUARTER
        self.measure = measure
    
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
        self.one_measure_parts = one_measure_parts



class HorizontalChunk():
    """model for vertical one-measure length, n-parts height section.
    """
    def __init__(self, part: list[Measure] = None):
        self.measures = [] if part is None else part

     
class Chunk:
    def __init__(self, v_chunks: list[VerticalChunk]):
        self.v_chunks = v_chunks
        self.duration_ratio = Ratio(t=(4,4))
        h_chunks = [HorizontalChunk() for _ in v_chunks[0].one_measure_parts]
        
        for m_idx, v_ch in enumerate(v_chunks):
            for part_no, m in enumerate(v_ch.one_measure_parts):
                h_chunks[part_no].measures.append(m)
                
        self.h_chunks = h_chunks
        
    def to_ruler_bars(self):         
        lanes_data2 =  [
            RulerBar([
                RulerEvent(r) for r in ratio_lanes_to_ruler([[th.duration.to_ratio() for th in m.time_holders] for m in v_ch.one_measure_parts])
                ]) for v_ch in self.v_chunks]
        return lanes_data2
        
        
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