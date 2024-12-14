from model.duration import Duration
import math

def duration_to_space(time: float):
    space = math.sqrt(time) 
    return space
    
    
def get_single_ruler(times: list[float]):
    # time_space_list = [(t, duration_to_space(t)) for t in times]
    curr = 0
    res = [0]
    for t in times:
        curr+=t
        res.append(curr)
        
    return res


def map_to(steps: list[float], x0: float, x1: float):
    width = x1 - x0
    res = [v*width + x0 for v in steps]
    return res

def get_ruler_from_list(times_list: list[list[float]]):
    rulers = [get_single_ruler(times) for times in times_list]
    curr_time = 0
    return None