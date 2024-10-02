# mathscript/parser.py

from .lexer import Token

class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = float(value)

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value.strip('"')

class VarAccessNode(ASTNode):
    def __init__(self, var_name):
        self.var_name = var_name

class VarAssignNode(ASTNode):
    def __init__(self, var_name, expr):
        self.var_name = var_name
        self.expr = expr

class BinOpNode(ASTNode):
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

class UnaryOpNode(ASTNode):
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

class IfNode(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForNode(ASTNode):
    def __init__(self, var_name, iterable, body):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body

class FuncDefNode(ASTNode):
    def __init__(self, func_name, param_names, body):
        self.func_name = func_name
        self.param_names = param_names
        self.body = body

class FuncCallNode(ASTNode):
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

class ReturnNode(ASTNode):
    def __init__(self, expr):
        self.expr = expr

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok = None
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        statements = []
        while self.current_tok.type != 'EOF':
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
            else:
                break
        return statements

