from PyQt5.QtWidgets import (
	QApplication, QWidget, QMainWindow, QTextEdit, QVBoxLayout,
	QHBoxLayout, QLabel, QMenuBar, QMenu, QAction, QFileDialog, QDialog,
	QListWidget, QPushButton, QScrollBar, QComboBox
)
from PyQt5.QtCore import Qt, QTimer, QDateTime, pyqtSignal
from PyQt5.QtGui import QFont, QActionEvent
import sys
import os
from datetime import datetime

# Component
from dialogs.FontDialogWinStyle import FontDialogWinStyle
from features.syntax_highlight import QtSyntaxHighlighter
from features.shortcut_key import bind_shortcuts
from features.hash_menu import create_hash_menu, update_hash_menu_theme
from ui.context_menu import setup_context_menu_qt
from dialogs.exit_dialog import on_exit
from dialogs.find_and_replace import FindReplaceDialog
from ui.file_explorer import FileExplorerQt


class PyPadQt(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("PyPad")
		self.resize(800, 600)

		self.is_dark_mode = False
		self.auto_save_enabled = False
		self.file_path = None
		self.auto_save_interval_ms = 3000
		self.current_font = QFont("Arial", 12)

		self.text_area = QTextEdit()
		self.syntax_highlighter = QtSyntaxHighlighter(self.text_area.document())
		self.find_dialog = None

		self._create_widgets()
		self._create_menu()
		bind_shortcuts(self)
		setup_context_menu_qt(self)
		self._create_status_bar()
		self._apply_light_theme()
		self._start_auto_save()

	def _create_widgets(self):
		central = QWidget()
		self.setCentralWidget(central)
		layout = QHBoxLayout()
		central.setLayout(layout)

		# File explorer
		self.explorer_frame = FileExplorerQt(self, self.open_file_from_explorer)
		layout.addWidget(self.explorer_frame, 1)

		# Text editor
		self.current_font = QFont("Consolas", 12)
		self.text_area.setFont(self.current_font)
		self.text_area.textChanged.connect(self._update_status_bar)
		layout.addWidget(self.text_area, 3)

	def _create_menu(self):
		menu_bar = self.menuBar()

		# File menu
		file_menu = menu_bar.addMenu("File")
		new_action = QAction("New File", self)
		new_action.triggered.connect(self.new_file)
		file_menu.addAction(new_action)

		open_action = QAction("Open", self)
		open_action.triggered.connect(self.open_file)
		file_menu.addAction(open_action)

		save_action = QAction("Save", self)
		save_action.triggered.connect(self.save_file)
		file_menu.addAction(save_action)

		save_as_action = QAction("Save As", self)
		save_as_action.triggered.connect(self.save_as_file)
		file_menu.addAction(save_as_action)

		file_menu.addSeparator()

		exit_action = QAction("Exit", self)
		exit_action.triggered.connect(lambda: on_exit(self))
		file_menu.addAction(exit_action)

		open_folder_action = QAction("Open Folder", self)
		open_folder_action.triggered.connect(self.open_folder)
		file_menu.addAction(open_folder_action)

		# Edit menu
		edit_menu = menu_bar.addMenu("Edit")
		cut_action = QAction("Cut", self)
		cut_action.triggered.connect(self.text_area.cut)
		edit_menu.addAction(cut_action)

		copy_action = QAction("Copy", self)
		copy_action.triggered.connect(self.text_area.copy)
		edit_menu.addAction(copy_action)

		paste_action = QAction("Paste", self)
		paste_action.triggered.connect(self.text_area.paste)
		edit_menu.addAction(paste_action)

		edit_menu.addSeparator()

		find_action = QAction("Find and Replace...", self)
		find_action.triggered.connect(self.show_find_dialog)
		edit_menu.addAction(find_action)

		datetime_action = QAction("Date and Time", self)
		datetime_action.triggered.connect(self.insert_datetime)
		edit_menu.addAction(datetime_action)

		# View menu
		view_menu = menu_bar.addMenu("View")
		dark_mode_action = QAction("Toggle Dark Mode", self)
		dark_mode_action.triggered.connect(self.toggle_dark_mode)
		view_menu.addAction(dark_mode_action)

		font_action = QAction("Change Font", self)
		font_action.triggered.connect(self.change_font)
		view_menu.addAction(font_action)

		# Tools menu
		create_hash_menu(self)

		# Options menu
		options_menu = menu_bar.addMenu("Options")
		self.auto_save_action = QAction("Enable Auto-Save", self, checkable=True)
		self.auto_save_action.triggered.connect(self.toggle_auto_save)
		options_menu.addAction(self.auto_save_action)

	def _create_status_bar(self):
		self.status_bar = self.statusBar()
		self._update_status_bar()

	def _update_status_bar(self):
		cursor = self.text_area.textCursor()
		line = cursor.blockNumber() + 1
		col = cursor.columnNumber() + 1
		text = self.text_area.toPlainText()
		words = len(text.split())
		chars = len(text)
		self.status_bar.showMessage(f"Ln {line}, Col {col} | Words: {words} | Chars: {chars}")

	def insert_datetime(self):
		now = QDateTime.currentDateTime().toString("HH:mm dd/MM/yy")
		self.text_area.insertPlainText(now)
		cursor = self.text_area.textCursor()
		cursor.movePosition(cursor.MoveOperation.End)
		self.text_area.setTextCursor(cursor)

	def open_folder(self):
		folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
		if folder_path:
			self.explorer_frame.load_directory(folder_path)

	def new_file(self):
		self.text_area.clear()
		self.file_path = None
		self.setWindowTitle("PyPad - Untitled")
		self._update_status_bar()

	def open_file(self):
		file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
		if file_path:
			self.load_file_content(file_path)

	def open_file_from_explorer(self, file_path):
		if os.path.isfile(file_path):
			self.load_file_content(file_path)

	def load_file_content(self, file_path):
		try:
			with open(file_path, "r", encoding="utf-8") as f:
				content = f.read()
			self.text_area.setPlainText(content)
			self.file_path = file_path
			self.setWindowTitle(f"PyPad - {file_path}")

			if hasattr(self, "syntax_highlighter") and self.syntax_highlighter is not None:
				self.syntax_highlighter.set_file(file_path)

			self._update_status_bar()
		except Exception as e:
			from PyQt5.QtWidgets import QMessageBox
			QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")

	def save_file(self):
		if self.file_path:
			try:
				with open(self.file_path, "w", encoding="utf-8") as f:
					f.write(self.text_area.toPlainText())
				return True
			except Exception as e:
				from PyQt5.QtWidgets import QMessageBox
				QMessageBox.critical(self, "Error", f"Failed to save file: {e}")
				return False
		else:
			return self.save_as_file()
			
	def save_as_file(self):
		file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "All Files (*.*)")
		if file_path:
			self.file_path = file_path
			if self.save_file():
				self.setWindowTitle(f"PyPad - {file_path}")
				# update highlighter to use new file extension / lexer
				if hasattr(self, "syntax_highlighter") and self.syntax_highlighter is not None:
					self.syntax_highlighter.set_file(file_path)
				return True
		return False

	def show_find_dialog(self):
		if self.find_dialog is None:
			self.find_dialog = FindReplaceDialog(self)
		self.find_dialog.show()

	def toggle_dark_mode(self):
		if self.is_dark_mode:
			self._apply_light_theme()
		else:
			self._apply_dark_theme()

		self.is_dark_mode = not self.is_dark_mode

		# just change theme
		self.syntax_highlighter.set_theme(self.is_dark_mode)

		# If file is opening --> re-highlight it
		if self.file_path:
			self.syntax_highlighter.set_file(self.file_path)

		update_hash_menu_theme(self)

	def _apply_dark_theme(self):
		self.text_area.setStyleSheet("background-color:#1e1e1e; color:#d4d4d4")
		self.status_bar.setStyleSheet("background-color:#2d2d2d; color:white")
		self.explorer_frame.set_theme(True)
		self.centralWidget().setStyleSheet("background-color:#2d2d2d;")

		# menu bar + menu items
		self.menuBar().setStyleSheet("""
			QMenuBar {
				background-color: #2d2d2d;
				color: white;
			}
			QMenuBar::item {
				background: transparent;
				padding: 4px 10px;
			}
			QMenuBar::item:selected {
				background: #444444;   /* hover màu xám đậm */
			}
			QMenu {
				background-color: #2d2d2d;
				color: white;
			}
			QMenu::item:selected {
				background-color: #444444;  /* hover item trong menu */
			}
		""")

	def _apply_light_theme(self):
		self.text_area.setStyleSheet("background-color:white; color:black")
		self.status_bar.setStyleSheet("background-color:#f0f0f0; color:black")
		self.explorer_frame.set_theme(False)
		self.centralWidget().setStyleSheet("background-color:#f0f0f0;")

		self.menuBar().setStyleSheet("""
			QMenuBar {
				background-color: #f0f0f0;
				color: black;
			}
			QMenuBar::item {
				background: transparent;
				padding: 4px 10px;
			}
			QMenuBar::item:selected {
				background: #dcdcdc;  /* hover xám nhạt */
			}
			QMenu {
				background-color: #f0f0f0;
				color: black;
			}
			QMenu::item:selected {
				background-color: #dcdcdc;
			}
		""")



	def toggle_auto_save(self):
		self.auto_save_enabled = self.auto_save_action.isChecked()
		if self.auto_save_enabled and not self.file_path:
			self.save_as_file()

	def _start_auto_save(self):
		if self.auto_save_enabled and self.file_path:
			self.save_file()
		QTimer.singleShot(self.auto_save_interval_ms, self._start_auto_save)

	def change_font(self):
		# Callback to apply when press "OK"
		def apply_font(name, size, style):
			weight = "bold" if "Bold" in style else "normal"
			slant = "italic" if "Italic" in style else "roman"

			font = QFont(name, size)
			font.setWeight(QFont.Bold if weight=="bold" else QFont.Normal)
			font.setItalic(slant=="italic")

			self.text_area.setFont(font)
			self.current_font = font

		# Create dialog with current font and callback
		dialog = FontDialogWinStyle(self, self.current_font, apply_font)
		dialog.show()

