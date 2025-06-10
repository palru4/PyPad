import os
import tkinter as tk
import customtkinter as ctk

class FileExplorer(ctk.CTkFrame):
    def __init__(self, master, open_file_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.open_file_callback = open_file_callback
        self.file_paths = []

        self.listbox = tk.Listbox(self, selectmode="browse", activestyle="none")
        self.listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

    def load_directory(self, folder_path):
        self.file_paths.clear()
        self.listbox.delete(0, tk.END)

        for root, dirs, files in os.walk(folder_path):
            for f in files:
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, folder_path)
                self.file_paths.append(abs_path)
                self.listbox.insert(tk.END, rel_path)
            break  # Chỉ hiển thị thư mục gốc

    def on_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            file_path = self.file_paths[index]
            self.open_file_callback(file_path)

    def set_theme(self, dark_mode):
        if dark_mode:
            bg = "#2a2a2a"
            fg = "#eeeeee"
        else:
            bg = "#f0f0f0"
            fg = "#111111"

        self.listbox.configure(
            bg=bg,
            fg=fg,
            selectbackground="#5555ff",
            selectforeground="#ffffff",
            highlightthickness=0,
            bd=0
        )
