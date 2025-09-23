from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QCheckBox, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt

class FindReplaceDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.text_area = parent.text_area  # QTextEdit của PyPadQt

        self.setWindowTitle("Find & Replace")
        self.setModal(False)
        self.resize(400, 150)

        # --- Widgets ---
        self.find_label = QLabel("Find what:")
        self.find_entry = QLineEdit()
        self.replace_label = QLabel("Replace with:")
        self.replace_entry = QLineEdit()

        self.match_case_cb = QCheckBox("Match case")
        self.wrap_around_cb = QCheckBox("Wrap around")
        self.wrap_around_cb.setChecked(True)

        self.find_next_btn = QPushButton("Find Next")
        self.replace_btn = QPushButton("Replace")
        self.replace_all_btn = QPushButton("Replace All")
        self.cancel_btn = QPushButton("Cancel")

        # --- Layout ---
        grid = QGridLayout()
        grid.addWidget(self.find_label, 0, 0)
        grid.addWidget(self.find_entry, 0, 1, 1, 3)
        grid.addWidget(self.replace_label, 1, 0)
        grid.addWidget(self.replace_entry, 1, 1, 1, 3)
        grid.addWidget(self.match_case_cb, 2, 0)
        grid.addWidget(self.wrap_around_cb, 2, 1)
        grid.addWidget(self.find_next_btn, 3, 0)
        grid.addWidget(self.replace_btn, 3, 1)
        grid.addWidget(self.replace_all_btn, 3, 2)
        grid.addWidget(self.cancel_btn, 3, 3)

        self.setLayout(grid)

        # --- Signals ---
        self.find_next_btn.clicked.connect(self.find_next)
        self.replace_btn.clicked.connect(self.replace)
        self.replace_all_btn.clicked.connect(self.replace_all)
        self.cancel_btn.clicked.connect(self.hide)

        # Highlight format
        self.highlight_format = self.text_area.currentCharFormat()
        self.highlight_format.setBackground(Qt.yellow)

    def find_next(self):
        cursor = self.text_area.textCursor()
        find_text = self.find_entry.text()
        if not find_text:
            return

        flags = QTextDocument.FindFlags()
        if self.match_case_cb.isChecked():
            flags |= QTextDocument.FindCaseSensitively

        found = self.text_area.find(find_text, flags)
        if not found and self.wrap_around_cb.isChecked():
            cursor.movePosition(QTextCursor.Start)
            self.text_area.setTextCursor(cursor)
            self.text_area.find(find_text, flags)
        elif not found:
            QMessageBox.information(self, "Not Found", f"Cannot find '{find_text}'")

    def replace(self):
        cursor = self.text_area.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.replace_entry.text())
        self.find_next()

    def replace_all(self):
        find_text = self.find_entry.text()
        replace_text = self.replace_entry.text()
        if not find_text:
            return
        text = self.text_area.toPlainText()
        if self.match_case_cb.isChecked():
            new_text = text.replace(find_text, replace_text)
        else:
            import re
            pattern = re.compile(re.escape(find_text), re.IGNORECASE)
            new_text = pattern.sub(replace_text, text)
        self.text_area.setPlainText(new_text)
