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

    def statement(self):
        if self.current_tok.type == 'KEYWORD':
            if self.current_tok.value == 'function':
                return self.func_def()
            elif self.current_tok.value == 'if':
                return self.if_statement()
            elif self.current_tok.value == 'while':
                return self.while_statement()
            elif self.current_tok.value == 'for':
                return self.for_statement()
            elif self.current_tok.value == 'return':
                return self.return_statement()
            elif self.current_tok.value == 'print':
                return self.print_statement()
            else:
                raise SyntaxError(f"Unknown keyword '{self.current_tok.value}'")
        elif self.current_tok.type == 'IDENT':
            if self.peek_next().type == 'OP' and self.peek_next().value == '=':
                return self.var_assign()
            elif self.peek_next().type == 'OP' and self.peek_next().value == '(':
                return self.expr()
            else:
                return self.expr()
        else:
            return self.expr()

    def var_assign(self):
        var_name = self.current_tok.value
        self.advance()  # Skip variable name
        self.advance()  # Skip '='
        expr = self.expr()
        return VarAssignNode(var_name, expr)

    def expr(self):
        return self.bin_op(self.comp_expr, [('OP', 'and'), ('OP', 'or')])

    def comp_expr(self):
        return self.bin_op(self.arith_expr, [('OP', '=='), ('OP', '!='), ('OP', '<'), ('OP', '>'), ('OP', '<='), ('OP', '>=')])

    def arith_expr(self):
        return self.bin_op(self.term, [('OP', '+'), ('OP', '-')])

    def term(self):
        return self.bin_op(self.factor, [('OP', '*'), ('OP', '/')])

    def factor(self):
        tok = self.current_tok
        if tok.type == 'OP' and tok.value in ('+', '-', 'not'):
            self.advance()
            node = self.factor()
            return UnaryOpNode(tok, node)
        elif tok.type == 'NUMBER':
            self.advance()
            return NumberNode(tok.value)
        elif tok.type == 'STRING':
            self.advance()
            return StringNode(tok.value)
        elif tok.type == 'IDENT':
            if self.peek_next().type == 'OP' and self.peek_next().value == '(':
                return self.func_call()
            else:
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
        else:
            raise SyntaxError(f'Unexpected token {tok}')

    def func_def(self):
        self.advance()  # Skip 'function'
        func_name = self.current_tok.value
        self.advance()  # Skip function name
        if self.current_tok.type != 'OP' or self.current_tok.value != '(':
            raise SyntaxError('Expected "(" after function name')
        self.advance()  # Skip '('
        param_names = []
        if self.current_tok.type == 'IDENT':
            param_names.append(self.current_tok.value)
            self.advance()
            while self.current_tok.type == 'OP' and self.current_tok.value == ',':
                self.advance()
                if self.current_tok.type == 'IDENT':
                    param_names.append(self.current_tok.value)
                    self.advance()
                else:
                    raise SyntaxError('Expected parameter name')
        if self.current_tok.type != 'OP' or self.current_tok.value != ')':
            raise SyntaxError('Expected ")" after parameters')
        self.advance()  # Skip ')'
        body = self.block()
        return FuncDefNode(func_name, param_names, body)

    def func_call(self):
        func_name = self.current_tok.value
        self.advance()  # Skip function name
        self.advance()  # Skip '('
        args = []
        if self.current_tok.type != 'OP' or self.current_tok.value != ')':
            args.append(self.expr())
            while self.current_tok.type == 'OP' and self.current_tok.value == ',':
                self.advance()
                args.append(self.expr())
        if self.current_tok.type != 'OP' or self.current_tok.value != ')':
            raise SyntaxError('Expected ")" after arguments')
        self.advance()  # Skip ')'
        return FuncCallNode(func_name, args)

    def if_statement(self):
        self.advance()  # Skip 'if'
        condition = self.expr()
        body = self.block()
        else_body = None
        if self.current_tok.type == 'KEYWORD' and self.current_tok.value == 'else':
            self.advance()
            else_body = self.block()
        return IfNode(condition, body, else_body)

    def while_statement(self):
        self.advance()  # Skip 'while'
        condition = self.expr()
        body = self.block()
        return WhileNode(condition, body)

    def for_statement(self):
        self.advance()  # Skip 'for'
        var_name = self.current_tok.value
        self.advance()  # Skip variable name
        if self.current_tok.type != 'KEYWORD' or self.current_tok.value != 'in':
            raise SyntaxError('Expected "in" after variable name in for loop')
        self.advance()  # Skip 'in'
        iterable = self.expr()
        body = self.block()
        return ForNode(var_name, iterable, body)

    def return_statement(self):
        self.advance()  # Skip 'return'
        expr = self.expr()
        return ReturnNode(expr)

    def print_statement(self):
        self.advance()  # Skip 'print'
        args = []
        if self.current_tok.type == 'OP' and self.current_tok.value == '(':
            self.advance()  # Skip '('
            args.append(self.expr())
            while self.current_tok.type == 'OP' and self.current_tok.value == ',':
                self.advance()
                args.append(self.expr())
            if self.current_tok.type != 'OP' or self.current_tok.value != ')':
                raise SyntaxError('Expected ")" after arguments')
            self.advance()  # Skip ')'
        else:
            args.append(self.expr())
        return FuncCallNode('print', args)

    def block(self):
        if self.current_tok.type != 'OP' or self.current_tok.value != '{':
            raise SyntaxError('Expected "{" to start block')
        self.advance()  # Skip '{'
        statements = []
        while self.current_tok.type != 'OP' or self.current_tok.value != '}':
            stmt = self.statement()
            statements.append(stmt)
        self.advance()  # Skip '}'
        return statements

    def bin_op(self, func, ops):
        left = func()
        while any(self.current_tok.type == op[0] and self.current_tok.value == op[1] for op in ops):
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
