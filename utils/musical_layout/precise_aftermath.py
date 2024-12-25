

from model.Ratio import Ratio

def to_moving_sum(lane: list[Ratio]) -> list[Ratio]:
    curr = Ratio(t=(0, 1))
    res = []
    for r in lane:
        curr = curr + r
        res.append(curr)
    return res

def ratio_lanes_to_ruler(lanes: list[list[Ratio]]) -> list[Ratio]:
    curr_pos = Ratio(t=(0, 1))
    moving_sum_lanes = [to_moving_sum(lane) for lane in lanes]        
    widths_ruler = []
    while True:
        curr_check = []
        mov = [[m for m in mov if m > curr_pos][:1] for mov in moving_sum_lanes]
        if not mov:
            break
        for m in mov:
            if m:
                curr_check.append(m[0])
        
        ok, idxs, lowest = Ratio.get_lowest(curr_check)
        if not ok:
            break
        widths_ruler.append(lowest - curr_pos)
        curr_pos = lowest
    return widths_ruler

