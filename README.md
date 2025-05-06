# 📝 PyPad

A modern, lightweight Notepad clone built with Python and Tkinter, featuring dark mode, auto-save, multiple tabs, and a sleek Windows-style font dialog.

---

## 🚀 Features

- 🌗 **Dark/Light Theme Toggle**
- 🧠 **Auto-Save** support to prevent data loss
- 🗂️ **Multiple Tabs** with file management
- 🔠 **Windows-Style Font Dialog** with live preview
- 🧾 **Minimap Preview** for code navigation
- 🖱️ **Context Menu** for quick editing actions
- ⌨️ **Keyboard Shortcuts** for faster workflow
- ✅ Clean, structured, and modular codebase

---

## 📁 Project Structure

```
PyPad/
├── main.py                # Entry point of the application
├── .gitignore             # Git ignore file
├── LICENSE                # MIT License
├── README.md              # Project documentation

├── dialogs/               # Dialog-related features
│   ├── exit_dialog.py         # Custom exit confirmation dialog
│   └── FontDialogWinStyle.py  # Custom font picker with preview

├── features/              # Utility and additional features
│   └── shortcut_key.py        # Keyboard shortcut bindings

├── ui/                    # UI components
│   ├── context_menu.py        # Right-click menu
│   ├── minimap.py             # Minimap view for text area
│   ├── PyPad_UI.py            # Main Notepad GUI layout

├── assets/                # Static resources (icons, themes, etc.)
│   └── ...                  

└── .git/                  # Git version control directory
```

---

## 📦 Requirements

- Python 3.10+
- No external dependencies (pure Tkinter)

---

## 🛠️ How to Run

```bash
git clone https://github.com/sundae0/PyPad
cd PyPad
python main.py
```

---

## 🎨 Screenshots

> *(Screenshots will be added here)*

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
