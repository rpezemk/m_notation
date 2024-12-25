from model.Ratio import Ratio


class RulerEvent():
    def __init__(self, ratio: Ratio):
        self.ratio = ratio
        
        
class RulerBar():
    def __init__(self, ruler_events: list[RulerEvent] = None):
        self.ruler_events = [] if ruler_events is None else ruler_events
        pass