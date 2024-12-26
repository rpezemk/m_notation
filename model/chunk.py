from model.ratio import Ratio
from model.structure import Measure


class RulerEvent():
    def __init__(self, len_ratio: Ratio, offset_ratio: Ratio):
        self.len_ratio = len_ratio
        self.offset_ratio = offset_ratio
        self.inner_events = []
        
class CsEvent():
    def __init__(self, i_no: int, start_offset: float, duration: float):
        pass
        
        
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
        lanes = [[th.duration.to_ratio() for th in m.time_holders] for m in self.vertical_measures]
        for v_m in self.vertical_measures:
            curr_pos = Ratio(t=(0, 1))
            for th in v_m.time_holders:
                th.offset_ratio = curr_pos
                curr_pos += th.duration.to_ratio()
        curr_offset = Ratio(t=(0, 1))
        moving_sum_lanes: list[tuple[list[Ratio], list[Ratio]]] = [(lane, VerticalChunk.to_moving_sum(lane)) for lane in lanes]
        res2 = [(k[0], k[1]) for idx, k in enumerate(moving_sum_lanes)]
        
        mov_ordered_list =[Ratio(t=(0, 1)), *sorted(set([r for bar_ratios in moving_sum_lanes for r in bar_ratios[1]]), key=lambda r: r.to_float())]
        ruler_events: list[RulerEvent] = []
         

        for idx, offset_ratio in enumerate(mov_ordered_list[:-1]):
            len_ratio = mov_ordered_list[idx] - offset_ratio
            evt = RulerEvent(len_ratio, offset_ratio)
            ruler_events.append(evt)
        
        for evt in ruler_events:
            this_time_evts = [th for m in self.vertical_measures for th in m.time_holders if th.offset_ratio == evt.offset_ratio]
            evt.inner_events = this_time_evts
        
        return ruler_events

    def to_moving_sum(lane: list[Ratio]) -> list[Ratio]:
        curr = Ratio(t=(0, 1))
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

        for m_idx, v_ch in enumerate(v_chunks):
            for part_no, m in enumerate(v_ch.vertical_measures):
                self.h_chunks[part_no].measures.append(m)

    def to_ruler_bars(self) -> list[list[RulerEvent]]:
        lanes_data2 = [v_ch.ratio_lanes_to_ruler() for v_ch in self.v_chunks]
        return lanes_data2




