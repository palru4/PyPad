from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import Qt
from pygments import lexers, token
import os

class QtSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.light_theme = {
            token.Keyword: "#0000FF",
            token.Name: "#000000",
            token.Name.Function: "#795E26",
            token.Name.Class: "#267f99",
            token.Comment: "#999988",
            token.String: "#008000",
            token.Literal.Number: "#098658",
            token.Operator: "#000000",
            token.Punctuation: "#000000",
            "default": "#000000"
        }

        self.dark_theme = {
            token.Keyword: "#C586C0",
            token.Name: "#9CDCFE",
            token.Name.Function: "#DCDCAA",
            token.Name.Class: "#4EC9B0",
            token.Comment: "#6A9955",
            token.String: "#CE9178",
            token.Literal.Number: "#B5CEA8",
            token.Operator: "#D4D4D4",
            token.Punctuation: "#D4D4D4",
            "default": "#D4D4D4"
        }

        self.current_theme = self.light_theme
        self.lexer_cache = {}
        self.lexer = None

    def set_theme(self, is_dark_mode):
        self.current_theme = self.dark_theme if is_dark_mode else self.light_theme
        self.rehighlight()

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

    def set_file(self, file_path):
        self.lexer = self.get_lexer_for_file(file_path)
        self.rehighlight()

    def highlightBlock(self, text):
        if not self.lexer:
            return

        tokens = self.lexer.get_tokens(text)
        index = 0
        for tok_type, value in tokens:
            if not value:
                continue
            fmt = QTextCharFormat()
            color = self.current_theme.get(tok_type, self.current_theme["default"])
            fmt.setForeground(QColor(color))
            if "Bold" in str(tok_type):
                fmt.setFontWeight(QFont.Weight.Bold)
            if "Italic" in str(tok_type):
                fmt.setFontItalic(True)
            length = len(value)
            self.setFormat(index, length, fmt)
            index += length
