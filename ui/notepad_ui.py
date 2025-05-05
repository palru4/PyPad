import tkinter as tk 
from tkinter import filedialog, messagebox, font as tkfont, ttk
from ui.minimap import Minimap
from dialogs.FontDialogWinStyle import FontDialogWinStyle
from features.shortcut_key import bind_shortcuts
from ui.context_menu import setup_context_menu
from dialogs.exit_dialog import on_exit

class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad Python")
        self.root.geometry("800x600")
        root.protocol("WM_DELETE_WINDOW", lambda: on_exit(root))

        self.is_dark_mode = False
        self.auto_save_enabled = False
        self.file_path = None
        self.auto_save_interval_ms = 30000  # 30 giây
        self.current_font = tkfont.Font(family="Arial", size=12)

        self._create_widgets()
        self._create_menu()
        bind_shortcuts(self)
        setup_context_menu(self)
        self._create_status_bar()
        self._apply_light_theme()
        self._start_auto_save()

    def _create_widgets(self):
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(fill="both", expand=True)

        self.text_area = tk.Text(self.text_frame, wrap="word", font=self.current_font)
        self.text_area.pack(side="left", fill="both", expand=True)

        self.minimap = Minimap(self.text_frame, self.text_area)
        self.minimap.pack(side="right", fill="y")

    def _create_menu(self):
        menu_bar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New File", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # View menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        view_menu.add_command(label="Change Font", command=self.change_font)
        menu_bar.add_cascade(label="View", menu=view_menu)

        # Options menu
        self.auto_save_var = tk.BooleanVar(value=self.auto_save_enabled)
        options_menu = tk.Menu(menu_bar, tearoff=0)
        options_menu.add_checkbutton(label="Enable Auto-Save", onvalue=True, offvalue=False,
                                     variable=self.auto_save_var, command=self.toggle_auto_save)
        menu_bar.add_cascade(label="Options", menu=options_menu)

        self.root.config(menu=menu_bar)

    def _create_status_bar(self):
        self.status_bar = tk.Label(self.root, text="Ln 1, Col 1 | Words: 0 | Chars: 0", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")
        self.text_area.bind("<KeyRelease>", self._update_status_bar)
        self.text_area.bind("<ButtonRelease>", self._update_status_bar)
        self._update_status_bar()

    def _update_status_bar(self, event=None):
        try:
            pos = self.text_area.index(tk.INSERT)
            line, col = map(int, pos.split('.'))
            text = self.text_area.get("1.0", "end-1c")
            words = len(text.split())
            chars = len(text)
            self.status_bar.config(text=f"Ln {line}, Col {col + 1} | Words: {words} | Chars: {chars}")
        except:
            self.status_bar.config(text="")

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def delete_selection(self):
        try:
            self.text.delete("sel.first", "sel.last")
        except tk.TclError:
            pass

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("Notepad Python - Untitled")
        self._update_status_bar()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                self.file_path = file_path
                self.root.title(f"Notepad Python - {file_path}")
                self._update_status_bar()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get(1.0, tk.END))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.file_path = file_path
            self.save_file()
            self.root.title(f"Notepad Python - {file_path}")

    def toggle_dark_mode(self):
        if self.is_dark_mode:
            self._apply_light_theme()
        else:
            self._apply_dark_theme()
        self.is_dark_mode = not self.is_dark_mode

    def _apply_dark_theme(self):
        self.text_area.config(bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
        self.root.config(bg="#2d2d2d")
        self.status_bar.config(bg="#2d2d2d", fg="white")
        self.minimap.set_theme(True)


    def _apply_light_theme(self):
        self.text_area.config(bg="white", fg="black", insertbackground="black")
        self.root.config(bg="SystemButtonFace")
        self.status_bar.config(bg="SystemButtonFace", fg="black")
        self.minimap.set_theme(False)


    def toggle_auto_save(self):
        self.auto_save_enabled = self.auto_save_var.get()
        if self.auto_save_enabled and not self.file_path:
            self.save_as_file()

    def _start_auto_save(self):
        if self.auto_save_enabled and self.file_path:
            self.save_file()
        self.root.after(self.auto_save_interval_ms, self._start_auto_save)

    def change_font(self):
        top = tk.Toplevel(self.root)
        top.title("Font")
        top.resizable(False, False)
        top.grab_set()

        fonts = list(tkfont.families())
        fonts.sort()
        styles = ["Regular", "Italic", "Bold", "Bold Italic"]
        sizes = [str(s) for s in range(8, 30, 2)]

        font_var = tk.StringVar(value=self.current_font.actual("family"))
        style_var = tk.StringVar(value="Regular")
        size_var = tk.StringVar(value=str(self.current_font.actual("size")))

        # Font list
        tk.Label(top, text="Font:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        font_listbox = tk.Listbox(top, listvariable=tk.StringVar(value=fonts), height=10, exportselection=False)
        font_listbox.grid(row=1, column=0, padx=5, sticky="nsew")
        font_listbox.bind("<<ListboxSelect>>", lambda e: font_var.set(fonts[font_listbox.curselection()[0]]))
        font_listbox.selection_set(fonts.index(font_var.get()))

        font_scroll = tk.Scrollbar(top, orient="vertical", command=font_listbox.yview)
        font_scroll.grid(row=1, column=1, sticky="ns")
        font_listbox.config(yscrollcommand=font_scroll.set)

        # Style list
        tk.Label(top, text="Font style:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        style_listbox = tk.Listbox(top, listvariable=tk.StringVar(value=styles), height=10, exportselection=False)
        style_listbox.grid(row=1, column=2, padx=5, sticky="nsew")
        style_listbox.bind("<<ListboxSelect>>", lambda e: style_var.set(styles[style_listbox.curselection()[0]]))
        style_listbox.selection_set(0)

        style_scroll = tk.Scrollbar(top, orient="vertical", command=style_listbox.yview)
        style_scroll.grid(row=1, column=3, sticky="ns")
        style_listbox.config(yscrollcommand=style_scroll.set)

        # Size list
        tk.Label(top, text="Size:").grid(row=0, column=4, sticky="w", padx=5, pady=2)
        size_listbox = tk.Listbox(top, listvariable=tk.StringVar(value=sizes), height=10, exportselection=False)
        size_listbox.grid(row=1, column=4, padx=5, sticky="nsew")
        size_listbox.bind("<<ListboxSelect>>", lambda e: size_var.set(sizes[size_listbox.curselection()[0]]))
        size_listbox.selection_set(sizes.index(size_var.get()))

        size_scroll = tk.Scrollbar(top, orient="vertical", command=size_listbox.yview)
        size_scroll.grid(row=1, column=5, sticky="ns")
        size_listbox.config(yscrollcommand=size_scroll.set)

        # Sample
        tk.Label(top, text="Sample").grid(row=2, column=0, columnspan=5, sticky="w", padx=5, pady=(10, 2))
        sample_label = tk.Label(top, text="AaBbYyZz", relief="solid", width=20, height=3)
        sample_label.grid(row=3, column=0, columnspan=6, padx=5, pady=5)

        def update_sample(*args):
            weight = "bold" if "Bold" in style_var.get() else "normal"
            slant = "italic" if "Italic" in style_var.get() else "roman"
            sample_font = tkfont.Font(family=font_var.get(), size=int(size_var.get()), weight=weight, slant=slant)
            sample_label.config(font=sample_font)

        font_var.trace_add("write", update_sample)
        style_var.trace_add("write", update_sample)
        size_var.trace_add("write", update_sample)
        update_sample()

        # OK & Cancel buttons
        def apply_and_close():
            weight = "bold" if "Bold" in style_var.get() else "normal"
            slant = "italic" if "Italic" in style_var.get() else "roman"
            self.current_font.config(family=font_var.get(), size=int(size_var.get()), weight=weight, slant=slant)
            top.destroy()

        tk.Button(top, text="OK", width=10, command=apply_and_close).grid(row=4, column=4, pady=10, sticky="e")
        tk.Button(top, text="Cancel", width=10, command=top.destroy).grid(row=4, column=5, pady=10, sticky="w")

        top.columnconfigure(0, weight=1)
        top.columnconfigure(2, weight=1)
        top.columnconfigure(4, weight=1)


    def apply_font(self, font_name, size):
        self.current_font.config(family=font_name, size=size)

