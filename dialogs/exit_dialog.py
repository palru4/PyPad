from PyQt5.QtWidgets import QMessageBox

def on_exit(app):
    reply = QMessageBox.question(
        app.root,
        "Quit",
        "Do you really want to quit?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    if reply == QMessageBox.StandardButton.Yes:
        app.root.close()
