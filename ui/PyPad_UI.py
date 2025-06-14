import customtkinter as ctk
from customtkinter import CTkFont
import tkinter as tk
from tkinter import filedialog, messagebox, font as tkfont
from dialogs.FontDialogWinStyle import FontDialogWinStyle
from features.syntax_highlight import SyntaxHighlighter
from features.shortcut_key import bind_shortcuts
from ui.context_menu import setup_context_menu
from dialogs.exit_dialog import on_exit
from dialogs.find_and_replace import FindReplaceDialog
from ui.file_explorer import FileExplorer
import os
from datetime import datetime
import threading

class PyPad:
	def __init__(self, root):
		self.root = root
		self.root.title("PyPad")
		self.root.geometry("800x600")
		self.root.protocol("WM_DELETE_WINDOW", lambda: on_exit(root))

		ctk.set_appearance_mode("light")
		ctk.set_default_color_theme("blue")
		self.is_dark_mode = False
		self.auto_save_enabled = False
		self.file_path = None
		self.auto_save_interval_ms = 3000  # 3 giây
		self.current_font = CTkFont(family="Arial", size=12)

		# Khởi tạo trình tô sáng cú pháp
		self.syntax_highlighter = SyntaxHighlighter()

		self.find_dialog = None

		self._create_widgets()          # tạo text + minimap
		self._create_menu()             # tạo menu
		bind_shortcuts(self)           # bind Ctrl+S, Ctrl+F,...
		setup_context_menu(self)       # chuột phải
		self._create_status_bar()      # thanh trạng thái dưới cùng
		self._apply_light_theme()      # thiết lập theme sáng mặc định
		self._start_auto_save()        # bắt đầu tự lưu định kỳ

	def _create_widgets(self):
		self.main_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
		self.main_frame.pack(fill="both", expand=True)

		self.main_frame.grid_rowconfigure(0, weight=1)
		self.main_frame.grid_columnconfigure(0, weight=0)
		self.main_frame.grid_columnconfigure(1, weight=1)
		self.main_frame.grid_columnconfigure(2, weight=0)


		self.explorer_frame = FileExplorer(self.main_frame, self.open_file_from_explorer)
		self.explorer_frame.grid(row=0, column=0, sticky="nsw")

		self.text_area = ctk.CTkTextbox(
			self.main_frame,
			wrap="word",
			font=self.current_font,
			corner_radius=0
		)
		self.text_area.grid(row=0, column=1, sticky="nsew")

		self.text_area.bind("<F5>", self.insert_datetime)

		# Text editor
		self.text_area = ctk.CTkTextbox(
			self.main_frame,
			wrap="word",
			font=self.current_font,
			corner_radius=0
		)
		self.text_area.grid(row=0, column=1, sticky="nsew")

	def insert_datetime(self):
		now=datetime.now()
		formatted=now.strftime("%H:%M %d/%m/%y")
		self.text_area.insert("insert", formatted)
		
	def _create_menu(self):
		menu_bar = tk.Menu(self.root)

		# File menu
		file_menu = tk.Menu(menu_bar, tearoff=0)
		file_menu.add_command(label="New File", command=self.new_file)
		file_menu.add_command(label="Open", command=self.open_file)
		file_menu.add_command(label="Save", command=self.save_file)
		file_menu.add_command(label="Save As", command=self.save_as_file)
		file_menu.add_separator()
		file_menu.add_command(label="Exit", command=lambda: on_exit(self.root))
		file_menu.add_command(label="Open Folder", command=self.open_folder)
		menu_bar.add_cascade(label="File", menu=file_menu)

		# Edit menu
		edit_menu = tk.Menu(menu_bar, tearoff=0)
		edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
		edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
		edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
		edit_menu.add_separator()
		edit_menu.add_command(label="Find & Replace...", command=self.show_find_dialog)
		edit_menu.add_command(label="Date and Time", command=lambda: self.insert_datetime)
		menu_bar.add_cascade(label="Edit", menu=edit_menu)

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
		self.status_bar = ctk.CTkLabel(self.root, text="Ln 1, Col 1 | Words: 0 | Chars: 0", anchor="w")
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
			self.status_bar.configure(text=f"Ln {line}, Col {col + 1} | Words: {words} | Chars: {chars}")
		except:
			self.status_bar.configure(text="")

	def show_context_menu(self, event):
		try:
			self.context_menu.tk_popup(event.x_root, event.y_root)
		finally:
			self.context_menu.grab_release()

	def delete_selection(self):
		try:
			self.text_area.delete("sel.first", "sel.last")
		except tk.TclError:
			pass

	def open_folder(self):
		folder_path = filedialog.askdirectory()
		if folder_path:
			self.explorer_frame.load_directory(folder_path)

	def new_file(self):
		self.text_area.delete(1.0, tk.END)
		self.file_path = None
		self.root.title("PyPad - Untitled")
		self._update_status_bar()

	def open_file(self):
		file_path = filedialog.askopenfilename(filetypes=[
			("Python Files", "*.py *.pyw"),
			("JavaScript Files", "*.js *.jsx"),
			("TypeScript Files", "*.ts *.tsx"),
			("HTML Files", "*.html *.htm *.svelte"),
			("CSS & Preprocessors", "*.css *.scss *.sass *.less"),
			("Java Files", "*.java"),
			("C/C++ Files", "*.c *.h *.cpp *.cc *.cxx *.hpp *.hxx"),
			("C#", "*.cs"),
			("Go", "*.go"),
			("Rust", "*.rs"),
			("Swift", "*.swift"),
			("Kotlin", "*.kt *.kts"),
			("Scala", "*.scala"),
			("Dart", "*.dart"),
			("PHP", "*.php"),
			("R", "*.r"),
			("Ruby", "*.rb"),
			("Perl", "*.pl"),
			("Lua", "*.lua"),
			("Groovy", "*.groovy"),
			("MATLAB/Objective-C", "*.matlab *.m *.mm"),
			("CoffeeScript", "*.coffee"),
			("Config/Data Files", "*.json *.yml *.yaml *.xml *.ini *.toml *.csv *.tsv"),
			("SQL Files", "*.sql *.pgsql *.plsql"),
			("Shell Scripts", "*.sh *.bash *.zsh *.fish *.ps1 *.bat *.cmd"),
			("Markdown & Docs", "*.md *.rst *.tex *.latex *.adoc"),
			("Vue & GraphQL", "*.vue *.graphql"),
			("Docker & Terraform", "*.dockerfile *.docker *.tf *.hcl"),
			("Jenkinsfile", "*.jenkinsfile"),
			("Assembly & Low-level", "*.asm *.s *.diff *.patch *.proto"),
			("Text Files", "*.txt *.log"),
			("All Files", "*.*")
		])
		if file_path:
			self.load_file_content(file_path)

	def open_file_from_explorer(self, file_path):
		if os.path.isfile(file_path):
			self.load_file_content(file_path)

	def load_file_content(self, file_path):
		try:
			with open(file_path, "r", encoding="utf-8") as file:
				content = file.read()

			self.text_area.delete("1.0", tk.END)
			self.text_area.insert("1.0", content)

			self.file_path = file_path
			self.root.title(f"PyPad - {file_path}")

			# Highlight toàn bộ hoặc một phần tùy độ dài
			line_count = int(self.text_area.index("end-1c").split('.')[0])
			if line_count <= 1000 or not hasattr(self.syntax_highlighter, "highlight_partial"):
				self.syntax_highlighter.highlight_syntax(self.text_area._textbox, file_path)
			else:
				self.syntax_highlighter.highlight_partial(self.text_area._textbox, file_path, max_lines=500)

			self._update_status_bar()

		except Exception as e:
			messagebox.showerror("Error", f"Could not open file:\n{e}")


	# def open_file_from_explorer(self, file_path):
	#     if os.path.isfile(file_path):
	#         try:
	#             with open(file_path, "r", encoding="utf-8") as file:
	#                 content = file.read()
	#             self.text_area.delete("1.0", "end")
	#             self.text_area.insert("1.0", content)
	#             self.file_path = file_path
	#             self.root.title(f"PyPad - {file_path}")
	#             self.syntax_highlighter.highlight_syntax(self.text_area._textbox, file_path)
	#             self._update_status_bar()
	#         except Exception as e:
	#             messagebox.showerror("Error", f"Could not open file:\n{e}")



	# def open_file(self):
	#     file_path = filedialog.askopenfilename(filetypes=[
	#         ("Python Files", "*.py *.pyw"),
	#         ("JavaScript Files", "*.js *.jsx"),
	#         ("TypeScript Files", "*.ts *.tsx"),
	#         ("HTML Files", "*.html *.htm *.svelte"),
	#         ("CSS & Preprocessors", "*.css *.scss *.sass *.less"),
	#         ("Java Files", "*.java"),
	#         ("C/C++ Files", "*.c *.h *.cpp *.cc *.cxx *.hpp *.hxx"),
	#         ("C#", "*.cs"),
	#         ("Go", "*.go"),
	#         ("Rust", "*.rs"),
	#         ("Swift", "*.swift"),
	#         ("Kotlin", "*.kt *.kts"),
	#         ("Scala", "*.scala"),
	#         ("Dart", "*.dart"),
	#         ("PHP", "*.php"),
	#         ("R", "*.r"),
	#         ("Ruby", "*.rb"),
	#         ("Perl", "*.pl"),
	#         ("Lua", "*.lua"),
	#         ("Groovy", "*.groovy"),
	#         ("MATLAB/Objective-C", "*.matlab *.m *.mm"),
	#         ("CoffeeScript", "*.coffee"),
	#         ("Config/Data Files", "*.json *.yml *.yaml *.xml *.ini *.toml *.csv *.tsv"),
	#         ("SQL Files", "*.sql *.pgsql *.plsql"),
	#         ("Shell Scripts", "*.sh *.bash *.zsh *.fish *.ps1 *.bat *.cmd"),
	#         ("Markdown & Docs", "*.md *.rst *.tex *.latex *.adoc"),
	#         ("Vue & GraphQL", "*.vue *.graphql"),
	#         ("Docker & Terraform", "*.dockerfile *.docker *.tf *.hcl"),
	#         ("Jenkinsfile", "*.jenkinsfile"),
	#         ("Assembly & Low-level", "*.asm *.s *.diff *.patch *.proto"),
	#         ("Text Files", "*.txt *.log"),
	#         ("All Files", "*.*")
	#     ])
		
	#     if file_path:
	#         try:
	#             with open(file_path, "r", encoding="utf-8") as file:
	#                 content = file.read()
	#                 self.text_area.delete(1.0, tk.END)
	#                 self.text_area.insert(tk.END, content)
					
	#             self.file_path = file_path
	#             self.root.title(f"PyPad - {file_path}")
				
	#             # Apply syntax highlighting
	#             self.syntax_highlighter.highlight_syntax(self.text_area._textbox, file_path)
	#             self._update_status_bar()
	#         except Exception as e:
	#             messagebox.showerror("Error", f"Failed to open file: {e}")

	def save_file(self):
		if self.file_path:
			try:
				with open(self.file_path, "w", encoding="utf-8") as file:
					file.write(self.text_area.get(1.0, tk.END))
				return True
			except Exception as e:
				messagebox.showerror("Error", f"Failed to save file: {e}")
				return False
		else:
			return self.save_as_file()

	def save_as_file(self):
		file_path = filedialog.asksaveasfilename(defaultextension=".txt",
			filetypes=[
				("Python Files", "*.py *.pyw"),
				("JavaScript Files", "*.js *.jsx"),
				("TypeScript Files", "*.ts *.tsx"),
				("HTML Files", "*.html *.htm *.svelte"),
				("CSS & Preprocessors", "*.css *.scss *.sass *.less"),
				("Java Files", "*.java"),
				("C/C++ Files", "*.c *.h *.cpp *.cc *.cxx *.hpp *.hxx"),
				("C#", "*.cs"),
				("Go", "*.go"),
				("Rust", "*.rs"),
				("Swift", "*.swift"),
				("Kotlin", "*.kt *.kts"),
				("Scala", "*.scala"),
				("Dart", "*.dart"),
				("PHP", "*.php"),
				("R", "*.r"),
				("Ruby", "*.rb"),
				("Perl", "*.pl"),
				("Lua", "*.lua"),
				("Groovy", "*.groovy"),
				("MATLAB/Objective-C", "*.matlab *.m *.mm"),
				("CoffeeScript", "*.coffee"),
				("Config/Data Files", "*.json *.yml *.yaml *.xml *.ini *.toml *.csv *.tsv"),
				("SQL Files", "*.sql *.pgsql *.plsql"),
				("Shell Scripts", "*.sh *.bash *.zsh *.fish *.ps1 *.bat *.cmd"),
				("Markdown & Docs", "*.md *.rst *.tex *.latex *.adoc"),
				("Vue & GraphQL", "*.vue *.graphql"),
				("Docker & Terraform", "*.dockerfile *.docker *.tf *.hcl"),
				("Jenkinsfile", "*.jenkinsfile"),
				("Assembly & Low-level", "*.asm *.s *.diff *.patch *.proto"),
				("Text Files", "*.txt *.log"),
				("All Files", "*.*")
			])
			
		if file_path:
			self.file_path = file_path
			if self.save_file():
				self.root.title(f"PyPad - {file_path}")
				# Apply syntax highlighting for the newly saved file
				self.syntax_highlighter.highlight_syntax(self.text_area, file_path)
				return True
		return False

	def show_find_dialog(self):
		if self.find_dialog is None:
			self.find_dialog = FindReplaceDialog(self)
		self.find_dialog.show()


	def toggle_dark_mode(self):
		if self.is_dark_mode:
			self._apply_light_theme()
		else:
			self._apply_dark_theme()
		self.is_dark_mode = not self.is_dark_mode
		
		# Update syntax highlighting colors according to theme
		self.syntax_highlighter.set_theme(self.is_dark_mode)
		if self.file_path:
			self.syntax_highlighter.highlight_syntax(self.text_area._textbox, self.file_path)

	def _apply_dark_theme(self):
		self.text_area.configure(
			bg_color="#1e1e1e",
			fg_color="#1e1e1e",
			text_color="#d4d4d4"
		)
		self.root.configure(bg="#2d2d2d")
		self.status_bar.configure(bg_color="#2d2d2d", text_color="white")
		self.explorer_frame.set_theme(True)
	def _apply_light_theme(self):
		self.text_area.configure(
			bg_color="white",
			fg_color="white",
			text_color="black"
		)
		self.root.configure(bg="#f0f0f0")
		self.status_bar.configure(bg_color="#f0f0f0", text_color="black")
		self.explorer_frame.set_theme(False)
	def toggle_auto_save(self):
		self.auto_save_enabled = self.auto_save_var.get()
		if self.auto_save_enabled and not self.file_path:
			self.save_as_file()

	def _start_auto_save(self):
		if self.auto_save_enabled and self.file_path:
			self.save_file()
		self.root.after(self.auto_save_interval_ms, self._start_auto_save)

	def change_font(self):
		top = ctk.CTkToplevel(self.root)
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
		
		# Set initial selection for the font
		try:
			font_listbox.selection_set(fonts.index(font_var.get()))
		except ValueError:
			font_listbox.selection_set(0)  # Default selection if font not found

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
		
		# Set initial selection for size
		try:
			size_listbox.selection_set(sizes.index(size_var.get()))
		except ValueError:
			size_listbox.selection_set(2)  # Default selection if size not found

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
			self.current_font.configure(family=font_var.get(), size=int(size_var.get()), weight=weight, slant=slant)
			self.text_area.config(font=self.current_font)
			top.destroy()

		tk.Button(top, text="OK", width=10, command=apply_and_close).grid(row=4, column=4, pady=10, sticky="e")
		tk.Button(top, text="Cancel", width=10, command=top.destroy).grid(row=4, column=5, pady=10, sticky="w")

		top.columnconfigure(0, weight=1)
		top.columnconfigure(2, weight=1)
		top.columnconfigure(4, weight=1)

	def apply_font(self, font_name, size):
		self.current_font.config(family=font_name, size=size)
		self.text_area.config(font=self.current_font)