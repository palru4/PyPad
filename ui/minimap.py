import tkinter as tk
from tkinter import font as tkfont

class Minimap(tk.Canvas):
    def __init__(self, parent, text_widget, **kwargs):
        super().__init__(parent, **kwargs)
        self.text_widget = text_widget
        self.configure(width=100, bg="#1e1e1e", highlightthickness=0)
        self.text_font = tkfont.Font(family="Courier", size=1)  # Rất nhỏ để hiển thị nhiều dòng
        self.text_fg_color = "#cccccc"
        self.vp_fill = "#cccccc"
        self.vp_outline = "#888888"

        self.bind("<Button-1>", self.scroll_to_position)
        self.bind("<B1-Motion>", self.scroll_to_position)

        self.text_widget.bind("<<Modified>>", self.update_minimap)
        self.text_widget.bind("<MouseWheel>", self.sync_scroll)
        self.text_widget.bind("<KeyRelease>", self.update_minimap)

        self.after(100, self.update_minimap)

    def set_theme(self, dark_mode=True):
        if dark_mode:
            # Tông màu đậm hơn editor một chút
            bg_color = "#2a2a2a"      # đậm hơn editor (#1e1e1e)
            fg_color = "#bbbbbb"
            vp_color = "#999999"
            vp_outline = "#666666"
        else:
            bg_color = "#e8e8e8"      # nhẹ hơn trắng, dễ phân biệt
            fg_color = "#444444"
            vp_color = "#aaaaaa"
            vp_outline = "#777777"

        self.configure(bg=bg_color)
        self.text_fg_color = fg_color
        self.vp_fill = vp_color
        self.vp_outline = vp_outline
        self.update_minimap()

    def update_minimap(self, event=None):
        self.delete("all")
        text_content = self.text_widget.get("1.0", "end-1c")
        lines = text_content.splitlines()

        for i, line in enumerate(lines):
            y = i * 2
            self.create_text(2, y, anchor="nw", text=line[:50],
                             font=self.text_font, fill=self.text_fg_color)

        self.draw_viewport()
        self.text_widget.edit_modified(False)

    def draw_viewport(self):
        first, last = self.text_widget.yview()
        height = int(self.text_widget.index("end-1c").split('.')[0]) * 2
        y1 = first * height
        y2 = last * height
        self.create_rectangle(0, y1, self.winfo_width(), y2,
                              fill=self.vp_fill, outline=self.vp_outline)

    def sync_scroll(self, event=None):
        self.after(50, self.update_minimap)

    def scroll_to_position(self, event):
        height = int(self.text_widget.index("end-1c").split('.')[0]) * 2
        y_ratio =_
