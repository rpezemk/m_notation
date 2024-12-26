from model.ratio import Ratio
from model.structure import Measure


class RulerEvent():
    def __init__(self, ratio: Ratio):
        self.len_ratio = ratio
        self.offset_ratio = Ratio(t=(0, 1))
        
class CsEvent():
    def __init__(self, i_no: int, start_offset: float, duration: float):
        pass


class EventTimeGroup():
    def __init__(self):
        self.events: list[CsEvent] = []
        self.offset_ratio = Ratio(t=(0, 1))
        self.len_ratio = Ratio(t=(0, 1))
        
        
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
        curr_pos = Ratio(t=(0, 1))
        moving_sum_lanes: list[tuple[list[Ratio], list[Ratio]]] = [(lane, VerticalChunk.to_moving_sum(lane)) for lane in lanes]
        res2 = [(k[0], k[1]) for idx, k in enumerate(moving_sum_lanes)]
        
        mov_ordered_list = sorted(set([r for bar_ratios in moving_sum_lanes for r in bar_ratios[1]]), key=lambda r: r.to_float())
        ruler_events: list[RulerEvent] = []
        while True:
            curr_check: list[Ratio] = []
            mov = [[m for m in mov[1] if m > curr_pos][:1] for mov in moving_sum_lanes]
            if not mov:
                break
            for m in mov:
                if m:
                    curr_check.append(m[0])

            ok, idxs, lowest = Ratio.get_lowest(curr_check)
            if not ok:
                break
            ratio: Ratio = lowest - curr_pos
            evt = RulerEvent(ratio)
            ruler_events.append(evt)
            curr_pos = lowest


        curr_pos = Ratio(t=(0, 1))
        for m in self.vertical_measures:
            for e_idx, evt in list(enumerate(m.time_holders))[:-1]:
                curr_pos += evt.duration.to_ratio()
                m.time_holders[e_idx + 1].offset_ratio = curr_pos

        curr_pos = Ratio(t=(0, 1))
        for e_idx, evt in list(enumerate(ruler_events))[:-1]:
            curr_pos += evt.len_ratio
            ruler_events[e_idx + 1].offset_ratio = curr_pos

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




