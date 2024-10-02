# mathscript.py

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

class MathScript:
    def __init__(self):
        self.interpreter = Interpreter()

    def execute(self, code):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result = None
        for node in ast:
            result = self.interpreter.visit(node)
        return result

    def get_variables(self):
        return self.interpreter.context.symbol_table
