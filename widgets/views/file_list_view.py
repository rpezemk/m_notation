import os
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QCheckBox, QLabel

from utils.file_utils.fs_model import DirModel, ParentDirModel
from widgets.basics.my_button import SyncButton
from widgets.basics.text_box import LineBox
from widgets.compound.stack_panels import HStack, VStack
from widgets.views.file_table import FileTable


class FileBrowserView(HStack):
    def __init__(self, margin = None, spacing = 0):
        self.line_box = LineBox("abc", validation_func=self.dir_validation_func, on_validate_ok=self.dir_validate_ok)
        self.old_path = self.line_box.text()
        
        self.file_table = FileTable(self.on_path_change)
        self.up_button = SyncButton("UP", sync_click_func=self.dir_up)
        sub_children = [HStack(fixed_height=30, children=[self.up_button, self.line_box], stretch=False), 
                    self.file_table]
        
        left_part = VStack(children=sub_children, stretch=False, fixed_width=600)
        
        
        self.checkbox = QCheckBox("Enable Option")
        self.checkbox.stateChanged.connect(self.on_toggle)  # Connect signal
        
        right_part = VStack(children=[self.checkbox], stretch=True)
        super().__init__(margin, spacing, [left_part, right_part], stretch=False)
        
        
    def on_path_change(self, path: str):
        self.line_box.setText(path)
        print("path changed")
        
    def dir_validation_func(self, txt: str):
        return os.path.exists(txt) and os.path.isdir(txt)
    
    def dir_up(self):
        maybe_parent = [fsi for fsi in self.file_table.dir_children if isinstance(fsi, ParentDirModel)]
        if maybe_parent:
            self.file_table.dir_model = maybe_parent[0]
            self.file_table.refresh_view()
            self.line_box.setText(self.file_table.dir_model.abs_path)
            print("path changed")
            
    def dir_validate_ok(self, txt: str):
        self.file_table.current_path = txt
        self.file_table.dir_model = DirModel(abs_path=txt)
        self.file_table.refresh_view()
    
    def on_toggle(self, state):
        """Handle toggle box state change."""
        if state == 2:  # Checked (Qt.Checked == 2)
            self.checkbox.setText("Toggle box is ON")
        else:  # Unchecked (Qt.Unchecked == 0)
            self.checkbox.setText("Toggle box is OFF")
    
