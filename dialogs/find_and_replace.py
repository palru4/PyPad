import tkinter as tk
from tkinter import messagebox

class FindReplaceDialog:
    def __init__(self, parent):
        self.parent = parent
        self.text_area = parent.text_area

        # Create a non-modal Toplevel window
        self.root = tk.Toplevel(parent.root)
        self.root.title("Find & Replace")
        self.root.resizable(False, False)
        # Hide window on close instead of destroying it
        self.root.protocol("WM_DELETE_WINDOW", self.hide)
        
        # Variables for checkboxes
        self.match_case_var = tk.BooleanVar()
        self.wrap_around_var = tk.BooleanVar(value=True)

        self._create_widgets()
        
        # Hide initially
        self.root.withdraw()

    def _create_widgets(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # --- Find and Replace entries ---
        tk.Label(main_frame, text="Find what:").grid(row=0, column=0, sticky="w", pady=2)
        self.find_entry = tk.Entry(main_frame, width=40)
        self.find_entry.grid(row=0, column=1, columnspan=2, pady=2, padx=5)

        tk.Label(main_frame, text="Replace with:").grid(row=1, column=0, sticky="w", pady=2)
        self.replace_entry = tk.Entry(main_frame, width=40)
        self.replace_entry.grid(row=1, column=1, columnspan=2, pady=2, padx=5)

        # --- Checkboxes for options ---
        checkbox_frame = tk.Frame(main_frame)
        checkbox_frame.grid(row=2, column=0, columnspan=3, pady=5, sticky='w')
        tk.Checkbutton(checkbox_frame, text="Match case", variable=self.match_case_var).pack(side="left")
        tk.Checkbutton(checkbox_frame, text="Wrap around", variable=self.wrap_around_var).pack(side="left", padx=10)

        # --- Buttons ---
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        tk.Button(button_frame, text="Find Next", command=self.find_next, width=12).pack(side="left", padx=5)
        tk.Button(button_frame, text="Replace", command=self.replace, width=12).pack(side="left", padx=5)
        tk.Button(button_frame, text="Replace All", command=self.replace_all, width=12).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cancel", command=self.hide, width=12).pack(side="left", padx=5)

        # Configure tag for highlighting found text
        self.text_area.tag_configure("found", background="yellow", foreground="black")

    def find_next(self, start_index=None):
        self.text_area.tag_remove("found", "1.0", tk.END)
        
        find_text = self.find_entry.get()
        if not find_text:
            return

        nocase = not self.match_case_var.get()
        start_pos = start_index or self.text_area.index(tk.INSERT)
        
        pos = self.text_area.search(find_text, start_pos, stopindex=tk.END, nocase=nocase)

        if not pos and self.wrap_around_var.get():
            # If not found and wrap is enabled, search from the beginning
            pos = self.text_area.search(find_text, "1.0", stopindex=tk.END, nocase=nocase)

        if pos:
            end_pos = f"{pos}+{len(find_text)}c"
            self.text_area.tag_add("found", pos, end_pos)
            self.text_area.mark_set(tk.INSERT, end_pos)
            self.text_area.see(tk.INSERT)
            self.text_area.focus_set()
            return True
        else:
            messagebox.showinfo("Not Found", f"Cannot find '{find_text}'", parent=self.root)
            return False

    def replace(self):
        # Check if "found" tag exists (i.e., text is highlighted)
        if not self.text_area.tag_ranges("found"):
            self.find_next()
            return

        replace_text = self.replace_entry.get()
        
        # Get position of the found tag
        start_pos, end_pos = self.text_area.tag_ranges("found")
        
        # Replace the text
        self.text_area.delete(start_pos, end_pos)
        self.text_area.insert(start_pos, replace_text)
        
        # Find the next occurrence
        self.find_next(start_index=f"{start_pos}+{len(replace_text)}c")

    def replace_all(self):
        find_text = self.find_entry.get()
        replace_text = self.replace_entry.get()

        if not find_text:
            return
            
        content = self.text_area.get("1.0", tk.END)
        nocase = not self.match_case_var.get()

        if nocase:
            new_content = content.lower().replace(find_text.lower(), replace_text)
            count = content.lower().count(find_text.lower())
        else:
            new_content = content.replace(find_text, replace_text)
            count = content.count(find_text)

        if count > 0:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", new_content)
            messagebox.showinfo("Replace All", f"Replaced {count} occurrence(s).", parent=self.root)
        else:
            messagebox.showinfo("Not Found", f"Cannot find '{find_text}'", parent=self.root)

    def show(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_set()
        self.find_entry.focus_set()
        self.find_entry.select_range(0, tk.END)
        
    def hide(self):
        # Remove highlight when closing the dialog
        self.text_area.tag_remove("found", "1.0", tk.END)
        self.root.withdraw()