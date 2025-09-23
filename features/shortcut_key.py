from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

def bind_shortcuts(app):
    # File
    QShortcut(QKeySequence("Ctrl+N"), app, activated=app.new_file)
    QShortcut(QKeySequence("Ctrl+O"), app, activated=app.open_file)
    QShortcut(QKeySequence("Ctrl+S"), app, activated=app.save_file)
    QShortcut(QKeySequence("Ctrl+Shift+S"), app, activated=app.save_as_file)

    # Edit
    QShortcut(QKeySequence("Ctrl+X"), app.text_area, activated=lambda: app.text_area.cut())
    QShortcut(QKeySequence("Ctrl+C"), app.text_area, activated=lambda: app.text_area.copy())
    QShortcut(QKeySequence("Ctrl+V"), app.text_area, activated=lambda: app.text_area.paste())
    QShortcut(QKeySequence("Ctrl+Z"), app.text_area, activated=lambda: app.text_area.undo())
    QShortcut(QKeySequence("Ctrl+Y"), app.text_area, activated=lambda: app.text_area.redo())
    QShortcut(QKeySequence("Ctrl+A"), app.text_area, activated=lambda: app.text_area.selectAll())
    QShortcut(QKeySequence("F5"), app, activated=app.insert_datetime)
    QShortcut(QKeySequence("Ctrl+F"), app, activated=app.show_find_dialog)

    # Exit
    QShortcut(QKeySequence("Ctrl+Q"), app, activated=app.close)
