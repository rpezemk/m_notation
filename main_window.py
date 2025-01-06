from PyQt5.QtWidgets import QApplication
from widgets.views.file_list_view import FileBrowserView
from widgets.views.daw_view import DawView
from widgets.views.score_view import ScoreView
from widgets.base_window import BaseWindow
from widgets.compound.base_compound import MyCompound
from widgets.compound.stack_panels import HStack, VStack
from widgets.compound.stretch import Stretch
from widgets.basics.my_button import AsyncButton, SyncButton
import wirings.layouts.general as general


class MainWindow(BaseWindow):
    def __init__(self):
        self.attached = []
        super().__init__()
        self.set_central(ScoreView())

    def load_piece(self):
        self.set_central(ScoreView())

    def load_daw(self):
        self.set_central(DawView())

    def load_file_view(self):
        self.set_central(FileBrowserView())

    def close_app(self):
        QApplication.quit()
        super().close()

    def set_central(self, compound: MyCompound):
        for att in self.attached:
            att.detach()
        self.attached.append(compound)

        self.root_kbd_resolver.set_view(compound)

        central_v_stack = VStack(
            children=
            [
                HStack(
                    children=
                    [
                        SyncButton("load piece", self.load_piece),
                        SyncButton("load DAW", self.load_daw),
                        SyncButton("FILE BROWSER", self.load_file_view),
                        SyncButton("CLOSE APP", self.close_app)
                    ]),
                HStack(
                    children=
                    [
                        # VStack(fixed_width=120, children=general.get_left_pane_buttons(), stretch=True),
                        compound
                    ],
                    stretch=False),
                ],
            stretch=False)

        self.setCentralWidget(central_v_stack.widget)
