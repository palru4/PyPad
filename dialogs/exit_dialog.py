from tkinter import messagebox
from ui.notepad_ui import *

def on_exit(root):
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()
