import os
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QFrame, QWidget, QApplication, QTableView, QVBoxLayout, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QSizePolicy
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from model.piece import generate_sample_piece
from widgets.basics.button_delegate import ButtonDelegate
from widgets.compound.stack_panels import HStack, VStack
from widgets.basics.my_button import SyncButton
from widgets.musical.PartWidget import PartWidget
from widgets.basics.text_box import TextBox
from utils.file_utils.fs_model import DirModel, FsItem, get_tree

def finish_path(fsItem: FsItem):
    if isinstance(fsItem, DirModel):
        return fsItem.rel_path + "/"
    else:
        return fsItem.rel_path

class FileListView(QWidget):
    def __init__(self, margin = None, spacing = 0, children = None, stretch=True, fixed_width=-1):
        super().__init__()
        # Set up the table widget
        self.table_widget = QTableWidget(self)

        # Set the number of rows and columns
        self.table_widget.setRowCount(3)
        self.table_widget.setColumnCount(3)

        # Set column headers
        self.table_widget.setHorizontalHeaderLabels(["Name", "Age", "City"])

        # Add data to the table
        data = [
            ["Alice", 30, "New York"],
            ["Bob", 25, "Los Angeles"],
            ["Charlie", 35, "Chicago"]
        ]

        for row in range(3):
            for col in range(3):
                item = QTableWidgetItem(str(data[row][col]))
                self.table_widget.setItem(row, col, item)

        # Set the table to expand and take available space
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout(self)
        # Set up the layout
        self.table_widget.selectionModel().selectionChanged.connect(self.on_selection_changed)

        layout.addWidget(self.table_widget)
    
        
    def on_selection_changed(self, selected, deselected):
            """Method called when the selection changes."""
            # Get the list of selected rows
            selected_rows = [index.row() for index in self.table_widget.selectedIndexes()]

            # You can also print the selected row(s) or perform some other action
            print(f"Selected rows: {selected_rows}")
            
            # Example: Get data from the selected row(s)
            for row in selected_rows:
                name = self.table_widget.item(row, 0).text()  # Get 'Name' column data
                age = self.table_widget.item(row, 1).text()   # Get 'Age' column data
                city = self.table_widget.item(row, 2).text()  # Get 'City' column data
                print(f"Row {row} - Name: {name}, Age: {age}, City: {city}")