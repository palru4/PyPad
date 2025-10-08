from PyQt5.QtWidgets import QDialog, QLabel, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QFont, QFontDatabase

class FontDialogWinStyle(QDialog):
    def __init__(self, parent, current_font, apply_callback):
        super().__init__(parent)
        self.setWindowTitle("Font")
        self.setModal(True)
        self.apply_callback = apply_callback
        self.setFixedSize(520, 340)

        # Font list, style list, size list
        self.font_list = QListWidget()
        self.style_list = QListWidget()
        self.size_list = QListWidget()

        font_db = QFontDatabase()
        self.font_names = font_db.families()
        self.font_list.addItems(sorted(self.font_names))

        self.font_styles = ["Regular", "Italic", "Bold", "Bold Italic"]
        self.style_list.addItems(self.font_styles)

        self.font_sizes = [str(i) for i in range(8, 33)]
        self.size_list.addItems(self.font_sizes)

        # Sample preview
        self.sample_label = QLabel("AaBbYyZz")
        self.sample_label.setMinimumHeight(50)
        self.sample_label.setStyleSheet("border: 1px solid gray; padding: 8px;")
        self.sample_label.setFont(current_font)

        # Buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        # Layouts
        # grid = QGridLayout()
        # grid.addWidget(QLabel("Font:"), 0, 0)
        # grid.addWidget(QLabel("Style:"), 0, 1)
        # grid.addWidget(QLabel("Size:"), 0, 2)

        # grid.addWidget(self.font_list, 1, 0)
        # grid.addWidget(self.style_list, 1, 1)
        # grid.addWidget(self.size_list, 1, 2)

        # vbox = QVBoxLayout()
        # vbox.addLayout(grid)
        # vbox.addWidget(QLabel("Sample:"))
        # vbox.addWidget(self.sample_label)

        # hbox = QHBoxLayout()
        # hbox.addWidget(self.ok_button)
        # hbox.addWidget(self.cancel_button)
        # vbox.addLayout(hbox)

        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(6)

        grid.addWidget(QLabel("Font:"), 0, 0)
        grid.addWidget(QLabel("Style:"), 0, 1)
        grid.addWidget(QLabel("Size:"), 0, 2)

        grid.addWidget(self.font_list, 1, 0)
        grid.addWidget(self.style_list, 1, 1)
        grid.addWidget(self.size_list, 1, 2)

        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 1)
        
        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(QLabel("Sample:"))
        vbox.addWidget(self.sample_label)

        hbox = QHBoxLayout()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        vbox.setContentsMargins(10, 10, 10, 10)

        # Select current font
        current_family = current_font.family()
        current_size = str(current_font.pointSize())
        current_weight = "Bold" if current_font.bold() else "Regular"
        current_style = "Italic" if current_font.italic() else "Regular"

        # Set selection
        if current_family in self.font_names:
            self.font_list.setCurrentRow(self.font_names.index(current_family))
        if current_size in self.font_sizes:
            self.size_list.setCurrentRow(self.font_sizes.index(current_size))
        # Determine combined style
        style_name = "Regular"
        if current_font.bold() and current_font.italic():
            style_name = "Bold Italic"
        elif current_font.bold():
            style_name = "Bold"
        elif current_font.italic():
            style_name = "Italic"
        self.style_list.setCurrentRow(self.font_styles.index(style_name))

        # Signals
        self.font_list.currentTextChanged.connect(self.update_preview)
        self.style_list.currentTextChanged.connect(self.update_preview)
        self.size_list.currentTextChanged.connect(self.update_preview)

        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.reject)

        # Initial preview
        self.update_preview()

    def update_preview(self):
        family = self.font_list.currentItem().text() if self.font_list.currentItem() else "Arial"
        size = int(self.size_list.currentItem().text()) if self.size_list.currentItem() else 12
        style = self.style_list.currentItem().text() if self.style_list.currentItem() else "Regular"

        weight = QFont.Bold if "Bold" in style else QFont.Normal
        italic = True if "Italic" in style else False

        font = QFont(family, size, weight)
        font.setItalic(italic)
        self.sample_label.setFont(font)

    def on_ok(self):
        family = self.font_list.currentItem().text()
        size = int(self.size_list.currentItem().text())
        style = self.style_list.currentItem().text()

        self.apply_callback(family, size, style)
        self.accept()
