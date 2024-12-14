from widgets.compound.stack_panels import VStack


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget


class PartWidget(QWidget):
    def __init__(self, parent=None, flags=None, widget_type: type = None):
        super().__init__(parent, flags or Qt.WindowFlags())
        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        label = QLabel(text="Label", parent=self)
        layout.addWidget(
            VStack(
                margin=(0, 0, 0, 0),
                children=[label],
                fixed_width=100, stretch=False)
            .widget)

        self.staff_widget = widget_type()
        layout.addWidget(self.staff_widget)