from enum import Enum
from widgets.compound.stack_panels import VStack


class View(VStack):
    def __init__(self, margin = None, spacing = None, children = None, stretch=False, fixed_width=-1):
        super().__init__(margin, spacing, children, stretch, fixed_width)
        self.mode = None

    def set_mode(self, mode: Enum):
        self.mode = mode