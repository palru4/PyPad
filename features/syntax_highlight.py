import tkinter as tk
from pygments import lexers, token
from pygments.token import Token
import os

class SyntaxHighlighter:
    def __init__(self):
        self.light_theme = {
            Token.Keyword: "#0000FF",
            Token.String: "#008000",
            Token.Name.Function: "#800080",
            Token.Name.Class: "#800080",
            Token.Literal.Number: "#FF8000",
            Token.Comment: "#808080",
            Token.Operator: "#000000",
            Token.Punctuation: "#000000",
            "default": "#000000"
        }
        self.dark_theme = {
            Token.Keyword: "#569CD6",
            Token.String: "#CE9178",
            Token.Name.Function: "#DCDCAA",
            Token.Name.Class: "#4EC9B0",
            Token.Literal.Number: "#B5CEA8",
            Token.Comment: "#6A9955",
            Token.Operator: "#D4D4D4",
            Token.Punctuation: "#D4D4D4",
            "default": "#D4D4D4"
        }
        self.current_theme = self.light_theme
        self.lexer_cache = {}

    def set_theme(self, is_dark_mode):
        self.current_theme = self.dark_theme if is_dark_mode else self.light_theme

    def get_lexer_for_file(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()
        if extension in self.lexer_cache:
            return self.lexer_cache[extension]

        extension_map = {
            '.py': lexers.PythonLexer(),
            '.js': lexers.JavascriptLexer(),
            '.ts': lexers.TypeScriptLexer(),
            '.html': lexers.HtmlLexer(),
            '.css': lexers.CssLexer(),
            '.java': lexers.JavaLexer(),
            '.c': lexers.CLexer(),
            '.cpp': lexers.CppLexer(),
            '.cs': lexers.CSharpLexer(),
            '.go': lexers.GoLexer(),
            '.rs': lexers.RustLexer(),
            '.swift': lexers.SwiftLexer(),
            '.kt': lexers.KotlinLexer(),
            '.rb': lexers.RubyLexer(),
            '.php': lexers.PhpLexer(),
            '.sh': lexers.BashLexer(),
            '.json': lexers.JsonLexer(),
            '.md': lexers.MarkdownLexer(),
            # Add more if needed
        }
        lexer = extension_map.get(extension, None)
        self.lexer_cache[extension] = lexer
        return lexer

    def highlight_syntax(self, text_widget, file_path):
        content = text_widget.get("1.0", "end-1c")
        lexer = self.get_lexer_for_file(file_path)
        if lexer is None:
            # No lexer, remove all tags except "sel"
            for tag in text_widget.tag_names():
                if tag != "sel":
                    text_widget.tag_remove(tag, "1.0", "end")
            return

        # Clear previous tags except selection
        for tag in text_widget.tag_names():
            if tag != "sel":
                text_widget.tag_remove(tag, "1.0", "end")

        # Configure tags for all token types in theme
        for tok_type, color in self.current_theme.items():
            tag_name = str(tok_type).replace(".", "_")
            text_widget.tag_configure(tag_name, foreground=color)

        # Tokenize and apply tags
        start_index = 0
        tokens = lexer.get_tokens(content)
        line = 1
        column = 0

        for tok_type, value in tokens:
            if not value:
                continue
            lines = value.split("\n")
            for i, part in enumerate(lines):
                if part == "":
                    # Just a newline
                    if i < len(lines) - 1:
                        line += 1
                        column = 0
                    continue

                start = f"{line}.{column}"
                end_col = column + len(part)
                end = f"{line}.{end_col}"

                # Find the nearest color tag in hierarchy
                t = tok_type
                tag_name = None
                while t is not None:
                    candidate = str(t).replace(".", "_")
                    if candidate in text_widget.tag_names():
                        tag_name = candidate
                        break
                    t = t.parent

                if not tag_name:
                    tag_name = "default"

                text_widget.tag_add(tag_name, start, end)

                column += len(part)
                if i < len(lines) - 1:
                    line += 1
                    column = 0

        text_widget.update()
