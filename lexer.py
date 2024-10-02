# mathscript/lexer.py

import re

class Token:
    def __init__(self, type_, value=None, line=0, column=0):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {self.value}, line={self.line}, column={self.column})'

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1

        # Define token specifications
        self.token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),               # Integer or decimal number
            ('STRING',   r'"(.*?)"'),                   # String literals
            ('IDENT',    r'[A-Za-z_][\w_]*'),           # Identifiers
            ('OP',       r'[+\-*/^=<>()%,]'),           # Operators and delimiters
            ('KEYWORD',  r'\b(function|if|else|for|while|return|and|or|not|in|range|print|input)\b'),  # Keywords
            ('NEWLINE',  r'\n'),                        # Line endings
            ('SKIP',     r'[ \t]+'),                    # Skip spaces and tabs
            ('MISMATCH', r'.'),                         # Any other character
        ]
        self.token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)
        self.get_token = re.compile(self.token_regex).match

    def tokenize(self):
        tokens = []
        code = self.code
        pos = 0
        line = 1
        column = 1
        while pos < len(code):
            match = self.get_token(code, pos)
            if match:
                kind = match.lastgroup
                value = match.group(kind)
                if kind == 'NEWLINE':
                    line += 1
                    column = 1
                elif kind == 'SKIP':
                    column += len(value)
                elif kind == 'MISMATCH':
                    raise SyntaxError(f'Unexpected character {value!r} at line {line} column {column}')
                else:
                    tokens.append(Token(kind, value, line, column))
                    column += len(value)
                pos = match.end()
            else:
                raise SyntaxError(f'Unexpected character {code[pos]!r} at line {line} column {column}')
        tokens.append(Token('EOF', line=line, column=column))
        return tokens
