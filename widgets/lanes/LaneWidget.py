import fonts.loader


from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget


from typing import Any, override


class LaneWidget(QWidget):
    def __init__(self):
        super().__init__()
        res, self.bravura_font = fonts.loader.try_get_music_font()
        self.dark_gray = QColor(100, 100, 100)
        self.light_gray = QColor(140, 140, 140)
        self.very_light_gray = QColor(160, 160, 160)
        self.light_black = QColor(13, 13, 13)
        self.black = QColor(0, 0, 0)
        self.setFixedHeight(120)

    def set_content(self, data: Any):
        ...

    @override
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    @override
    def paintEvent(self, event):
        super().paintEvent(event)