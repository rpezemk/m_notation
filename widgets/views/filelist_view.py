import os
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QFrame, QWidget, QApplication, QTableView, QVBoxLayout, QWidget, QTableWidget, QHeaderView
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

class FileListView(VStack):
    def __init__(self, margin = None, spacing = 0, children = None, stretch=True, fixed_width=-1):
        super().__init__(margin, spacing, children, False, fixed_width)
        current_dir = "."
        resolved_path = os.path.abspath(current_dir)
        
        self.current_path = resolved_path
        self.dir_model = DirModel(abs_path=self.current_path)
        ok, self.dir_children = get_tree(self.dir_model)
            
        path_box = TextBox("")
        path_box.setText(self.current_path)
          
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["rel_path", "ext", "play"])
        data = [[finish_path(fs), fs.ext, fs.sel] for fs in self.dir_children]

        for rowData in data:
            items = [QStandardItem(str(value)) for value in rowData]
            self.model.appendRow(items)

        self.table_view.setModel(self.model)
        # self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # Dynamic column
        self.table_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)    # Fixed column
        self.table_view.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)          
        self.table_view.setColumnWidth(1, 80)
        self.table_view.setColumnWidth(2, 50)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)  # Select entire rows
                
        self.table_view.setSelectionMode(QTableView.SingleSelection) 
        sel_model = self.table_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.table_view.setItemDelegateForColumn(2, ButtonDelegate())
        # Set layout
        self.upper_bar = HStack(fixed_height=40, children=[SyncButton("UP", None), path_box])
        self.layout.addWidget(self.upper_bar.widget)
        self.layout.addWidget(self.table_view)
        
    def on_selection_changed(self, selected, deselected):
        for s in selected:
            print(f"{s}")
        for d in deselected:
            print(f"{s}")