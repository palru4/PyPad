import hashlib
import os
from PyQt5.QtWidgets import (
	QAction, QMenu, QFileDialog, QMessageBox,
	QDialog, QVBoxLayout, QCheckBox, QTextEdit,
	QPushButton, QHBoxLayout, QApplication
)


class HashDialog(QDialog):
	def __init__(self, algo_func, parent=None, preset_text=None, preset_results=None):
		super().__init__(parent)
		self.algo_func = algo_func

		self.setWindowTitle(f"Generate {algo_func().name.upper()} digest")
		self.resize(500, 300)

		layout = QVBoxLayout(self)

		self.checkbox = QCheckBox("Treat each line as a separate string")
		layout.addWidget(self.checkbox)

		self.input_edit = QTextEdit()
		layout.addWidget(self.input_edit)

		self.output_edit = QTextEdit()
		self.output_edit.setReadOnly(True)
		layout.addWidget(self.output_edit)

		btn_layout = QHBoxLayout()
		self.copy_btn = QPushButton("Copy to Clipboard")
		self.close_btn = QPushButton("Close")
		btn_layout.addWidget(self.copy_btn)
		btn_layout.addWidget(self.close_btn)
		layout.addLayout(btn_layout)

		self.input_edit.textChanged.connect(self.update_hash)
		self.checkbox.stateChanged.connect(self.update_hash)
		self.copy_btn.clicked.connect(self.copy_to_clipboard)
		self.close_btn.clicked.connect(self.close)

		if preset_text:
			self.input_edit.setPlainText(preset_text)
		if preset_results:
			self.output_edit.setPlainText("\n".join(preset_results))

		if hasattr(parent, "is_dark_mode") and parent.is_dark_mode:
			self.apply_dark_theme()
		else:
			self.apply_light_theme()

	def update_hash(self):
		text = self.input_edit.toPlainText()
		if not text.strip():
			self.output_edit.clear()
			return

		algo = self.algo_func
		results = []
		if self.checkbox.isChecked():
			for line in text.splitlines():
				if line.strip():
					results.append(algo(line.encode()).hexdigest())
		else:
			results.append(algo(text.encode()).hexdigest())

		self.output_edit.setPlainText("\n".join(results))

	def copy_to_clipboard(self):
		QApplication.clipboard().setText(self.output_edit.toPlainText())

	def apply_dark_theme(self):
		self.setStyleSheet("""
			QDialog { background-color: #2d2d2d; color: white; }
			QTextEdit {
				background-color: #1e1e1e;
				color: #d4d4d4;
				border: 1px solid #444444;
				font-family: Consolas, monospace;
				font-size: 12px;
			}
			QPushButton {
				background-color: #3a3a3a;
				color: white;
				border: 1px solid #555555;
				border-radius: 6px;
				padding: 6px 12px;
			}
			QPushButton:hover { background-color: #505050; }
			QPushButton:pressed { background-color: #2d2d2d; }
			QCheckBox { color: white; }
		""")

	def apply_light_theme(self):
		self.setStyleSheet("""
			QDialog { background-color: white; color: black; }
			QTextEdit {
				background-color: #ffffff;
				color: black;
				border: 1px solid #cccccc;
				font-family: Consolas, monospace;
				font-size: 12px;
			}
			QPushButton {
				background-color: #e0e0e0;
				color: black;
				border: 1px solid #a0a0a0;
				border-radius: 6px;
				padding: 6px 12px;
			}
			QPushButton:hover { background-color: #d0d0d0; }
			QPushButton:pressed { background-color: #c0c0c0; }
			QCheckBox { color: black; }
		""")



def create_hash_menu(parent):
	menu_bar = parent.menuBar()
	tools_menu = menu_bar.addMenu("Tools")

	hash_algorithms = {
		"MD5": hashlib.md5,
		"SHA-1": hashlib.sha1,
		"SHA-256": hashlib.sha256,
		"SHA-512": hashlib.sha512,
	}

	for algo_name, algo_func in hash_algorithms.items():
		algo_menu = QMenu(algo_name, parent)

		gen_action = QAction("Generate...", parent)
		gen_action.triggered.connect(lambda checked, a=algo_func: open_hash_dialog_from_text(parent, a))
		algo_menu.addAction(gen_action)

		gen_file_action = QAction("Generate from files...", parent)
		gen_file_action.triggered.connect(lambda checked, a=algo_func: open_hash_dialog_from_files(parent, a))
		algo_menu.addAction(gen_file_action)

		gen_sel_action = QAction("Generate from selection...", parent)
		gen_sel_action.triggered.connect(lambda checked, a=algo_func: open_hash_dialog_from_selection(parent, a))
		algo_menu.addAction(gen_sel_action)

		tools_menu.addMenu(algo_menu)

	update_hash_menu_theme(parent)


def open_hash_dialog_from_text(parent, algo_func):
	dialog = HashDialog(algo_func, parent)
	dialog.exec_()


def open_hash_dialog_from_files(parent, algo_func):
	file_paths, _ = QFileDialog.getOpenFileNames(parent, "Select Files")
	if not file_paths:
		return

	results = []
	for path in file_paths:
		if os.path.isfile(path):
			h = algo_func()
			with open(path, "rb") as f:
				while chunk := f.read(4096):
					h.update(chunk)
			results.append(f"{os.path.basename(path)}: {h.hexdigest()}")

	dialog = HashDialog(algo_func, parent, preset_results=results)
	dialog.exec_()


def open_hash_dialog_from_selection(parent, algo_func):
	text = parent.text_area.textCursor().selectedText()
	if not text:
		return

	dialog = HashDialog(algo_func, parent, preset_text=text)
	dialog.exec_()


def update_hash_menu_theme(parent):
	if not parent:
		return

	for action in parent.menuBar().actions():
		menu = action.menu()
		if not menu:
			continue

		if menu.title() == "Tools":
			for sub_action in menu.actions():
				sub_menu = sub_action.menu()
				if not sub_menu:
					continue

				if sub_menu.title() in ["MD5", "SHA-1", "SHA-256", "SHA-512"]:
					if getattr(parent, "is_dark_mode", False):
						sub_menu.setStyleSheet("""
							QMenu { background-color: #2d2d2d; color: white; }
							QMenu::item:selected { background-color: #444444; }
						""")
					else:
						sub_menu.setStyleSheet("""
							QMenu { background-color: #f0f0f0; color: black; }
							QMenu::item:selected { background-color: #dcdcdc; }
						""")