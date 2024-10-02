

# mathscript.py

import re
import sys
import math

class MathScript:
    def __init__(self):
        self.variables = {}
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'exp': math.exp,
            'sqrt': math.sqrt,
        }

    def transpile(self, code):
        """
        Transpile MathScript code into executable Python code.

        Parameters:
        - code (str): The MathScript code to transpile.

        Returns:
        - Transpiled Python code as a string.
        """
        # Tokenize the input code
        tokens = self.tokenize(code)
        # Parse tokens into an abstract syntax tree (AST)
        ast = self.parse(tokens)
        # Generate Python code from the AST
        python_code = self.generate_python_code(ast)
        return python_code

    def tokenize(self, code):
        """
        Convert the input code into a list of tokens.

        Parameters:
        - code (str): The MathScript code to tokenize.

        Returns:
        - A list of tokens.
        """
        token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
            ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers
            ('OP',       r'[+\-*/^∑∏∫=<>≤≥≠()]'),  # Operators and delimiters
            ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
            ('NEWLINE',  r'\n'),           # Line endings
            ('MISMATCH', r'.'),            # Any other character
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line_num = 1
        line_start = 0
        tokens = []
        pos = 0
        mo = get_token(code)
        while mo is not None:
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == 'NUMBER':
                tokens.append(('NUMBER', value))
            elif kind == 'IDENT':
                tokens.append(('IDENT', value))
            elif kind == 'OP':
                tokens.append(('OP', value))
            elif kind == 'NEWLINE':
                line_num += 1
                line_start = mo.end()
            elif kind == 'SKIP':
                pass
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            pos = mo.end()
            mo = get_token(code, pos)
        return tokens

    def parse(self, tokens):
        """
        Parse the list of tokens into an AST.

        Parameters:
        - tokens (list): The list of tokens to parse.

        Returns:
        - An abstract syntax tree representing the code.
        """
        # For simplicity, we'll assume the code is a single expression
        # In a full implementation, we would build a complete parser
        return tokens

    def generate_python_code(self, ast):
        """
        Generate Python code from the AST.

        Parameters:
        - ast: The abstract syntax tree.

        Returns:
        - Python code as a string.
        """
        python_code = ''
        for token in ast:
            token_type, value = token
            if token_type == 'NUMBER':
                python_code += value
            elif token_type == 'IDENT':
                python_code += value
            elif token_type == 'OP':
                python_code += self.map_operator(value)
            else:
                pass  # Handle other token types if necessary
        return python_code

    def map_operator(self, op):
        """
        Map MathScript operators to Python operators.

        Parameters:
        - op (str): The operator symbol.

        Returns:
        - The corresponding Python operator as a string.
        """
        operator_mapping = {
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '^': '**',
            '=': '=',
            '<': '<',
            '>': '>',
            '≤': '<=',
            '≥': '>=',
            '≠': '!=',
            '∑': 'sum',  # Special handling required
            '∏': 'product',  # Special handling required
            '∫': 'integrate',  # Special handling required
            '(': '(',
            ')': ')',
        }
        return operator_mapping.get(op, op)

    def execute(self, code):
        """
        Execute the given MathScript code.

        Parameters:
        - code (str): The MathScript code to execute.

        Returns:
        - The result of the execution.
        """
        python_code = self.transpile(code)
        # Prepare the execution environment
        exec_env = {**self.functions, **self.variables}
        # Execute the Python code
        exec(python_code, exec_env)
        # Update variables with any changes
        self.variables.update(exec_env)
        return exec_env

# Example usage
if __name__ == "__main__":
    ms = MathScript()
    code = """
    x = 10
    y = ∑(i=1 to x) i
    z = ∏(i=1 to 5) i
    area = ∫(x=0 to π) sin(x) dx
    result = x + y + z + area
    """
    ms.execute(code)
    print("Variables:", ms.variables)
