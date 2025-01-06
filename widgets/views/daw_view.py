from widgets.basics.my_button import StateButton, SyncButton
from widgets.compound.stack_panels import HStack, VStack
from widgets.compound.stretch import Stretch
from widgets.lanes.RulerWidget import RulerWidget
from widgets.lanes.PartWidget import PartWidget
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

        # ruler_widget = PartWidget(widget_type=RulerWidget)
        # self.layout.addWidget(ruler_widget)

        bottom_panel = HStack(
                    children=
                    [
                        Stretch(),
                        SyncButton("<<", None),
                        SyncButton("<", None),
                        StateButton("PLAY", None, color_hex_off="#334477", color_hex_on="#4477FF"),
                        StateButton("REC", None, color_hex_off="#554422", color_hex_on="#FF5522"),
                        SyncButton("STOP", None),
                        SyncButton(">", None),
                        SyncButton(">>", None),
                    ],
                    stretch=False)
        self.layout.addWidget(bottom_panel.widget)

        self.layout.parentWidget().update()
        self.layout.update()