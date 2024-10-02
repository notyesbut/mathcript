# mathscript/lexer.py

import re

class Token:
    def __init__(self, type_, value=None, line=1, column=1):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {self.value}, line={self.line}, column={self.column})'

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_pos = 0
        self.line = 1
        self.column = 1

        # Define token patterns
        self.token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),               # Integer or decimal number
            ('STRING',   r'"[^"\\]*(\\.[^"\\]*)*"'),    # String literals
            ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'),    # Identifiers
            ('ASSIGN',   r'='),                         # Assignment operator
            ('LPAREN',   r'\('),                        # Left Parenthesis
            ('RPAREN',   r'\)'),                        # Right Parenthesis
            ('LBRACE',   r'\{'),                        # Left Brace
            ('RBRACE',   r'\}'),                        # Right Brace
            ('COMMA',    r','),                         # Comma
            ('COLON',    r':'),                         # Colon
            ('OP',       r'[\+\-\*/\^%]'),              # Arithmetic operators
            ('COMPARE',  r'==|!=|<=|>=|<|>'),           # Comparison operators
            ('NEWLINE',  r'\n'),                        # Line endings
            ('SKIP',     r'[ \t]+'),                    # Skip spaces and tabs
            ('COMMENT',  r'#.*'),                       # Comments
            ('KEYWORD',  r'\b(function|if|else|elif|for|while|return|and|or|not|in|true|false)\b'),  # Keywords
            ('MISMATCH', r'.'),                         # Any other character
        ]

        self.token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)
        self.get_token = re.compile(self.token_regex).match

    def tokenize(self):
        code = self.code
        pos = 0
        while pos < len(code):
            match = self.get_token(code, pos)
            if match:
                kind = match.lastgroup
                value = match.group(kind)
                if kind == 'NEWLINE':
                    self.line += 1
                    self.column = 1
                elif kind == 'SKIP' or kind == 'COMMENT':
                    pass
                elif kind == 'MISMATCH':
                    raise RuntimeError(f'{value!r} unexpected on line {self.line}')
                else:
                    self.tokens.append(Token(kind, value, self.line, self.column))
                pos = match.end()
            else:
                raise RuntimeError(f'Unexpected character {code[pos]} on line {self.line}')
        self.tokens.append(Token('EOF', line=self.line, column=self.column))
        return self.tokens
