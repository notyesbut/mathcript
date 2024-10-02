# lexer.py

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
            ('NUMBER',   r'\d+(\.\d*)?'),       # Integer or decimal number
            ('IDENT',    r'[A-Za-z_][\w_]*'),   # Identifiers
            ('OP',       r'[+\-*/^=<>≤≥≠()]'),  # Operators and delimiters
            ('SUM',      r'∑'),                 # Summation symbol
            ('PROD',     r'∏'),                 # Product symbol
            ('INT',      r'∫'),                 # Integral symbol
            ('COMMA',    r','),                 # Comma separator
            ('NEWLINE',  r'\n'),                # Line endings
            ('SKIP',     r'[ \t]+'),            # Skip spaces and tabs
            ('MISMATCH', r'.'),                 # Any other character
        ]
        self.token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)
        self.get_token = re.compile(self.token_regex).match

    def tokenize(self):
        tokens = []
        mo = self.get_token(self.code)
        while mo is not None:
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == 'NUMBER':
                tokens.append(Token('NUMBER', value, self.line, self.column))
            elif kind == 'IDENT':
                tokens.append(Token('IDENT', value, self.line, self.column))
            elif kind in ('OP', 'SUM', 'PROD', 'INT', 'COMMA'):
                tokens.append(Token(kind, value, self.line, self.column))
            elif kind == 'NEWLINE':
                self.line += 1
                self.column = 0
            elif kind == 'SKIP':
                pass
            elif kind == 'MISMATCH':
                raise SyntaxError(f'Unexpected character {value!r} at line {self.line} column {self.column}')
            self.pos = mo.end()
            self.column += mo.end() - mo.start()
            mo = self.get_token(self.code, self.pos)
        tokens.append(Token('EOF', line=self.line, column=self.column))
        return tokens
