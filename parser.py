# parser.py

from lexer import Token

class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = float(value)

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

class SumNode(ASTNode):
    def __init__(self, var_name, start_expr, end_expr, body_expr):
        self.var_name = var_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body_expr = body_expr

class ProdNode(ASTNode):
    def __init__(self, var_name, start_expr, end_expr, body_expr):
        self.var_name = var_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body_expr = body_expr

class IntNode(ASTNode):
    def __init__(self, var_name, start_expr, end_expr, body_expr):
        self.var_name = var_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body_expr = body_expr

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
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

    def statement(self):
        if self.current_tok.type == 'IDENT' and self.peek_next().type == 'OP' and self.peek_next().value == '=':
            return self.assignment()
        else:
            return self.expr()

    def assignment(self):
        var_name = self.current_tok.value
        self.advance()  # Skip IDENT
        self.advance()  # Skip '='
        expr = self.expr()
        return VarAssignNode(var_name, expr)

    def expr(self):
        return self.bin_op(self.term, ('OP',), ('+', '-'))

    def term(self):
        return self.bin_op(self.factor, ('OP',), ('*', '/'))

    def factor(self):
        tok = self.current_tok
        if tok.type == 'OP' and tok.value in ('+', '-'):
            self.advance()
            node = self.factor()
            return UnaryOpNode(tok, node)
        elif tok.type == 'NUMBER':
            self.advance()
            return NumberNode(tok.value)
        elif tok.type == 'IDENT':
            self.advance()
            return VarAccessNode(tok.value)
        elif tok.type == 'OP' and tok.value == '(':
            self.advance()
            expr = self.expr()
            if self.current_tok.type == 'OP' and self.current_tok.value == ')':
                self.advance()
                return expr
            else:
                raise SyntaxError('Expected ")"')
        elif tok.type in ('SUM', 'PROD', 'INT'):
            return self.special_operator()
        else:
            raise SyntaxError(f'Unexpected token {tok}')

    def special_operator(self):
        tok = self.current_tok
        op_type = tok.type
        self.advance()
        if self.current_tok.type != 'OP' or self.current_tok.value != '(':
            raise SyntaxError('Expected "(" after operator')
        self.advance()
        var_name = self.current_tok.value
        self.advance()
        if self.current_tok.type != 'OP' or self.current_tok.value != '=':
            raise SyntaxError('Expected "=" after variable name')
        self.advance()
        start_expr = self.expr()
        if self.current_tok.type != 'COMMA':
            raise SyntaxError('Expected "," after start expression')
        self.advance()
        end_expr = self.expr()
        if self.current_tok.type != 'COMMA':
            raise SyntaxError('Expected "," after end expression')
        self.advance()
        body_expr = self.expr()
        if self.current_tok.type != 'OP' or self.current_tok.value != ')':
            raise SyntaxError('Expected ")" at the end of operator')
        self.advance()
        if op_type == 'SUM':
            return SumNode(var_name, start_expr, end_expr, body_expr)
        elif op_type == 'PROD':
            return ProdNode(var_name, start_expr, end_expr, body_expr)
        elif op_type == 'INT':
            return IntNode(var_name, start_expr, end_expr, body_expr)

    def bin_op(self, func, op_types, op_values):
        left = func()
        while self.current_tok.type in op_types and self.current_tok.value in op_values:
            op_tok = self.current_tok
            self.advance()
            right = func()
            left = BinOpNode(left, op_tok, right)
        return left

    def peek_next(self):
        if self.tok_idx + 1 < len(self.tokens):
            return self.tokens[self.tok_idx + 1]
        else:
            return Token('EOF')
