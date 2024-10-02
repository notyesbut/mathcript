# interpreter.py

import math
from parser import *

class Context:
    def __init__(self):
        self.symbol_table = {}

class Interpreter:
    def __init__(self):
        self.context = Context()
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'exp': math.exp,
            'sqrt': math.sqrt,
            'π': math.pi,
            'e': math.e,
        }

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node):
        return node.value

    def visit_VarAccessNode(self, node):
        var_name = node.var_name
        value = self.context.symbol_table.get(var_name, None)
        if value is None:
            func = self.functions.get(var_name, None)
            if func is not None:
                return func
            else:
                raise NameError(f'Variable "{var_name}" is not defined')
        return value

    def visit_VarAssignNode(self, node):
        var_name = node.var_name
        value = self.visit(node.expr)
        self.context.symbol_table[var_name] = value
        return value

    def visit_BinOpNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        op = node.op_token.value
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '^':
            return left ** right
        else:
            raise Exception(f'Unknown operator {op}')

    def visit_UnaryOpNode(self, node):
        value = self.visit(node.node)
        op = node.op_token.value
        if op == '+':
            return +value
        elif op == '-':
            return -value
        else:
            raise Exception(f'Unknown operator {op}')

    def visit_SumNode(self, node):
        var_name = node.var_name
        start = int(self.visit(node.start_expr))
        end = int(self.visit(node.end_expr))
        total = 0
        for i in range(start, end + 1):
            self.context.symbol_table[var_name] = i
            total += self.visit(node.body_expr)
        del self.context.symbol_table[var_name]
        return total

    def visit_ProdNode(self, node):
        var_name = node.var_name
        start = int(self.visit(node.start_expr))
        end = int(self.visit(node.end_expr))
        result = 1
        for i in range(start, end + 1):
            self.context.symbol_table[var_name] = i
            result *= self.visit(node.body_expr)
        del self.context.symbol_table[var_name]
        return result

    def visit_IntNode(self, node):
        var_name = node.var_name
        start = self.visit(node.start_expr)
        end = self.visit(node.end_expr)
        steps = 1000
        delta = (end - start) / steps
        total = 0
        for i in range(steps):
            x = start + i * delta
            self.context.symbol_table[var_name] = x
            total += self.visit(node.body_expr) * delta
        del self.context.symbol_table[var_name]
        return total
