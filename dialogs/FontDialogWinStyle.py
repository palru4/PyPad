import tkinter as tk
from tkinter import font as tkfont

class FontDialogWinStyle(tk.Toplevel):
    def __init__(self, parent, current_font, apply_callback):
        super().__init__(parent)
        self.title("Font")
        self.resizable(False, False)
        self.apply_callback = apply_callback  # Use this later if the OK was hit

        # Get available fonts and sort them
        font_names = sorted(list(tkfont.families()))
        common_sizes = list(range(8, 33))  # Most used font sizes
        font_styles = ["Regular", "Italic", "Bold", "Bold Italic"]

        self.filtered_fonts = font_names  # Default to all fonts at first

        # ------- Labels -------
        tk.Label(self, text="Font:").grid(row=1, column=0, padx=10, sticky="w")
        tk.Label(self, text="Font style:").grid(row=1, column=1, padx=10, sticky="w")
        tk.Label(self, text="Size:").grid(row=1, column=2, padx=10, sticky="w")

        # ------- Font List -------
        self.font_listbox = tk.Listbox(self, height=10, exportselection=False)
        self.font_scrollbar = tk.Scrollbar(self, command=self.font_listbox.yview)
        self.font_listbox.config(yscrollcommand=self.font_scrollbar.set)

        self.font_listbox.grid(row=2, column=0, padx=(10, 0), sticky="nsew")
        self.font_scrollbar.grid(row=2, column=0, sticky="nse", padx=(0, 10), pady=5)

        # ------- Style List -------
        self.style_listbox = tk.Listbox(self, height=10, exportselection=False)
        for style in font_styles:
            self.style_listbox.insert(tk.END, style)
        self.style_listbox.grid(row=2, column=1, padx=10, sticky="nsew")

        # ------- Size List -------
        self.size_listbox = tk.Listbox(self, height=10, exportselection=False)
        for size in common_sizes:
            self.size_listbox.insert(tk.END, str(size))
        self.size_listbox.grid(row=2, column=2, padx=10, sticky="nsew")

        # ------- Sample Preview -------
        tk.Label(self, text="Sample:").grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        self.sample_label = tk.Label(self, text="AaBbYyZz", relief="sunken", width=30, height=2)
        self.sample_label.grid(row=4, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="we")

        # ------- Buttons -------
        buttons = tk.Frame(self)
        buttons.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        tk.Button(buttons, text="OK", width=8, command=self.on_ok).pack(side="left", padx=5)
        tk.Button(buttons, text="Cancel", width=8, command=self.destroy).pack(side="left", padx=5)

        # Initial load of font list
        self.load_fonts(font_names)

        # Apply current font selection from the outside input
        try:
            family = current_font.cget("family")
            size = current_font.cget("size")
            weight = current_font.cget("weight")
            slant = current_font.cget("slant")
        except Exception as e:
            # Sometimes fonts get weird, not all info is available
            family, size, weight, slant = "Arial", 12, "normal", "roman"

        if family in font_names:
            idx = font_names.index(family)
            self.font_listbox.select_set(idx)
            self.font_listbox.see(idx)

        if size in common_sizes:
            self.size_listbox.select_set(common_sizes.index(size))
            self.size_listbox.see(common_sizes.index(size))

        if weight == "bold" and slant == "italic":
            selected_style = "Bold Italic"
        elif weight == "bold":
            selected_style = "Bold"
        elif slant == "italic":
            selected_style = "Italic"
        else:
            selected_style = "Regular"

        self.style_listbox.select_set(font_styles.index(selected_style))

        self.update_preview_font()

        # Hooking up listbox changes
        self.font_listbox.bind("<<ListboxSelect>>", lambda e: self.update_preview_font())
        self.size_listbox.bind("<<ListboxSelect>>", lambda e: self.update_preview_font())
        self.style_listbox.bind("<<ListboxSelect>>", lambda e: self.update_preview_font())

        self.grab_set()  # Lock focus to this dialog

    def load_fonts(self, font_list):
        self.font_listbox.delete(0, tk.END)
        for fname in font_list:
            self.font_listbox.insert(tk.END, fname)

    def update_preview_font(self):
        try:
            selected_font = self.font_listbox.curselection()
            selected_size = self.size_listbox.curselection()
            selected_style = self.style_listbox.curselection()

            if selected_font and selected_size and selected_style:
                family = self.font_listbox.get(selected_font[0])
                size = int(self.size_listbox.get(selected_size[0]))
                style = self.style_listbox.get(selected_style[0])

                weight = "bold" if "Bold" in style else "normal"
                slant = "italic" if "Italic" in style else "roman"

                # Apply the font to the preview label
                preview_font = tkfont.Font(family=family, size=size, weight=weight, slant=slant)
                self.sample_label.config(font=preview_font)
        except:
            pass

    def on_ok(self):
        # Pull selected values
        chosen_font = self.font_listbox.curselection()
        chosen_size = self.size_listbox.curselection()
        chosen_style = self.style_listbox.curselection()

        if chosen_font and chosen_size and chosen_style:
            name = self.font_listbox.get(chosen_font[0])
            size = int(self.size_listbox.get(chosen_size[0]))
            style = self.style_listbox.get(chosen_style[0])

            # Send values to parent through the callback
            self.apply_callback(name, size, style)

        self.destroy()
