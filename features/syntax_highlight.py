import tkinter as tk
from pygments import highlight, lexers
from pygments.token import Token
import os
import re

class SyntaxHighlighter:
    def __init__(self):
        # Define color schemes for syntax highlighting
        self.light_theme = {
            Token.Keyword: "#0000FF",           # Blue
            Token.String: "#008000",            # Green
            Token.Name.Function: "#800080",     # Purple
            Token.Name.Class: "#800080",        # Purple
            Token.Literal.Number: "#FF8000",    # Orange
            Token.Comment: "#808080",           # Gray
            Token.Operator: "#000000",          # Black
            Token.Punctuation: "#000000",       # Black
            "default": "#000000"                # Black
        }
        
        self.dark_theme = {
            Token.Keyword: "#569CD6",           # Light Blue
            Token.String: "#CE9178",            # Light Orange
            Token.Name.Function: "#DCDCAA",     # Yellow
            Token.Name.Class: "#4EC9B0",        # Teal
            Token.Literal.Number: "#B5CEA8",    # Light Green
            Token.Comment: "#6A9955",           # Green
            Token.Operator: "#D4D4D4",          # Light Gray
            Token.Punctuation: "#D4D4D4",       # Light Gray
            "default": "#D4D4D4"                # Light Gray
        }
        
        self.current_theme = self.light_theme
        
    def set_theme(self, is_dark_mode):
        """Switch between dark and light themes"""
        self.current_theme = self.dark_theme if is_dark_mode else self.light_theme
    
    def get_lexer_for_file(self, file_path):
        """Get the appropriate lexer based on file extension"""
        try:
            extension = os.path.splitext(file_path)[1].lower()
            
            # Common file extensions mapping
            extension_map = {
                '.py': lexers.PythonLexer(),
                '.js': lexers.JavascriptLexer(),
                '.html': lexers.HtmlLexer(),
                '.css': lexers.CssLexer(),
                '.java': lexers.JavaLexer(),
                '.c': lexers.CLexer(),
                '.cpp': lexers.CppLexer(),
                '.json': lexers.JsonLexer(),
                '.md': lexers.MarkdownLexer(),
                '.xml': lexers.XmlLexer(),
                '.sql': lexers.SqlLexer(),
                '.sh': lexers.BashLexer(),
                '.txt': None  # Plain text
            }
            
            # Return the lexer if available
            if extension in extension_map:
                return extension_map[extension]
                
            # Try Pygments' get_lexer_for_filename as a fallback
            return lexers.get_lexer_for_filename(file_path)
        except:
            # Default to None if no lexer found
            return None
    
    def highlight_syntax(self, text_widget, file_path):
        """Apply syntax highlighting to the text in the widget"""
        # Clear any existing tags
        for tag in text_widget.tag_names():
            if tag != "sel":  # Don't remove the selection tag
                text_widget.tag_delete(tag)
        
        # Get the lexer for the file
        lexer = self.get_lexer_for_file(file_path)
        
        if lexer:
            # Get the text content
            content = text_widget.get("1.0", tk.END)
            
            # Create tags for different token types
            for token_type, color in self.current_theme.items():
                tag_name = str(token_type).replace(".", "_")
                text_widget.tag_configure(tag_name, foreground=color)
            
            # Get the tokens from the lexer
            tokens = lexer.get_tokens(content)
            
            # Apply highlighting by adding tags
            start_index = "1.0"
            for token_type, value in tokens:
                # Calculate end index
                end_index = text_widget.index(f"{start_index}+{len(value)}c")
                
                # Find parent token types for hierarchical tokens
                current_type = token_type
                while current_type is not None:
                    tag_name = str(current_type).replace(".", "_")
                    # Apply the tag if we have a color for it
                    if current_type in self.current_theme:
                        text_widget.tag_add(tag_name, start_index, end_index)
                        break
                    # Move up the token hierarchy
                    current_type = current_type.parent
                else:
                    # Use default color if no match was found
                    text_widget.tag_add("default", start_index, end_index)
                
                # Move to the next token
                start_index = end_index
        
        # Update the widget display
        text_widget.update()