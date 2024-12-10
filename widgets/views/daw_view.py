from widgets.compound.stack_panels import VStack
from widgets.note_widget import AudioWidget, PartWidget


class DawView(VStack):
    def __init__(self, margin = None, spacing = None, children = None, black_on_white=False, stretch=False, fixed_width=-1):
        super().__init__(margin, spacing, children, black_on_white, stretch, fixed_width)

        for track_no in range(0, 5):
            part_widget = PartWidget(widget_type=AudioWidget)
            part_widget.staff_widget.set_content(None)
            part_widget.staff_widget.update()
            self.layout.addWidget(part_widget)

        self.layout.addStretch()
        self.layout.parentWidget().update()
        self.layout.update()