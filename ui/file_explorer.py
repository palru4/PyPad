import os
import threading
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class FileExplorer(ctk.CTkFrame):
    def __init__(self, master, open_file_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.open_file_callback = open_file_callback
        self.item_paths = {}

        # Container chứa Treeview và Scrollbar
        tree_container = tk.Frame(self)
        tree_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Treeview
        self.tree = ttk.Treeview(tree_container, show="tree")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        # Cấu hình co giãn
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)

        # Bind sự kiện
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<<TreeviewOpen>>", self.on_open_node)

    def load_directory(self, folder_path):
        self.tree.delete(*self.tree.get_children())
        self.item_paths.clear()

        root_display = f"📁 {os.path.basename(folder_path)}"
        root_node = self.tree.insert("", "end", text=root_display, open=False)
        self.item_paths[root_node] = folder_path

        self._add_dummy_node(root_node)  # để hiển thị dấu mở rộng

    def _add_dummy_node(self, node):
        self.tree.insert(node, "end", text="dummy")

    def _load_directory_thread(self, parent_node, parent_path):
        try:
            item = os.listdir(parent_path)
            item.sort(key=lambda x:(not os.path.isdir(os.path.join(parent_path, x)), x.lower()))

            nodes_to_add = []
            for name in item:
                full_path = os.path.join(parent_path, name)
                is_dir = os.path.isdir(full_path)
                display_name = f"📁 {name}" if is_dir else f"📄 {name}"
                nodes_to_add.append((display_name, full_path, is_dir))

            def insert_items():
                for display_name, full_path, is_dir in nodes_to_add:
                    node = self.tree.insert(parent_node, "end", text=display_name, open=False)
                    self.item_paths[node] = full_path
                    if is_dir:
                        self._add_dummy_node(node)

            self.after(0, insert_items)
        except Exception as e:
            print("❌ Error while browsing directory:", e)

    def _insert_directory_contents(self, parent_node, parent_path):
        try:
            items = sorted(os.listdir(parent_path), key=lambda x: (not os.path.isdir(os.path.join(parent_path, x)), x.lower()))
            for name in items:
                full_path = os.path.join(parent_path, name)
                is_dir = os.path.isdir(full_path)
                display_name = f"📁 {name}" if is_dir else f"📄 {name}"

                node = self.tree.insert(parent_node, "end", text=display_name, open=False)
                self.item_paths[node] = full_path

                if is_dir:
                    self._add_dummy_node(node)
        except Exception as e:
            print("Failed to list folder:", e)

    def on_open_node(self, event):
        node = self.tree.focus()
        path = self.item_paths.get(node)
        if not path or not os.path.isdir(path):
            return

        children = self.tree.get_children(node)
        if len(children) == 1 and self.tree.item(children[0], "text") == "dummy":
            self.tree.delete(children[0])
            threading.Thread(target=self._load_directory_thread, args=(node, path), daemon=True).start()

    def on_select(self, event):
        node = self.tree.focus()
        path = self.item_paths.get(node)
        if path and os.path.isfile(path):
            self.open_file_callback(path)

    def set_theme(self, dark_mode):
        style = ttk.Style()
        if dark_mode:
            self.configure(fg_color="#1e1e1e")
            style.theme_use("clam")
            style.configure("Treeview",
                            background="#2d2d2d",
                            foreground="#d4d4d4",
                            fieldbackground="#2d2d2d",
                            rowheight=24,
                            font=("Consolas", 11))
            style.map("Treeview",
                      background=[('selected', '#3e598b')],
                      foreground=[('selected', 'white')])
        else:
            self.configure(fg_color="#f0f0f0")
            style.theme_use("default")
            style.configure("Treeview",
                            background="white",
                            foreground="black",
                            fieldbackground="white",
                            rowheight=24,
                            font=("Consolas", 11))
            style.map("Treeview",
                      background=[('selected', '#cce8ff')],
                      foreground=[('selected', 'black')])
