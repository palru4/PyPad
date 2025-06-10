import customtkinter as ctk 
from ui.PyPad_UI import PyPad

if __name__ == "__main__":
    root = ctk.CTk()
    app = PyPad(root)
    root.mainloop()

