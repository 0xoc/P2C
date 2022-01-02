import ply.lex as lex


class P2CLexer(object):
    # reserved words
    reserved = {
        'and': 'AND',
        'or': 'OR',
        'if': 'IF',
        'for': 'FOR',
        'while': 'WHILE',
        'in': 'IN',
        'range': 'RANGE',
        'break': 'BREAK',
        'continue': 'CONTINUE',
    }

    comparison_symbols = [
        'EQ',
        'NEQ',
        'LT',
        'LTE',
        'GT',
        'GTE'
    ]

    logical_symbols = [
        'and',
        'or',
    ]

    arithmetic_symbols = [
        # arithmetic
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'POW',
        'MOD'
    ]

    # all the possible tokens
    tokens = [
        'ID',
        'NUMBER',
        'LOGIC',
        'RELOP',
        'ARITHMETIC',
        'LPRAN',  # (
        'RPRAN',  # )
        'LBRACE',  # {
        'RBRACE',  # }
        'SEP',  # separator ,
    ]
    tokens += list(reserved.values())

    # simple tokens regex definition
    t_LPRAN = r'\('
    t_RPRAN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_SEP = r'\,'

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    def print_tokens(self):
        print(self.tokens)


lexer = P2CLexer()
lexer.print_tokens()
