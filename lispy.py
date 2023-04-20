program = ("(begin (define r 10) (* pi (* r r)))")

def parse(program: str) -> None:
    return read_from_tokens(tokenize(program))

def tokenize(chars: str) -> list[str]:
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def atomize(token):
    try: return int(token)
    except:
        try: return float(token)
        except:
            return str(token)

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