from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)  # Take the first item in the layout
        widget = item.widget()  # Get the widget from the layout item
        if widget is not None:
            widget.deleteLater()  # Schedule it for deletion
        else:
            # If it's a layout, recursively clear it
            sub_layout = item.layout()
            if sub_layout is not None:
                clear_layout(sub_layout)


