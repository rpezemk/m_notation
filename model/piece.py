from model.chunk import Chunk, VerticalChunk
from model.ratio import Ratio
from model.structure import ConductorPart, Part


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