from PyQt5.QtWidgets import QWidget

class MyCompound():
    def __init__(self, t: type, margin: tuple|list = None, spacing: int=None, children: list['MyCompound'] = None, stretch=False,
                 black_on_white=False
                 ):
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color: black;")
        self.layout = t(self.widget)
        if spacing is not None:
            self.layout.setSpacing(spacing)
        if children is not None:
            for c in children:
                if isinstance(c, MyCompound):
                    self.layout.addWidget(c.widget)
                elif isinstance(c, QWidget):
                    self.layout.addWidget(c)
        if stretch:
            self.layout.addStretch()   
        if margin is not None:
            self.layout.setContentsMargins(*margin)
        if black_on_white:
            self.widget.setStyleSheet("background-color: lightgray; border-right: 1px solid black;")

        
    def add_widgets(self, widgets: list[QWidget]):
        for w in widgets:
            self.layout.addWidget(w)
        return self
            
