from PyQt5.QtWidgets import (
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import os

class LoadDirThread(QThread):
    update_items = pyqtSignal(list)

    def __init__(self, parent_path):
        super().__init__()
        self.parent_path = parent_path

    def run(self):
        try:
            items = sorted(
                os.listdir(self.parent_path),
                key=lambda x: (not os.path.isdir(os.path.join(self.parent_path, x)), x.lower())
            )
            nodes = []
            for name in items:
                full_path = os.path.join(self.parent_path, name)
                is_dir = os.path.isdir(full_path)
                display_name = f"📁 {name}" if is_dir else f"📄 {name}"
                nodes.append((display_name, full_path, is_dir))
            self.update_items.emit(nodes)
        except Exception as e:
            print("Error loading directory:", e)

class FileExplorerQt(QWidget):
    def __init__(self, parent=None, open_file_callback=None):
        super().__init__(parent)
        self.open_file_callback = open_file_callback
        self._threads = []

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemExpanded.connect(self.on_expand)
        self.tree.itemClicked.connect(self.on_click)
        layout.addWidget(self.tree)

    def load_directory(self, folder_path):
        self.tree.clear()

        root_name = f"📁 {os.path.basename(folder_path)}"
        root_item = QTreeWidgetItem([root_name])
        root_item.setData(0, Qt.UserRole, folder_path)  # lưu path
        self.tree.addTopLevelItem(root_item)

        # add dummy child để lazy load
        dummy = QTreeWidgetItem(["dummy"])
        root_item.addChild(dummy)

    def on_expand(self, item):
        path = item.data(0, Qt.UserRole)
        if not path or not os.path.isdir(path):
            return

        # lazy load
        if item.childCount() == 1 and item.child(0).text(0) == "dummy":
            item.takeChild(0)  # remove dummy
            thread = LoadDirThread(path)
            thread.update_items.connect(lambda nodes, parent=item: self._insert_nodes(parent, nodes))
            thread.finished.connect(lambda: self._threads.remove(thread))
            self._threads.append(thread)
            thread.start()

    def _insert_nodes(self, parent, nodes):
        for display_name, full_path, is_dir in nodes:
            child = QTreeWidgetItem([display_name])
            child.setData(0, Qt.UserRole, full_path)  # lưu path
            parent.addChild(child)
            if is_dir:
                dummy = QTreeWidgetItem(["dummy"])
                child.addChild(dummy)

    def on_click(self, item, column):
        path = item.data(0, Qt.UserRole)
        if path and os.path.isfile(path) and self.open_file_callback:
            self.open_file_callback(path)

    def set_theme(self, dark_mode):
        if dark_mode:
            self.setStyleSheet("""
                QTreeWidget { background-color: #2d2d2d; color: #d4d4d4; }
                QTreeWidget::item:selected { background-color: #3e598b; color: white; }
            """)
        else:
            self.setStyleSheet("""
                QTreeWidget { background-color: white; color: black; }
                QTreeWidget::item:selected { background-color: #cce8ff; color: black; }
            """)
