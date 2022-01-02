import ply.lex as lex


class P2CLexer(object):
    # keyword constants
    IF = 'if'
    OR = 'or'
    AND = 'and'
    ELSE = 'else'
    FOR = 'for'
    WHILE = 'while'
    RANGE = 'range'
    IN = 'in'
    NOT = 'not'
    BREAK = 'break'
    CONTINUE = 'continue'

    # token constants
    NUMBER = 'NUMBER'
    ID = 'ID'
    LOGIC = 'LOGIC'
    RELOP = 'RELOP'
    OPERATOR = 'OPERATOR'
    LPRAN = 'LPRAN'
    RPRAN = 'RPRAN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    SEP = 'SEP'

    # reserved words
    reserved = {
        IF: IF,
        FOR: FOR,
        WHILE: WHILE,
        IN: IN,
        RANGE: RANGE,
        BREAK: BREAK,
        CONTINUE: CONTINUE,
        # some logical symbols are also reserved words
        AND: LOGIC,
        OR: LOGIC,
        NOT: LOGIC,
    }

    relop_symbols = {
        '==': '==',
        '!=': '!=',
        '<': '<',
        '<=': '<=',
        '>': '>',
        '>=': '>='
    }

    logical_symbols = {
        'and': '&&',
        'or': '||',
        'not': '!',

        '&&': '&&',
        '||': '||',
        '!': '!',
    }

    operator_symbols = {
        # arithmetic
        '+': '+',
        '-': '-',
        '*': '*',
        '/': '/',
        '//': '/',
        '%': '%'
    }

    # all the possible tokens
    tokens = [ID, NUMBER, LOGIC, RELOP, OPERATOR, LPRAN, RPRAN, LBRACE, RBRACE, SEP, ]
    tokens += list(reserved.values())
    # remove duplicate values
    tokens = list(set(tokens))

    # simple tokens regex definition
    t_LPRAN = r'\('
    t_RPRAN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_SEP = r'\,'

    def t_ID(self, t):
        r"""[a-zA-Z_][a-zA-Z_0-9]*"""

        # detect reserved word
        if t.value in self.reserved.keys():
            # detect logical reserved word
            _token_mapped_value = self.reserved.get(t.value)
            if _token_mapped_value == 'LOGIC':
                t.type = 'LOGIC',
                t.value = self.logical_symbols.get(t.value)

            # not logical reserved word
            else:
                t.type = t.value
                t.value = _token_mapped_value
        return t

    def t_NUMBER(self, t):
        r"""\d+\.?\d+"""
        t.type = 'NUMBER'

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
