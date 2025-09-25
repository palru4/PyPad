# 📝 PyPad  
A modern, lightweight Notepad clone built with **Python + PyQt5**, featuring syntax highlighting, dark/light mode, auto-save, multiple tabs, Windows-style dialogs, and extra tools like hashing utilities.

---

## 🚀 Features  

- 🎨 **Syntax Highlighting** for multiple programming languages  
- 🌗 **Dark/Light Theme Toggle** with theme-aware UI and syntax  
- 💾 **Auto-Save** support to prevent data loss  
- 🗂️ **Multiple Tabs** with file management  
- 🔠 **Windows-Style Font Dialog** with live preview  
- 📜 **Minimap Preview** for code navigation  
- 📂 **File Explorer Sidebar** for quick access to files  
- 🖱️ **Context Menu** for editing actions  
- 🔑 **Keyboard Shortcuts** for faster workflow  
- 🔒 **Hashing Tools** (MD5, SHA-1, SHA-256, SHA-512) with clipboard + file support  
- ✅ Clean, modular, and extensible codebase  

---

## 📁 Project Structure

```
PyPad/
├── main.py                # Entry point of the application
├── .gitignore             # Git ignore file
├── LICENSE                # MIT License
├── README.md              # Project documentation
├── dialogs/               # Dialog-related features
│   ├── exit_dialog.py          # Custom exit confirmation dialog
│   ├── find_and_replace.py     # Find and Replace dialog
│   └── FontDialogWinStyle.py   # Custom font picker with preview
├── features/              # Utility and additional features
│   ├── shortcut_key.py        # Keyboard shortcut bindings
│   └── syntax_highlight.py    # Syntax highlighting for code files
│   └── hash_menu.py           # Hashing tool (MD5/SHA-1/SHA-256/SHA-512)
├── ui/                    # UI components
│   ├── context_menu.py        # Right-click menu
│   ├── minimap.py             # Minimap view for text area
│   ├── file_explorer.py       # File Explorer sidebar
│   ├── PyPad_UI.py            # Main Notepad GUI layout
└── .git/                  # Git version control directory
```

---

## 📦 Requirements  

- Python 3.10+  
- PyQt5  

> (Tkinter version has been replaced with PyQt5 for a more modern UI experience)  

---

## 🛠️ How to Run

```bash
# Clone the repository
git clone https://github.com/sundae0/PyPad
cd PyPad

# Install required dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 🌟 Supported File Types for Syntax Highlighting

PyPad provides syntax highlighting for various programming and markup languages, including:

- Python (.py)
- JavaScript (.js)
- HTML (.html)
- CSS (.css)
- Java (.java)
- C/C++ (.c, .cpp)
- JSON (.json)
- Markdown (.md)
- XML (.xml)
- SQL (.sql)
- Shell scripts (.sh)
- And many more!

The editor automatically detects the file type based on extension and applies appropriate syntax highlighting.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
