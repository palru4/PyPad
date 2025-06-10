def bind_shortcuts(app):
    root = app.root  # Lấy cửa sổ chính
    # File
    root.bind("<Control-n>", lambda event: app.new_file())
    root.bind("<Control-o>", lambda event: app.open_file())
    root.bind("<Control-s>", lambda event: app.save_file())
    root.bind("<Control-Shift-S>", lambda event: app.save_file_as())

    # Edit
    root.bind("<Control-x>", lambda event: app.text_area.event_generate("<<Cut>>"))
    root.bind("<Control-c>", lambda event: app.text_area.event_generate("<<Copy>>"))
    root.bind("<Control-v>", lambda event: app.text_area.event_generate("<<Paste>>"))
    root.bind("<Control-z>", lambda event: app.text_area.event_generate("<<Undo>>"))
    root.bind("<Control-y>", lambda event: app.text_area.event_generate("<<Redo>>"))
    root.bind("<Control-a>", lambda event: app.text_area.event_generate("<<SelectAll>>"))
    root.bind("<F5>", lambda event: app.insert_datetime())
    root.bind("<Control-f>", lambda event: app.show_find_dialog()) 

    # Exit
    root.bind("<Control-q>", lambda event: app.on_exit())
