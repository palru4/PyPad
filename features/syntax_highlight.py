import tkinter as tk
from pygments import lexers, token
from pygments.token import Token
import os

class SyntaxHighlighter:
    def __init__(self):
        self.light_theme = {
            Token.Keyword: "#0000FF",
            Token.Name: "#000000",
            Token.Name.Function: "#795E26",
            Token.Name.Class: "#267f99",
            Token.Comment: "#999988",
            Token.String: "#008000",
            Token.Literal.Number: "#098658",
            Token.Operator: "#000000",
            Token.Punctuation: "#000000",
            "default": "#000000"
        }

        self.dark_theme = {
            Token.Keyword: "#C586C0",
            Token.Name: "#9CDCFE",
            Token.Name.Function: "#DCDCAA",
            Token.Name.Class: "#4EC9B0",
            Token.Comment: "#6A9955",
            Token.String: "#CE9178",
            Token.Literal.Number: "#B5CEA8",
            Token.Operator: "#D4D4D4",
            Token.Punctuation: "#D4D4D4",
            "default": "#D4D4D4"
        }

        self.current_theme = self.light_theme
        self.lexer_cache = {}

    def set_theme(self, is_dark_mode):
        self.current_theme = self.dark_theme if is_dark_mode else self.light_theme

    def get_lexer_for_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in self.lexer_cache:
            return self.lexer_cache[ext]

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
        }

        lexer = extension_map.get(ext)
        self.lexer_cache[ext] = lexer
        return lexer

    def highlight_syntax(self, text_widget, file_path):
        content = text_widget.get("1.0", "end-1c")
        lexer = self.get_lexer_for_file(file_path)
        if lexer is None:
            self.clear_tags(text_widget)
            return

        tokens = lexer.get_tokens(content)
        self.clear_tags(text_widget)
        self.configure_tags(text_widget)

        line = 1
        column = 0

        for tok_type, value in tokens:
            if not value:
                continue

            lines = value.split("\n")
            for i, part in enumerate(lines):
                if part == "":
                    if i < len(lines) - 1:
                        line += 1
                        column = 0
                    continue

                start = f"{line}.{column}"
                end = f"{line}.{column + len(part)}"
                tag = self.find_best_tag(text_widget, tok_type)

                if tag:
                    text_widget.tag_add(tag, start, end)

                column += len(part)
                if i < len(lines) - 1:
                    line += 1
                    column = 0

        text_widget.update()

    def clear_tags(self, text_widget):
        for tag in text_widget.tag_names():
            if tag != "sel":
                text_widget.tag_remove(tag, "1.0", "end")

    def configure_tags(self, text_widget):
        for tok_type, color in self.current_theme.items():
            tag = str(tok_type).replace(".", "_")
            text_widget.tag_configure(tag, foreground=color)

    def find_best_tag(self, text_widget, tok_type):
        while tok_type is not None:
            tag = str(tok_type).replace(".", "_")
            if tag in text_widget.tag_names():
                return tag
            tok_type = tok_type.parent
        return "default"
