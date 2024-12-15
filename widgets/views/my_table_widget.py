from typing import Any, Callable
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QFrame, QWidget, QApplication, QTableView, QVBoxLayout, QWidget, QTableWidget, QHeaderView, QSizePolicy, QTableWidgetItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from model.piece import generate_sample_piece
from utils.file_utils.fs_model import DirModel, FsItem
from widgets.basics.button_delegate import ButtonDelegate
from widgets.compound.stack_panels import HStack, VStack
from widgets.basics.my_button import SyncButton
from widgets.musical.PartWidget import PartWidget
from widgets.basics.text_box import TextBox

def finish_path(fsItem: FsItem):
    if isinstance(fsItem, DirModel):
        return fsItem.rel_path + "/"
    else:
        return fsItem.rel_path




class MyTableView(QWidget):
    def __init__(self, 
                 columns: list[tuple[str, int, bool]], 
                 get_data_func: Callable[[], list[list[Any]]], 
                 on_selection_changed: Callable[[Any, Any], None]):
        """MyTableView

        Args:
            columns (list[tuple[str, int, bool]]): list of tuples of name, width, editable.
            get_data_func (Callable[[], list[list[Any]]]): func to retrieve list of data (list of lists)
        """
        super().__init__()
        self.get_data_func = get_data_func
        self.columns = columns
            
        
        
        
        self.table_widget = QTableWidget(self)
        self.table_widget.setHorizontalHeaderLabels([c[0] for c in columns])
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows) 
        self.table_widget.selectionModel().selectionChanged.connect(on_selection_changed)
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.cellClicked.connect(self.on_cell_clicked)
        self.table_widget.cellDoubleClicked.connect(self.on_cell_double_clicked)
        
        n_cols = len(self.columns)
        self.table_widget.setColumnCount(n_cols)
        
        for idx, col_no in enumerate(columns):
            self.table_widget.setColumnWidth(idx, col_no[1])  
            
        self.refresh_view()
    
        layout = QVBoxLayout(self)

        layout.addWidget(self.table_widget)
    
    def refresh_view(self):
        data = self.get_data_func()
        self.data = data
        n_rows = len(self.data)
        self.table_widget.setRowCount(n_rows)
        n_cols = len(self.columns)
        for idx, row in enumerate(data):
            for col_no in range(n_cols):
                item = QTableWidgetItem(str(row[col_no]))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(idx, col_no, item)
        
    def on_cell_clicked(self, row_idx, column_idx):
        click_func = self.columns[column_idx][3]
        if click_func:
            row_data = self.data[row_idx]
            click_func(row_data, row_idx)
        
    def on_cell_double_clicked(self, row_idx, column_idx):
        double_click_func = self.columns[column_idx][4]
        if double_click_func:
            row_data = self.data[row_idx]
            double_click_func(row_data, row_idx)
        

            
        