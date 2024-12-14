from PyQt5.QtWidgets import QApplication
from widgets.views.filelist_view import FileListView
from widgets.views.daw_view import DawView
from widgets.views.score_view import ScoreView
from widgets.base_window import MyStyledWindow
from widgets.compound.base_compound import MyCompound
from widgets.compound.stack_panels import HStack, VStack
from widgets.compound.stretch import Stretch
from widgets.basics.my_button import AsyncButton, SyncButton
import wirings.layouts.general as general

     
class MainWindow(MyStyledWindow):
    def __init__(self):
        super().__init__()
        self.set_central(ScoreView())
    

    def load_piece(self):
        self.set_central(ScoreView())
            
    def load_daw(self):
        self.set_central(DawView())
        
    def load_file_view(self):
        self.set_central(FileListView())
        
    def close_app(self):
        QApplication.quit()
        super().close()
        
    def set_central(self, compound: MyCompound):

        central_v_stack = VStack(
            children=
            [
                HStack(
                    children=
                    [
                        SyncButton("load piece", self.load_piece), 
                        SyncButton("load DAW", self.load_daw),
                        SyncButton("load file view", self.load_file_view), 
                        SyncButton("CLOSE APP", self.close_app)
                    ]), 
                HStack(
                    children=
                    [
                        VStack(fixed_width=120, children=general.get_left_pane_buttons(), stretch=True), 
                        compound
                    ], 
                    stretch=False),
                HStack(
                    children=
                    [
                        SyncButton("PLAY", None), 
                        SyncButton("STOP", None)
                    ]),
                ],
            stretch=False)

        self.setCentralWidget(central_v_stack.widget)
            