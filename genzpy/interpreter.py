import re
import random
import sys

################################################################################
# 1. LEXER (The "Vibe Check")
################################################################################

class Lexer:
    def __init__(self, text):
        self.text = text
        keywords = [
            'bro', 'print', 'spill_tea', 'vibe', 'check', 'squad', 'tea', 'clique',
            'fr', 'if', 'mid', 'lowkey', 'no', 'cap', 'sleep', 'move', 'on',
            'yeet', 'bet', 'glow_up', 'spill', 'plus_one', 'take_L', 'flex',
            'split', 'leftovers', 'same_vibes', 'bad_vibes', 'pull_up', 'drip',
            'no_lies', 'caught_in_4k', 'vibe_with', 'facts', 'cap', 'ghosted',
            'fin', 'to'
        ]
        keyword_regex = r'\b(' + '|'.join(keywords) + r')\b'
        self.token_specs = [
            ('NUMBER',   r'\d+(\.\d*)?'), ('STRING',   r"'[^']*'"),
            ('KEYWORD',  keyword_regex), ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('OP',       r'[+\-*/%]'), ('COMP',     r'==|!=|<=|>=|>|<'),
            ('LPAREN',   r'\('), ('RPAREN',   r'\)'),
            ('LBRACKET', r'\['), ('RBRACKET', r'\]'),
            ('COMMA',    r','), ('ASSIGN',   r'='),
            ('NEWLINE',  r'\n'), ('SKIP',     r'[ \t]+'),
            ('MISMATCH', r'.'),
        ]
        self.token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specs)

    def tokenize(self):
        tokens = []
        for mo in re.finditer(self.token_regex, self.text):
            kind = mo.lastgroup
            value = mo.group()
            if kind in ('SKIP', 'NEWLINE'): continue
            if kind == 'MISMATCH': raise RuntimeError(f'Unexpected character: {value}')
            tokens.append((kind, value))
        return tokens

################################################################################
# 2. PARSER (The Brains)
################################################################################

class BinOp:
    def __init__(self, left, op, right): self.left, self.op, self.right = left, op, right
class Number:
    def __init__(self, value): self.value = value
class String:
    def __init__(self, value): self.value = value
class ListNode:
    def __init__(self, elements): self.elements = elements
class VarAccess:
    def __init__(self, var_name): self.var_name = var_name
class VarAssign:
    def __init__(self, var_name, value): self.var_name, self.value = var_name, value
class PrintStatement:
    def __init__(self, value): self.value = value
class IfStatement:
    def __init__(self, cases, else_case): self.cases, self.else_case = cases, else_case
class ForLoop:
    def __init__(self, var_name, start_val, end_val, body): self.var_name, self.start_val, self.end_val, self.body = var_name, start_val, end_val, body
class WhileLoop:
    def __init__(self, condition, body): self.condition, self.body = condition, body
class BreakNode: pass
class ContinueNode: pass
class FuncDef:
    def __init__(self, name, params, body): self.name, self.params, self.body = name, params, body
class FuncCall:
    def __init__(self, name_node, args): self.name_node, self.args = name_node, args
class ReturnNode:
    def __init__(self, value_node): self.value_node = value_node

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()
    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
    def parse(self):
        statements = []
        while self.current_token is not None and self.current_token[1] not in ('fin', 'lowkey', 'mid'):
            statements.append(self.statement())
        return statements
    def statement(self):
        if self.current_token[1] == 'vibe' and self.tokens[self.pos+1][1] == 'check':
            self.advance(); self.advance()
            var_name = self.current_token[1]
            self.advance()
            if self.current_token[0] != 'ASSIGN': raise SyntaxError("Expected '=' for vibe check")
            self.advance()
            return VarAssign(var_name, self.expression())
        if self.current_token[1] == 'bro' and self.tokens[self.pos+1][1] == 'print':
            self.advance(); self.advance()
            return PrintStatement(self.expression())
        if self.current_token[1] == 'fr' and self.tokens[self.pos+1][1] == 'if':
            return self.if_statement()
        if self.current_token[1] == 'no' and self.tokens[self.pos+1][1] == 'cap':
            return self.for_loop()
        if self.current_token[1] == 'keep' and self.tokens[self.pos+2][1] == '100':
             return self.while_loop()
        if self.current_token[1] == 'yeet': self.advance(); return BreakNode()
        if self.current_token[1] == 'bet': self.advance(); return ContinueNode()
        if self.current_token[1] == 'glow_up':
            return self.func_def()
        if self.current_token[1] == 'spill':
            self.advance()
            return ReturnNode(self.expression())
        return self.expression()
    def if_statement(self):
        cases, else_case = [], None
        self.advance(); self.advance()
        condition = self.expression()
        body = self.parse()
        cases.append((condition, body))
        while self.current_token is not None and self.current_token[1] == 'mid':
            self.advance(); self.advance()
            condition = self.expression()
            body = self.parse()
            cases.append((condition, body))
        if self.current_token is not None and self.current_token[1] == 'lowkey':
            self.advance()
            else_case = self.parse()
        if self.current_token is None or self.current_token[1] != 'fin':
            raise SyntaxError("Expected 'fin' to end conditional block")
        self.advance()
        return IfStatement(cases, else_case)
    def for_loop(self):
        self.advance(); self.advance()
        var_name = self.current_token[1]
        self.advance()
        if self.current_token[1] != 'from': raise SyntaxError("Expected 'from' in for loop")
        self.advance()
        start_val = self.expression()
        if self.current_token[1] != 'to': raise SyntaxError("Expected 'to' in for loop")
        self.advance()
        end_val = self.expression()
        body = self.parse()
        if self.current_token[1] != 'fin': raise SyntaxError("Expected 'fin' to end 'no cap' loop")
        self.advance()
        return ForLoop(var_name, start_val, end_val, body)
    def while_loop(self):
        self.advance(); self.advance(); self.advance()
        condition = self.expression()
        body = self.parse()
        if self.current_token[1] != 'fin': raise SyntaxError("Expected 'fin' to end 'keep it 100' loop")
        self.advance()
        return WhileLoop(condition, body)
    def func_def(self):
        self.advance()
        name = self.current_token[1]
        self.advance()
        if self.current_token[0] != 'LPAREN': raise SyntaxError("Expected '(' in function definition")
        self.advance()
        params = []
        if self.current_token[0] != 'RPAREN':
            params.append(self.current_token[1])
            self.advance()
            while self.current_token[0] == 'COMMA':
                self.advance()
                params.append(self.current_token[1])
                self.advance()
        if self.current_token[0] != 'RPAREN': raise SyntaxError("Expected ')' or ',' in function parameters")
        self.advance()
        body = self.parse()
        if self.current_token[1] != 'fin': raise SyntaxError("Expected 'fin' to end 'glow_up'")
        self.advance()
        return FuncDef(name, params, body)
    def expression(self):
        node = self.term()
        while self.current_token is not None and self.current_token[0] in ('OP', 'COMP'):
            op_token = self.current_token
            self.advance()
            right = self.term()
            node = BinOp(node, op_token, right)
        return node
    def term(self):
        node = self.factor()
        if self.current_token is not None and self.current_token[0] == 'LPAREN':
            self.advance()
            args = []
            if self.current_token[0] != 'RPAREN':
                args.append(self.expression())
                while self.current_token[0] == 'COMMA':
                    self.advance()
                    args.append(self.expression())
            if self.current_token[0] != 'RPAREN': raise SyntaxError("Expected ')' or ',' in function call")
            self.advance()
            return FuncCall(node, args)
        return node
    def factor(self):
        token = self.current_token
        if token[0] == 'NUMBER': self.advance(); return Number(float(token[1]))
        if token[0] == 'STRING': self.advance(); return String(token[1][1:-1])
        if token[0] == 'ID': self.advance(); return VarAccess(token[1])
        if token[1] == 'facts': self.advance(); return Number(1)
        if token[1] == 'cap': self.advance(); return Number(0)
        if token[1] == 'squad': return self.list_expr()
        if token[0] == 'LPAREN':
            self.advance()
            node = self.expression()
            if self.current_token[0] != 'RPAREN': raise SyntaxError("Expected ')'")
            self.advance()
            return node
        raise SyntaxError(f"Invalid term: {token}")
    def list_expr(self):
        self.advance()
        elements = []
        if self.current_token[0] != 'LBRACKET': raise SyntaxError("Expected '[' for squad")
        self.advance()
        if self.current_token[0] != 'RBRACKET':
            elements.append(self.expression())
            while self.current_token[0] == 'COMMA':
                self.advance()
                elements.append(self.expression())
        if self.current_token[0] != 'RBRACKET': raise SyntaxError("Expected ']' or ',' in squad")
        self.advance()
        return ListNode(elements)

################################################################################
# 3. INTERPRETER (The Executor)
################################################################################

class ReturnValue(Exception):
    def __init__(self, value): self.value = value
class BreakSignal(Exception): pass
class ContinueSignal(Exception): pass

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent
    def get(self, name):
        if name in self.variables: return self.variables[name]
        if self.parent: return self.parent.get(name)
        raise NameError(f"Bhai, I don't know what '{name}' is. Ghosted.")
    def set(self, name, value): self.variables[name] = value

class BuiltInFunction:
    def __init__(self, name): self.name = name
    def execute(self, args):
        if self.name == 'spill_tea': return input(args[0] if args else "")
        if self.name == 'sneaky_link': return len(args[0])
        raise NameError(f"Built-in function '{self.name}' not found.")

class Function:
    def __init__(self, node, env): self.node, self.env = node, env
    def execute(self, args, interpreter):
        func_env = Environment(parent=self.env)
        if len(args) != len(self.node.params): raise TypeError("Wrong number of arguments")
        for name, val in zip(self.node.params, args):
            func_env.set(name, val)
        try:
            interpreter.interpret(self.node.body, func_env)
        except ReturnValue as ret:
            return ret.value
        return None

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.global_env.set('spill_tea', BuiltInFunction('spill_tea'))
        self.global_env.set('sneaky_link', BuiltInFunction('sneaky_link'))
    def interpret(self, ast_nodes, env=None):
        if env is None: env = self.global_env
        result = None
        for node in ast_nodes:
            result = self.visit(node, env)
        return result
    def visit(self, node, env):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, env)
    def no_visit_method(self, node, env):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    def visit_Number(self, node, env): return node.value
    def visit_String(self, node, env): return node.value
    def visit_ListNode(self, node, env): return [self.visit(elem, env) for elem in node.elements]
    def visit_VarAccess(self, node, env): return env.get(node.var_name)
    def visit_VarAssign(self, node, env):
        value = self.visit(node.value, env)
        env.set(node.var_name, value)
        return value
    def visit_PrintStatement(self, node, env): print(self.visit(node.value, env))
    def visit_BreakNode(self, node, env): raise BreakSignal()
    def visit_ContinueNode(self, node, env): raise ContinueSignal()
    def visit_ReturnNode(self, node, env): raise ReturnValue(self.visit(node.value_node, env))
    def visit_IfStatement(self, node, env):
        for condition, body in node.cases:
            if self.visit(condition, env) != 0:
                return self.interpret(body, Environment(parent=env))
        if node.else_case:
            return self.interpret(node.else_case, Environment(parent=env))
    def visit_ForLoop(self, node, env):
        start = int(self.visit(node.start_val, env))
        end = int(self.visit(node.end_val, env))
        loop_env = Environment(parent=env)
        for i in range(start, end):
            loop_env.set(node.var_name, i)
            try:
                self.interpret(node.body, loop_env)
            except BreakSignal: break
            except ContinueSignal: continue
    def visit_WhileLoop(self, node, env):
        loop_env = Environment(parent=env)
        while self.visit(node.condition, loop_env) != 0:
            try:
                self.interpret(node.body, loop_env)
            except BreakSignal: break
            except ContinueSignal: continue
    def visit_FuncDef(self, node, env):
        func = Function(node, env)
        env.set(node.name, func)
        return func
    def visit_FuncCall(self, node, env):
        func = self.visit(node.name_node, env)
        args = [self.visit(arg, env) for arg in node.args]
        if isinstance(func, Function):
            return func.execute(args, self)
        elif isinstance(func, BuiltInFunction):
            return func.execute(args)
        raise TypeError(f"'{node.name_node.var_name}' is not a function")
    def visit_BinOp(self, node, env):
        left = self.visit(node.left, env)
        right = self.visit(node.right, env)
        op = node.op[1]
        op_map = {'plus_one': '+', 'take_L': '-', 'flex': '*', 'split': '/', 'same_vibes': '==', 'bad_vibes': '!='}
        actual_op = op_map.get(op, op)
        if actual_op == '+': return left + right
        if actual_op == '-': return left - right
        if actual_op == '*': return left * right
        if actual_op == '/': return left / right
        if actual_op == '==': return 1 if left == right else 0
        if actual_op == '!=': return 1 if left != right else 0
        if actual_op == '>': return 1 if left > right else 0
        if actual_op == '<': return 1 if left < right else 0
        raise RuntimeError(f"Unknown operator: {op}")

def run(code):
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
    except (RuntimeError, SyntaxError, NameError, TypeError, ReturnValue, BreakSignal, ContinueSignal) as e:
        print(f"Yikes, an error: {e}")

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            code = f.read()
            run(code)
    else:
        print("GenZPy v0.1 - Interactive Mode")
        while True:
            try:
                code = input("> ")
                if code.strip() == 'exit':
                    break
                run(code)
            except EOFError:
                break
            except Exception as e:
                print(f"Yikes, an error: {e}")

if __name__ == "__main__":
    main()