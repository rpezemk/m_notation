import os
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QFrame, QWidget, QApplication, QTableView, QVBoxLayout, QWidget, QTableWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from model.piece import generate_sample_piece
from widgets.compound.stack_panels import HStack, VStack
from widgets.my_button import SyncButton
from widgets.note_widget import PartWidget, StaffWidget
from widgets.text_box import TextBox


class FileListView(VStack):
    def __init__(self, margin = None, spacing = 0, children = None, black_on_white=False, stretch=True, fixed_width=-1):
        super().__init__(margin, spacing, children, black_on_white, False, fixed_width)
        current_dir = "."
        resolved_path = os.path.abspath(current_dir)
        self.current_path = resolved_path
        
        path_box = TextBox("")
        path_box.setText(self.current_path)
        
        self.upper_bar = HStack(fixed_height=40, 
                                children=
                                    [
                                        SyncButton("UP", None), 
                                        path_box
                                    ]
                                )
            
        self.lower_bar = HStack(fixed_height=40, 
                                children=
                                    [
                                        SyncButton("load piece", None), 
                                        SyncButton("load piece", None), 
                                        SyncButton("load piece", None), 
                                    ]
                                )
        
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Name", "Age", "City"])
        self.table_view.setStyleSheet("background-color: black;")
        self.widget.setStyleSheet("""
            QWidget {
                background-color: black;
                color: white;
            }
        """)
        
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
        self.layout.addWidget(self.upper_bar.widget)
        self.layout.addWidget(self.table_view)
        self.layout.addWidget(self.lower_bar.widget)
        
