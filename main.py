import tkinter as tk 
from ui.PyPad_UI import PyPad

if __name__ == "__main__":
    root = tk.Tk()
    app = PyPad(root)
    root.mainloop()
