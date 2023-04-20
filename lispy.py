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