from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QSizePolicy

from widgets.compound.stack_panels import VStack


class MyTable(VStack):
    def __init__(self):
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

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        # Window properties
        self.setWindowTitle("Maximized TableWidget")

class MyWindow(QWidget):
    

# Run the application
app = QApplication([])
window = MyWindow()
window.show()
app.exec_()
