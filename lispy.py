program = ("(begin (define r 10) (* pi (* r r)))")

Symbol = str              # A Scheme Symbol is implemented as a Python str
Number = (int, float)     # A Scheme Number is implemented as a Python int or float
Atom   = (Symbol, Number) # A Scheme Atom is a Symbol or Number
List   = list             # A Scheme List is implemented as a Python list
Exp    = (Atom, List)     # A Scheme expression is an Atom or List
Env    = dict             # A Scheme environment (defined below) 
                          # is a mapping of {variable: value}

def parse(program: str) -> None:
    return read_from_tokens(tokenize(program))

def tokenize(chars: str) -> list[str]:
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def atomize(token):
    try: return int(token)
    except:
        try: return float(token)
        except:
            return Symbol(token)

def read_from_tokens(tokens: list) -> list:
    if not tokens:
        raise SyntaxError('unxpected EOF')

    def read_inner_tokens():
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L


    token: str = tokens.pop(0)


    match token:
        case '(':
            return read_inner_tokens()
        case ')':
            return SyntaxError('unexpected )')
        case _:
            return atomize(token)

assert parse(program) == ['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]]

class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        return self if (var in self) else self.outer.find(var)

class Procedure:
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))

import math
import operator as op

def standard_env() -> Env:
    env = Env()
    env.update(vars(math))
    env.update({'+' : op.add, '-' : op.sub, '*'  : op.mul, '/'  : op.truediv,
                '>' : op.gt,  '<' : op.lt,  '>=' : op.ge,  '<=' : op.le,      '=' : op.eq,
                'abs'        : abs,
                'append'     : op.add,
                'apply'      : lambda proc, args: proc(*args),
                'begin'      : lambda *x: x[-1],
                'car'        : lambda x: x[0],
                'cdr'        : lambda x: x[1:],
                'cons'       : lambda x, y: [x] + y,
                'eq?'        : op.is_,
                'equal?'     : op.eq,
                'expt'       : pow,
                'length'     : len,
                'list'       : lambda *x: List(x),
                'list?'      : lambda x: isinstance(x, List),
                'map'        : map,
                'max'        : max,
                'min'        : min,
                'not'        : op.not_,
                'null?'      : lambda x: x == [],
                'number'     : lambda x: isinstance(x, Number),
                'print'      : print,
                'procedure?' : lambda x: isinstance(x, callable),
                'round'      : round,
                'symbol?'     : lambda x: isinstance(x, Symbol),
    })
    
    return env

global_env = standard_env()


def eval(x: Exp, env=global_env) -> Exp:
    '''Eval expression in environment'''
    if isinstance(x, Symbol):
        return env.find(x)[x]
    elif isinstance(x, Number):
        return x
    
    op, *args = x

    if op == 'quote':
        return args[0]
    elif op == 'if':
        (test, conseq, alt) = args
        exp = (conseq if eval(test, env) else alt)

        return eval(exp)
    elif op == 'set!':
        (symbol, exp) = args
        env.find(symbol)[symbol] = eval(exp, env)
    elif op == 'define':
        (symbol, exp) = args
        env[symbol] = eval(exp, env)
    elif op == 'lambda':
        parms, body = args
        return Procedure(parms, body, env)
    else:
        proc = eval(op, env)
        vals = [eval(arg, env) for arg in args]

        return proc(*vals)

def repl(prompt='list.py> '):
    while True:
        raw_input = input(prompt)

        if raw_input == 'quit':
            break

        val = eval(parse(raw_input))

        if val is not None:
            print(schemestr(val))

def schemestr(exp):
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)