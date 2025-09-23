import sys
from PyQt5.QtWidgets import QApplication
from ui.PyPad_UI import PyPadQt

if __name__ == "__main__":
	app = QApplication(sys.argv)
	main_window = PyPadQt()
	main_window.show()
	sys.exit(app.exec())
