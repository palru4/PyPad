from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import Qt

def setup_context_menu_qt(app):
    menu = QMenu(app.text_area)
    menu.addAction("Cut", app.text_area.cut)
    menu.addAction("Copy", app.text_area.copy)
    menu.addAction("Paste", app.text_area.paste)
    menu.addAction("Select All", app.text_area.selectAll)

    # Enable custom context menu
    app.text_area.setContextMenuPolicy(Qt.CustomContextMenu)

    def show_context_menu(point):
        menu.exec_(app.text_area.mapToGlobal(point))

    app.text_area.customContextMenuRequested.connect(show_context_menu)
