import ply.lex as lex


class P2CLexer(object):
    def __init__(self):
        self.lexer = None

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
    tokens = [ID, NUMBER, LOGIC, RELOP, OPERATOR, LPRAN, RPRAN, LBRACE, RBRACE, SEP]
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
        t.type = self.reserved.get(t.value, self.ID)
        if t.type == self.LOGIC:
            t.value = self.logical_symbols.get(t.value)

        return t

    def t_NUMBER(self, t):
        r"""\d+\.?\d+"""
        t.type = self.NUMBER
        t.value = float(t.value)
        return t

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Define a rule so we can track line numbers
    @staticmethod
    def t_newline(t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)
        # Error handling rule

    @staticmethod
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])

    # Builds the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


lexer = P2CLexer()
lexer.build()  # Build the lexer
lexer.test("""
sina
87
23423423.435
ali parvizi
for not
and
or ||
""")  # Test it


