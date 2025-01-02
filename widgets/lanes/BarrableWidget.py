from widgets.lanes.LaneWidget import LaneWidget


class BarrableWidget(LaneWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.measures = []
        self.clef_margin = 30
        self.bar_left_margin = 25
        self.bar_right_margin = 5
        self.x_offsets = None
        self.no_of_measures = 4
        
    def get_h_segments(self):
        l_mar = self.bar_left_margin
        r_mar = self.bar_right_margin
        areas = [self.x_offsets[idx:idx+2] for idx in range(0, len(self.x_offsets)-1)]
        areas_2 = [[a[0] + l_mar, a[1] - r_mar] for a in areas]
        return areas_2
    

    def get_x_offsets(self) -> list[int]:
        av_space = self.width() - self.clef_margin
        if av_space < 10:
            return [0, 10]
        measure_width = int(av_space/self.no_of_measures)
        infos = []
        for i in range(0, self.no_of_measures + 1):
            infos.append(self.clef_margin + measure_width * i)
        self.x_offsets = infos