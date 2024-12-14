import os
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QFrame, QWidget, QApplication, QTableView, QVBoxLayout, QWidget, QTableWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from model.piece import generate_sample_piece
from widgets.compound.stack_panels import HStack, VStack
from widgets.basics.my_button import SyncButton
from widgets.musical.PartWidget import PartWidget
from widgets.basics.text_box import TextBox
from utils.file_utils.fs_model import DirModel, get_tree

class FileListView(VStack):
    def __init__(self, margin = None, spacing = 0, children = None, stretch=True, fixed_width=-1):
        super().__init__(margin, spacing, children, False, fixed_width)
        current_dir = "."
        resolved_path = os.path.abspath(current_dir)
        
        self.current_path = resolved_path
        self.dir_model = DirModel(abs_path=self.current_path)
        self.dir_children = get_tree(self.dir_model)
        
        path_box = TextBox("")
        # path_box.setStyleSheet("border: 1px solid white;")
        path_box.setText(self.current_path)
        
                    
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Name", "Age", "City"])
                
        # Add data to the model
        data = [
            ["Alice", 25, "New York"],
            ["Bob", 30, "San Francisco"],
            ["Charlie", 28, "Chicago"],
            ["Diana", 22, "Los Angeles"]
        ]
        for rowData in data:
            items = [QStandardItem(str(value)) for value in rowData]
            self.model.appendRow(items)

        # Attach model to the view
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setStretchLastSection(True)

        # Set layout
        self.upper_bar = HStack(fixed_height=40, children=[SyncButton("UP", None), path_box])
        self.layout.addWidget(self.upper_bar.widget)
        self.layout.addWidget(self.table_view)
        
