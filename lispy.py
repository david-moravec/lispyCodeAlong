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
        return env[x]
    elif isinstance(x, Number):
        return x
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test) else alt)

        return eval(exp)
    elif x[0] == 'define':
        (_, symbol, exp) = x
        env[symbol] = eval(exp)
    else:
        proc = eval(x[0])
        args = [eval(arg) for arg in x[1:]]

        return proc(*args)

a = eval(parse("(begin (define r 10) (* pi (* r r)))"))