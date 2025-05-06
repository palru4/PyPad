from tkinter import messagebox
from ui.PyPad_UI import *

#Exit confirmation dialog
def on_exit(root):
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()
