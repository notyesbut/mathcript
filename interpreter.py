# mathscript/interpreter.py

from .parser import *
from .stdlib import mathlib, iolib, utils

class Context:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def get(self, name):
        value = self.variables.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.variables[name] = value

class Function:
    def __init__(self, name, param_names, body, context):
        self.name = name
        self.param_names = param_names
        self.body = body
        self.context = context

class Interpreter:
    def __init__(self):
        self.context = Context()
        self.builtins = self.init_builtins()

    def init_builtins(self):
        builtins = {}
        builtins.update(mathlib.__dict__)
        builtins.update(iolib.__dict__)
        builtins.update(utils.__dict__)
        return builtins

    def interpret(self, ast):
        for node in ast:
            self.visit(node)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_NumberNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value

    def visit_VarAccessNode(self, node):
        var_name = node.var_name
        value = self.context.get(var_name)
        if value is None:
            value = self.builtins.get(var_name)
            if value is None:
                raise NameError(f"Variable '{var_name}' is not defined")
        return value

    def visit_VarAssignNode(self, node):
        var_name = node.var_name
        value = self.visit(node.expr)
        self.context.set(var_name, value)
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
            if right == 0:
                raise ZeroDivisionError('Division by zero')
            return left / right
        elif op == '^':
            return left ** right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == 'and':
            return left and right
        elif op == 'or':
            return left or right
        else:
            raise Exception(f'Unknown operator {op}')

    def visit_UnaryOpNode(self, node):
        value = self.visit(node.node)
        op = node.op_token.value

        if op == '+':
            return +value
        elif op == '-':
            return -value
        elif op == 'not':
            return not value
        else:
            raise Exception(f'Unknown operator {op}')

    def visit_IfNode(self, node):
        condition = self.visit(node.condition)
        if condition:
            for stmt in node.body:
                self.visit(stmt)
        elif node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)

    def visit_WhileNode(self, node):
        while self.visit(node.condition):
            for stmt in node.body:
                self.visit(stmt)

    def visit_ForNode(self, node):
        iterable = self.visit(node.iterable)
        if not hasattr(iterable, '__iter__'):
            raise TypeError(f"Object '{iterable}' is not iterable")
        for item in iterable:
            self.context.set(node.var_name, item)
            for stmt in node.body:
                self.visit(stmt)

    def visit_FuncDefNode(self, node):
        func = Function(node.func_name, node.param_names, node.body, self.context)
        self.context.set(node.func_name, func)

    def visit_FuncCallNode(self, node):
        func = self.context.get(node.func_name)
        if func is None:
            func = self.builtins.get(node.func_name)
            if func is None:
                raise NameError(f"Function '{node.func_name}' is not defined")
            else:
                args = [self.visit(arg) for arg in node.args]
                return func(*args)
        elif isinstance(func, Function):
            if len(node.args) != len(func.param_names):
                raise TypeError(f"Function '{node.func_name}' expected {len(func.param_names)} arguments but got {len(node.args)}")
            new_context = Context(parent=func.context)
            for param_name, arg in zip(func.param_names, node.args):
                arg_value = self.visit(arg)
                new_context.set(param_name, arg_value)
            interpreter = Interpreter()
            interpreter.context = new_context
            interpreter.builtins = self.builtins
            interpreter.interpret(func.body)
            return interpreter.context.get('return_value')
        else:
            raise TypeError(f"'{node.func_name}' is not a function")

    def visit_ReturnNode(self, node):
        value = self.visit(node.expr)
        self.context.set('return_value', value)
        raise StopIteration('Return statement encountered')
