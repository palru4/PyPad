import tkinter as tk

def setup_context_menu(app):
    menu = tk.Menu(app.root, tearoff=0)
    menu.add_command(label="Cut", command=lambda: app.text_area.event_generate("<<Cut>>"))
    menu.add_command(label="Copy", command=lambda: app.text_area.event_generate("<<Copy>>"))
    menu.add_command(label="Paste", command=lambda: app.text_area.event_generate("<<Paste>>"))
    menu.add_command(label="Select All", command=lambda: app.text_area.event_generate("<<SelectAll>>"))

    def show_context_menu(event):
        menu.tk_popup(event.x_root, event.y_root)

    app.text_area.bind("<Button-3>", show_context_menu)
