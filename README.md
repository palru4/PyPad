# 📝 PyPad
A modern, lightweight Notepad clone built with Python and Tkinter, featuring syntax highlighting, dark mode, auto-save, multiple tabs, and a sleek Windows-style font dialog.
---
## 🚀 Features
- 🎨 **Syntax Highlighting** for multiple programming languages
- 🌗 **Dark/Light Theme Toggle** with theme-aware syntax highlighting
- 💾 **Auto-Save** support to prevent data loss
- 🗂️ **Multiple Tabs** with file management
- 🔠 **Windows-Style Font Dialog** with live preview
- 📜 **Minimap Preview** for code navigation
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
│   ├── shortcut_key.py        # Keyboard shortcut bindings
│   └── syntax_highlight.py    # Syntax highlighting for code files
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
- Pygments (for syntax highlighting)
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
## 🎨 Screenshots
### Find and Replace dialog

<p align="center">
  <img src="img/findandreplace.PNG" alt="image" width="600"/><br>
  <em>Dialog of "Find and Replace"</em>
</p>

### Syntax highlighting for multiple programming languages, support for both light and dark mode

<p align="center">
  <img src="img/syntaxlightmode.PNG" alt="image" width="600"/><br>
  <em>Light mode</em>
</p>

<p align="center">
  <img src="img/syntaxdarkmode.PNG" alt="image" width="600"/><br>
  <em>Dark mode</em>
</p>

---
## 📄 License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
