import os
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QFrame, QWidget, QApplication, QTableView, QVBoxLayout, QWidget, QTableWidget, QHeaderView, QSizePolicy, QTableWidgetItem
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
        current_dir = "."
        resolved_path = os.path.abspath(current_dir)
        
        self.current_path = resolved_path
        self.dir_model = DirModel(abs_path=self.current_path)
        ok, self.dir_children = get_tree(self.dir_model)
            
        self.table_widget = QTableWidget(self)
        
        columns = ["rel_path", "ext", "play"]
        data = [[finish_path(fs), fs.ext, fs.sel] for fs in self.dir_children]

        n_rows = len(data)
        n_cols = len(columns)
        self.table_widget.setRowCount(n_rows)
        self.table_widget.setColumnCount(n_cols)
        self.table_widget.setHorizontalHeaderLabels(columns)
        
        for idx, row in enumerate(data):
            for col in range(n_cols):
                item = QTableWidgetItem(str(data[idx][col]))
                self.table_widget.setItem(idx, col, item)

        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout(self)

        self.table_widget.selectionModel().selectionChanged.connect(self.on_selection_changed)

        layout.addWidget(self.table_widget)
    
        
    def on_selection_changed(self, selected, deselected):
            selected_rows = [index.row() for index in self.table_widget.selectedIndexes()]
            print(f"Selected rows: {selected_rows}")
            
            for row in selected_rows:
                # bullshit
                print(row)
                name = self.table_widget.item(row, 0).text()
                age = self.table_widget.item(row, 1).text() 
                city = self.table_widget.item(row, 2).text()
                print(f"Row {row} - Name: {name}, Age: {age}, City: {city}")