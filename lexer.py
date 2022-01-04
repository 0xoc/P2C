import ply.lex as lex


class P2CLexer(object):
    def __init__(self):
        self.lexer = lex.lex(module=self)
        print("Lexer build successfully")

    # keyword constants
    IF = 'IF'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    OR = 'OR'
    AND = 'AND'
    ELSE = 'ELSE'
    ELIF = 'ELIF'
    FOR = 'FOR'
    WHILE = 'WHILE'
    RANGE = 'RANGE'
    IN = 'IN'
    NOT = 'NOT'
    BREAK = 'BREAK'
    CONTINUE = 'CONTINUE'

    # relop constants
    LT = 'LT'
    LTE = 'LTE'
    GT = 'GT'
    GTE = 'GTE'
    EQU = 'EQU'
    NEQU = 'NEQU'

    # arithmetic constants
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    TIMES = 'TIMES'
    DIV = 'DIV'
    MOD = 'MOD'

    # token constants
    PLUS_EQUAL = 'PLUS_EQUAL'
    MINUS_EQUAL = 'MINUS_EQUAL'
    TIMES_EQUAL = 'TIMES_EQUAL'
    DIV_EQUAL = 'DIV_EQUAL'

    NUMBER = 'NUMBER'
    ID = 'ID'
    LOGIC = 'LOGIC'
    RELOP = 'RELOP'
    LPRAN = 'LPRAN'
    RPRAN = 'RPRAN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    SEP = 'SEP'
    EQ = 'EQ'
    COLON = 'COLON'

    ASSIGN = 'ASSIGN'
    OPERATOR = 'OPERATOR'
    KEYWORD = 'KEYWORD'

    # reserved words
    reserved = {
        'if': IF,
        'True': TRUE,
        'False': FALSE,
        'or': OR,
        'and': AND,
        'else': ELSE,
        'elif': ELIF,
        'for': FOR,
        'while': WHILE,
        'range': RANGE,
        'in': IN,
        'not': NOT,
        'break': BREAK,
        'continue': CONTINUE,
    }

    # all the possible tokens
    tokens = [ID, NUMBER, EQ,
              GT, GTE, LT, LTE, EQU, NEQU,
              AND, OR, NOT,
              PLUS_EQUAL, TIMES_EQUAL, MINUS_EQUAL, DIV_EQUAL,
              PLUS, MINUS, TIMES, DIV, MOD,
              LPRAN, RPRAN, LBRACE, RBRACE, SEP, COLON, 'COMMENTS']
    tokens += list(reserved.values())
    # remove duplicate values
    tokens = list(set(tokens))

    # simple tokens regex definition
    # arithmetic

    def t_GTE(self, t):
        r'(>=)'
        return t

    def t_EQU(self, t):
        r'(==)'
        return t

    def t_NEQU(self, t):
        r'(\!=)'
        return t

    # logic operators
    def t_AND(self, t):
        r'(&&)'
        return t

    def t_OR(self, t):
        r'(\|\|)'
        return t

    def t_PLUS_EQUAL(self, t):
        r'(\+=)'
        return t

    def t_DIV_EQUAL(self, t):
        r'(/=)'
        return t

    def t_MINUS_EQUAL(self, t):
        r'(\-=)'
        return t

    def t_TIMES_EQUAL(self, t):
        r'(\*=)'
        return t

    def t_PLUS(self, t):
        r'\+'
        return t

    def t_MINUS(self, t):
        r'\-'
        return t

    def t_TIMES(self, t):
        r'\*'
        return t

    def t_MOD(self, t):
        r'%'
        return t

    # relop
    def t_LTE(self, t):
        r'(<=)'
        return t
    def t_LT(self, t):
        r'<'
        return t

    def t_GT(self, t):
        r'>'
        return t

    def t_NOT(self, t):
        r'(\!)'
        return t

    # other
    def t_LPRAN(self, t):
        r'\('
        return t

    def t_RPRAN(self, t):
        r'\)'
        return t

    def t_LBRACE(self, t):
        r'\{'
        return t

    def t_RBRACE(self, t):
        r'\}'
        return t

    def t_SEP(self, t):
        r'\,'
        return t

    def t_EQ(self, t):
        r'\='
        return t

    def t_DIV(self, t):
        r"""(//)|/"""
        t.value = '/'
        return t

    def t_COLON(self, t):
        r':'
        return t

    def t_COMMENTS(self, t):
        r'\#.*|""".*"""|".*"|\'.*\''

    def t_ID(self, t):
        r"""[a-zA-Z_][a-zA-Z_0-9]*"""
        t.type = self.reserved.get(t.value, self.ID)
        if t.type in [self.AND, self.OR, self.NOT]:
            logical_symbols = {'and': '&&', 'or': '||', 'not': '!'}
            t.value = logical_symbols.get(t.value)
        elif t.type in [self.TRUE, self.FALSE]:
            t.value = 1 if t.value == "True" else 0
        return t

    def t_NUMBER(self, t):
        r"""[\+\-]?\d+(\.\d*)?"""
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
                # print(_tokens[i])
            except AssertionError:
                print('***ERROR\n')
                print(_tokens[i])
                print(answer_data[i])
                raise
                _error = True

        if not _error:
            print("[LEXER] Test passed")


if __name__ == '__main__':
    lexer = P2CLexer()

    # test 1
    lexer.test("""
    # number and assignment tests
        ifTrue = -3
        b = +45
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
            a + b
            for i in range(start, stop, step):
                a%b
                while condition != 0:
        else False:
            {
                m = 34
            }
    
    # operator tests
        a + b
        a - b
        a * b
        a / b
        a//b
        a%b
        
        m += n
        m -= n
        m *= n
        m /= n
    
    """, [
        (lexer.ID, 'ifTrue'), (lexer.EQ, '='), (lexer.MINUS, '-'), (lexer.NUMBER, 3),
        (lexer.ID, 'b'), (lexer.EQ, '='), (lexer.PLUS, '+'), (lexer.NUMBER, 45),
        (lexer.AND, '&&'), (lexer.EQ, '='), (lexer.NUMBER, 1.2),
        (lexer.ID, 'andor'), (lexer.EQ, '='), (lexer.NUMBER, 1.2),
        (lexer.ID, 'd'), (lexer.EQ, '='), (lexer.NUMBER, 166.897),
        (lexer.ID, 'm'), (lexer.EQ, '='), (lexer.ID, 'a'),
        (lexer.ID, 'v3'), (lexer.EQ, '='), (lexer.ID, 'variable_Longer'),
        (lexer.ID, 'a'), (lexer.LT, '<'), (lexer.ID, 'b'),
        (lexer.ID, 'other'), (lexer.LTE, '<='), (lexer.NUMBER, 3.3),
        (lexer.ID, 'var'), (lexer.NEQU, '!='), (lexer.ID, 'other'),
        (lexer.NUMBER, 5), (lexer.GT, '>'), (lexer.NUMBER, 6),
        (lexer.NUMBER, 89), (lexer.GTE, '>='), (lexer.NUMBER, 99),
        (lexer.ID, 'a'), (lexer.EQU, '=='), (lexer.ID, 'b'),
        (lexer.ID, 'l1'), (lexer.AND, '&&'), (lexer.ID, 'l2'),
        (lexer.ID, 'l1'), (lexer.AND, '&&'), (lexer.ID, 'l2'),
        (lexer.ID, 'wer'), (lexer.OR, '||'), (lexer.ID, 'rew'),
        (lexer.ID, 'wer'), (lexer.OR, '||'), (lexer.ID, 'rew'),
        (lexer.NOT, '!'), (lexer.ID, 'var'),
        (lexer.NOT, '!'), (lexer.ID, 'var'),
        (lexer.IF, 'if'), (lexer.ID, 'ab'), (lexer.GTE, '>='), (lexer.NUMBER, 454), (lexer.COLON, ':'),
        (lexer.ID, 'a'), (lexer.PLUS, '+'), (lexer.ID, 'b'),

        (lexer.FOR, 'for'), (lexer.ID, 'i'), (lexer.IN, 'in'), (lexer.RANGE, 'range'),
        (lexer.LPRAN, '('),
        (lexer.ID, 'start'),
        (lexer.SEP, ','),
        (lexer.ID, 'stop'),
        (lexer.SEP, ','),
        (lexer.ID, 'step'),
        (lexer.RPRAN, ')'),
        (lexer.COLON, ':'),
        (lexer.ID, 'a'), (lexer.MOD, '%'), (lexer.ID, 'b'),

        (lexer.WHILE, 'while'), (lexer.ID, 'condition'), (lexer.NEQU, '!='), (lexer.NUMBER, 0), (lexer.COLON, ':'),
        (lexer.ELSE, 'else'), (lexer.FALSE, 0), (lexer.COLON, ':'),
        (lexer.LBRACE, '{'),
        (lexer.ID, 'm'), (lexer.EQ, '='), (lexer.NUMBER, 34),
        (lexer.RBRACE, '}'),

        (lexer.ID, 'a'), (lexer.PLUS, '+'), (lexer.ID, 'b'),
        (lexer.ID, 'a'), (lexer.MINUS, '-'), (lexer.ID, 'b'),
        (lexer.ID, 'a'), (lexer.TIMES, '*'), (lexer.ID, 'b'),
        (lexer.ID, 'a'), (lexer.DIV, '/'), (lexer.ID, 'b'),
        (lexer.ID, 'a'), (lexer.DIV, '/'), (lexer.ID, 'b'),
        (lexer.ID, 'a'), (lexer.MOD, '%'), (lexer.ID, 'b'),

        (lexer.ID, 'm'), (lexer.PLUS_EQUAL, '+='), (lexer.ID, 'n'),
        (lexer.ID, 'm'), (lexer.MINUS_EQUAL, '-='), (lexer.ID, 'n'),
        (lexer.ID, 'm'), (lexer.TIMES_EQUAL, '*='), (lexer.ID, 'n'),
        (lexer.ID, 'm'), (lexer.DIV_EQUAL, '/='), (lexer.ID, 'n'),
    ])
