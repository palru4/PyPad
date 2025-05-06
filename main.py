import tkinter as tk 
from tkinter import filedialog, messagebox, font as tkfont, ttk
from ui.PyPad_UI import PyPad
from features.shortcut_key import bind_shortcuts
from dialogs.FontDialogWinStyle import *
from dialogs.exit_dialog import on_exit

if __name__ == "__main__":
    root = tk.Tk()
    app = PyPad(root)
    root.mainloop()
