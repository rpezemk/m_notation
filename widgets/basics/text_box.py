from typing import Callable
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QLineEdit
from PyQt5.QtGui import QFont

class TextBox(QTextEdit):
    def __init__(self, txt: str = "", read_only: bool = False, set_fixed_height = -1):
        super().__init__(txt)
        self.txt = txt
        if set_fixed_height > 0:
            self.setFixedHeight(set_fixed_height)
        else:
            self.setFixedHeight(40)
        font = QFont("Courier New")
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        if read_only:
            self.setReadOnly(True)

    def append_text(self, txt: str = ""):
        self.txt += f"{txt}"
        self.setText(self.txt)
        self.moveCursor(self.textCursor().End)
        self.ensureCursorVisible()

    def append_log(self, txt: str = ""):
        self.txt += f"\n{txt}"
        self.setText(self.txt)
        self.moveCursor(self.textCursor().End)
        self.ensureCursorVisible()


class LineBox(QLineEdit):
    def __init__(self, txt: str = "", read_only: bool = False, set_fixed_height = -1, validation_func: Callable[[str], bool] = None, on_validate_ok: Callable[[str], None] = None):
        super().__init__(txt)
        self.txt = txt
        self.setText(txt)
        self.old_text = self.text()

        self.validation_func = validation_func
        self.on_validate_ok = on_validate_ok

        self.editingFinished.connect(self.on_editing_finished)
        self.focusInEvent = self.on_focus_in
        if set_fixed_height > 0:
            self.setFixedHeight(set_fixed_height)
        else:
            self.setFixedHeight(40)
        font = QFont("Courier New")
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        if read_only:
            self.setReadOnly(True)

    def on_focus_in(self, event):
        self.old_text = self.text()
        """Handle when editing starts (focuses on QLineEdit)."""
        print("Editing started!")
        super().focusInEvent(event)  # Ensure the default behavior is preserved

    def on_editing_finished(self):
        """Handle editing finished event."""
        new_text = self.text()

        if self.validation_func:
            if self.validation_func(new_text):
                self.txt = new_text
                self.setText(new_text)
                if self.on_validate_ok:
                    self.on_validate_ok(new_text)
            else:
                self.txt = self.old_text
                self.setText(self.old_text)
            ...
        else:
            self.setText(new_text)
            self.old_text = new_text
            if self.on_validate_ok:
                self.on_validate_ok(new_text)

        print(self)
        print(f"Editing finished: {new_text}")