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
    EQ = 'EQ'

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
    tokens = [ID, NUMBER, EQ, LOGIC, RELOP, OPERATOR, LPRAN, RPRAN, LBRACE, RBRACE, SEP, 'COMMENTS']
    tokens += list(reserved.values())
    # remove duplicate values
    tokens = list(set(tokens))

    # simple tokens regex definition
    t_LPRAN = r'\('
    t_RPRAN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_SEP = r'\,'
    t_EQ = r'\='

    def t_COMMENTS(self, t):
        r'\#.*|""".*"""|".*"|\'.*\''

    def t_ID(self, t):
        r"""[a-zA-Z_][a-zA-Z_0-9]*"""
        t.type = self.reserved.get(t.value, self.ID)
        if t.type == self.LOGIC:
            t.value = self.logical_symbols.get(t.value)

        return t

    def t_NUMBER(self, t):
        r"""\d+(\.\d*)?"""
        t.type = self.NUMBER
        t.value = float(t.value)
        return t

    def t_LOGIC(self, t):
        r"""(\|\|)|\!|(&&)"""
        return t

    def t_RELOP(self, t):
        r"""(>=)|>|(<=)|<|(==)|(\!=)"""
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
    def test(self, input_data, answer_data):
        self.lexer.input(input_data)
        _tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            _tokens.append(tok)

        for i in range(len(answer_data)):
            assert _tokens[i].type == answer_data[i][0] and _tokens[i].value == answer_data[i][1]

        for _token in _tokens:
            print(_token)


lexer = P2CLexer()
lexer.build()  # Build the lexer

# test 1
lexer.test("""
# number and assignment tests

a = 3
b = 45
c = 1.2
\"\"\"\check for float number"\"\"
d = 166.897
m = a
"check longer variable"
v3 = variable_Longer

'comparison tests'

a < b
""", [
    (lexer.ID, 'a'), (lexer.EQ, '='), (lexer.NUMBER, 3),
    (lexer.ID, 'b'), (lexer.EQ, '='), (lexer.NUMBER, 45),
    (lexer.ID, 'c'), (lexer.EQ, '='), (lexer.NUMBER, 1.2),
    (lexer.ID, 'd'), (lexer.EQ, '='), (lexer.NUMBER, 166.897),
    (lexer.ID, 'm'), (lexer.EQ, '='), (lexer.ID, 'a'),
    (lexer.ID, 'v3'), (lexer.EQ, '='), (lexer.ID, 'variable_Longer'),
    (lexer.ID, 'a'), (lexer.RELOP, '<'), (lexer.ID, 'b'),

])  # Test it
