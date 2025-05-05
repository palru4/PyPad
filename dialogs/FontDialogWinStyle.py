import tkinter as tk
from tkinter import font as tkfont

class FontDialogWinStyle(tk.Toplevel):
    def __init__(self, parent, current_font, apply_callback):
        super().__init__(parent)
        self.title("Font")
        self.resizable(False, False)
        self.apply_callback = apply_callback

        fonts = sorted(list(tkfont.families()))
        sizes = list(range(8, 33))
        styles = ["Regular", "Italic", "Bold", "Bold Italic"]

        self.filtered_fonts = fonts

        # ============ Labels ============
        tk.Label(self, text="Font:").grid(row=1, column=0, padx=10, sticky="w")
        tk.Label(self, text="Font style:").grid(row=1, column=1, padx=10, sticky="w")
        tk.Label(self, text="Size:").grid(row=1, column=2, padx=10, sticky="w")

        # ============ Font List ============
        self.font_listbox = tk.Listbox(self, height=10, exportselection=False)
        font_scroll = tk.Scrollbar(self, command=self.font_listbox.yview)
        self.font_listbox.config(yscrollcommand=font_scroll.set)

        self.font_listbox.grid(row=2, column=0, padx=(10, 0), sticky="nsew")
        font_scroll.grid(row=2, column=0, sticky="nse", padx=(0, 10), pady=5)

        # ============ Style List ============
        self.style_listbox = tk.Listbox(self, height=10, exportselection=False)
        for style in styles:
            self.style_listbox.insert(tk.END, style)
        self.style_listbox.grid(row=2, column=1, padx=10, sticky="nsew")

        # ============ Size List ============
        self.size_listbox = tk.Listbox(self, height=10, exportselection=False)
        for s in sizes:
            self.size_listbox.insert(tk.END, str(s))
        self.size_listbox.grid(row=2, column=2, padx=10, sticky="nsew")

        # ============ Sample ============
        tk.Label(self, text="Sample:").grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        self.sample_label = tk.Label(self, text="AaBbYyZz", relief="sunken", width=30, height=2)
        self.sample_label.grid(row=4, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="we")

        # ============ Buttons ============
        button_frame = tk.Frame(self)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        tk.Button(button_frame, text="OK", width=8, command=self.on_ok).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cancel", width=8, command=self.destroy).pack(side="left", padx=5)

        # Load fonts
        self.load_fonts(fonts)

        # Current selection
        current_family = current_font.cget("family")
        current_size = current_font.cget("size")
        current_weight = current_font.cget("weight")
        current_slant = current_font.cget("slant")

        # Font
        if current_family in fonts:
            index = fonts.index(current_family)
            self.font_listbox.select_set(index)
            self.font_listbox.see(index)
        # Size
        if current_size in sizes:
            self.size_listbox.select_set(sizes.index(current_size))
            self.size_listbox.see(sizes.index(current_size))
        # Style
        current_style = "Regular"
        if current_weight == "bold" and current_slant == "italic":
            current_style = "Bold Italic"
        elif current_weight == "bold":
            current_style = "Bold"
        elif current_slant == "italic":
            current_style = "Italic"
        self.style_listbox.select_set(styles.index(current_style))

        self.update_preview_font()

        # Bind
        self.font_listbox.bind("<<ListboxSelect>>", lambda e: self.update_preview_font())
        self.size_listbox.bind("<<ListboxSelect>>", lambda e: self.update_preview_font())
        self.style_listbox.bind("<<ListboxSelect>>", lambda e: self.update_preview_font())

        self.grab_set()

    def load_fonts(self, font_list):
        self.font_listbox.delete(0, tk.END)
        for f in font_list:
            self.font_listbox.insert(tk.END, f)

    def update_font_list(self, *args):
        search_term = self.search_var.get().lower()
        self.filtered_fonts = [f for f in tkfont.families() if search_term in f.lower()]
        self.load_fonts(self.filtered_fonts)

    def update_preview_font(self):
        try:
            font_index = self.font_listbox.curselection()
            size_index = self.size_listbox.curselection()
            style_index = self.style_listbox.curselection()
            if font_index and size_index and style_index:
                font_name = self.font_listbox.get(font_index[0])
                size = int(self.size_listbox.get(size_index[0]))
                style = self.style_listbox.get(style_index[0])

                weight = "bold" if "Bold" in style else "normal"
                slant = "italic" if "Italic" in style else "roman"

                preview_font = tkfont.Font(family=font_name, size=size, weight=weight, slant=slant)
                self.sample_label.config(font=preview_font)
        except Exception:
            pass

    def on_ok(self):
        fonts = self.font_listbox.curselection()
        sizes = self.size_listbox.curselection()
        styles = self.style_listbox.curselection()
        if fonts and sizes and styles:
            font_name = self.font_listbox.get(fonts[0])
            size = int(self.size_listbox.get(sizes[0]))
            style = self.style_listbox.get(styles[0])
            self.apply_callback(font_name, size, style)
        self.destroy()
