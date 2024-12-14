from typing import override
import sys
from PyQt5.QtWidgets import QApplication, QTableView, QVBoxLayout, QWidget, QPushButton, QMessageBox, QStyledItemDelegate
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal, QObject, QRect, QLocale

# Custom delegate to add a button
class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)


    @override
    def editorEvent(self, event, model, option, index):
        res = super().editorEvent(event, model, option, index)
        return res
    
    @override
    def createEditor(self, parent, option, index):
        button = QPushButton("Click", parent)
        button.clicked.connect(self.button_clicked)
        row_no = index.row() 
        model = index.model()
        data = index.model().data(index)
        print("BUTTON CREATED")
        return button
    

    
    @override
    def setEditorData(self, editor, index):
        pass

    @override
    def setModelData(self, editor, model, index):
        pass
 
    @override
    def paint(self, painter, option, index):
        if index.column() == 2:  # For example, only show button in the 3rd column
            button_rect = QRect(option.rect)
            painter.fillRect(button_rect, option.palette.base())
            button = QPushButton("Click")
            button.setGeometry(button_rect)
            button.render(painter)
        else:
            super().paint(painter, option, index)


    def button_clicked(self):
        print("Button clicked!")
