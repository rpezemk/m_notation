from widgets.compound.stack_panels import VStack
from widgets.lanes.ConductorWidget import ConductorWidget
from widgets.musical.PartWidget import PartWidget
from widgets.lanes.AudioWidget import AudioWidget


class DawView(VStack):
    def __init__(self, margin = None, spacing = None, children = None, stretch=False, fixed_width=-1):
        super().__init__(margin, spacing, children, stretch, fixed_width)

        for track_no in range(0, 5):
            part_widget = PartWidget(widget_type=AudioWidget)
            part_widget.staff_widget.set_content(None)
            part_widget.staff_widget.update()
            self.layout.addWidget(part_widget)
        self.layout.addStretch()
        
        conductor = PartWidget(widget_type=ConductorWidget)
        self.layout.addWidget(conductor)
        self.layout.parentWidget().update()
        self.layout.update()