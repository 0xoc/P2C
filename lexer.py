import ply.lex as lex


class P2CLexer(object):
    def __init__(self):
        self.lexer = None

    # keyword constants
    IF = 'if'
    TRUE = 'True'
    FALSE = 'False'
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
    COLON = 'COLON'

    # reserved words
    reserved = {
        TRUE: TRUE,
        FALSE: FALSE,
        IF: IF,
        ELSE: ELSE,
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
    tokens = [ID, NUMBER, EQ, LOGIC, RELOP, OPERATOR, LPRAN, RPRAN, LBRACE, RBRACE, SEP, 'COMMENTS', COLON]
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

    def t_COLON(self, t):
        r':'
        return t

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

    def t_RELOP(self, t):
        r"""(>=)|>|(<=)|<|(==)|(\!=)"""
        return t

    def t_LOGIC(self, t):
        r"""(\|\|)|\!|(&&)"""
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

        _error = False
        for i in range(len(_tokens)):
            try:
                assert _tokens[i].type == answer_data[i][0] and _tokens[i].value == answer_data[i][1]
                print(_tokens[i])
            except AssertionError:
                print('***ERROR\n')
                print(_tokens[i].type, answer_data[i][0], " | ", _tokens[i].value, answer_data[i][1])
                _error = True

        if not _error:
            print("[TEST] No Errors")


lexer = P2CLexer()
lexer.build()  # Build the lexer

# test 1
lexer.test("""
# number and assignment tests
    ifTrue = 3
    b = 45
    and = 1.2
    andor = 1.2
    d = 166.897
    m = a
    v3 = variable_Longer

# relop tests

    a < b
    other <= 3.3
    var != other
    5 > 6
    89 >= 99
    a == b

# logic test
    l1 and l2
    l1 && l2
    
    wer or rew
    wer || rew
    not var
    !var

# keyword tests
    
    if ab >= 454:
        for i in range(start, stop, step):
            while True:
    else False:
        {
            m = 34
        }

""", [
    (lexer.ID, 'ifTrue'), (lexer.EQ, '='), (lexer.NUMBER, 3),
    (lexer.ID, 'b'), (lexer.EQ, '='), (lexer.NUMBER, 45),
    (lexer.LOGIC, '&&'), (lexer.EQ, '='), (lexer.NUMBER, 1.2),
    (lexer.ID, 'andor'), (lexer.EQ, '='), (lexer.NUMBER, 1.2),
    (lexer.ID, 'd'), (lexer.EQ, '='), (lexer.NUMBER, 166.897),
    (lexer.ID, 'm'), (lexer.EQ, '='), (lexer.ID, 'a'),
    (lexer.ID, 'v3'), (lexer.EQ, '='), (lexer.ID, 'variable_Longer'),
    (lexer.ID, 'a'), (lexer.RELOP, '<'), (lexer.ID, 'b'),
    (lexer.ID, 'other'), (lexer.RELOP, '<='), (lexer.NUMBER, 3.3),
    (lexer.ID, 'var'), (lexer.RELOP, '!='), (lexer.ID, 'other'),
    (lexer.NUMBER, 5), (lexer.RELOP, '>'), (lexer.NUMBER, 6),
    (lexer.NUMBER, 89), (lexer.RELOP, '>='), (lexer.NUMBER, 99),
    (lexer.ID, 'a'), (lexer.RELOP, '=='), (lexer.ID, 'b'),
    (lexer.ID, 'l1'), (lexer.LOGIC, '&&'), (lexer.ID, 'l2'),
    (lexer.ID, 'l1'), (lexer.LOGIC, '&&'), (lexer.ID, 'l2'),
    (lexer.ID, 'wer'), (lexer.LOGIC, '||'), (lexer.ID, 'rew'),
    (lexer.ID, 'wer'), (lexer.LOGIC, '||'), (lexer.ID, 'rew'),
    (lexer.LOGIC, '!'), (lexer.ID, 'var'),
    (lexer.LOGIC, '!'), (lexer.ID, 'var'),
    (lexer.IF, 'if'), (lexer.ID, 'ab'), (lexer.RELOP, '>='), (lexer.NUMBER, 454), (lexer.COLON, ':'),

    (lexer.FOR, 'for'), (lexer.ID, 'i'), (lexer.IN, 'in'), (lexer.RANGE, 'range'),
    (lexer.LPRAN, '('),
    (lexer.ID, 'start'),
    (lexer.SEP, ','),
    (lexer.ID, 'stop'),
    (lexer.SEP, ','),
    (lexer.ID, 'step'),
    (lexer.RPRAN, ')'),
    (lexer.COLON, ':'),

    (lexer.WHILE, 'while'), (lexer.TRUE, 'True'), (lexer.COLON, ':'),
    (lexer.ELSE, 'else'), (lexer.FALSE, 'False'), (lexer.COLON, ':'),
    (lexer.LBRACE, '{'),
    (lexer.ID, 'm'), (lexer.EQ, '='),  (lexer.NUMBER, 34),
    (lexer.RBRACE, '}'),

])
