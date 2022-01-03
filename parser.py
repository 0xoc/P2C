from lexer import P2CLexer as __
import ply.yacc as yacc


class P2CParser(object):
    tokens = __.tokens
    _ = __()
    lexer = _.lexer

    def __init__(self):
        self.parser = yacc.yacc(module=self)
        self.parse_tree = None

    precedence = (
        ('nonassoc', 'GTE', 'GT', 'LTE', 'LT', 'EQU', 'NEQU', 'AND', 'OR'),  # Nonassociative operators
        ('right', 'PLUS', 'MINUS'),
        ('right', 'TIMES', 'DIV', 'MOD'),
        ('right', 'NOT'),
    )

    def p_statements(self, p):
        """
        statements : statements statement
        | empty
        """
        if len(p) == 3:
            if not p[1]:
                p[1] = []
            p[0] = p[1] + [p[2]]
            self.parse_tree = p[0]

    def p_statement(self, p):
        """
        statement : assignment
        | if
        | while
        | for
        | expr
        | CONTINUE
        | BREAK
        """
        p[0] = p[1]

    def p_for(self, p):
        """
        for : FOR ID IN RANGE LPRAN params RPRAN COLON LBRACE statements RBRACE
        """
        p[0] = tuple((p[1], p[6], p[10]))

    def p_params(self, p):
        """
        params : NUMBER
            |   NUMBER SEP NUMBER
            | NUMBER SEP NUMBER SEP NUMBER
        """
        if len(p) == 2:
            p[0] = tuple((0, p[1], 1))
        elif len(p) == 4:
            p[0] = tuple((p[1], p[3], 1))
        elif len(p) == 6:
            p[0] = tuple((p[1], p[3], p[5]))

    def p_while(self, p):
        """
        while : WHILE expr COLON LBRACE statements RBRACE
        """
        p[0] = tuple((p[1], p[2], p[5]))

    def p_if(self, p):
        """
        if : IF expr COLON LBRACE statements RBRACE elif
        """
        p[0] = tuple((p[1], p[2], p[5], p[7]))

    def p_elif(self, p):
        """
        elif : ELIF expr COLON LBRACE statements RBRACE elif
        | else
        """
        if len(p) != 2:
            p[0] = tuple((p[1], p[2], p[5], p[7]))
        else:
            p[0] = p[1]

    def p_else(self, p):
        """
        else : ELSE COLON LBRACE statements RBRACE
        | empty
        """
        if len(p) != 2:
            p[0] = tuple((p[1], p[4]))

    def p_assignment(self, p):
        """
        assignment : ID EQ expr
                   | ID PLUS_EQUAL expr
                   | ID MINUS_EQUAL expr
                   | ID TIMES_EQUAL expr
        """
        p[0] = tuple((p[2], p[1], p[3]))

    def p_expr_operator_relop(self, p):
        """
        expr : expr operator expr
        | expr relop expr
        | expr logic expr
        | ID
        | NUMBER
        | TRUE
        | FALSE
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = tuple([p[2], p[1], p[3]])

    def p_operator(self, p):
        """
        operator : TIMES
                | DIV
                |  PLUS
                |  MINUS
                |  MOD
        """
        p[0] = p[1]

    def p_logic(self, p):
        """
        logic : AND
              | OR
        """
        p[0] = p[1]

    def p_relop(self, p):
        """
        relop : LT
                | LTE
                |  GT
                |  GTE
                |  EQU
                |  NEQU
        """
        p[0] = p[1]

    def p_expr_pran(self, p):
        """
        expr : LPRAN expr RPRAN
        """
        p[0] = p[2]

    def p_empty(self, p):
        'empty :'
        p[0] = None

    def test(self, input_data):
        self.parser.parse(input_data, lexer=self.lexer)
        for tree in self.parse_tree:
            print(tree)



parser = P2CParser()
parser.test("""
(a + b) * 4 + c
a + b
m + n

if a > b : 
{
    passed = True
    m = a + b
} elif a == b: {
    passed = False
    m = a - b
} elif a < b : {
    m = a
} else: {
    a = 0
    b = 0
    m = 0
}

while True : {
    if a > b: {
        break
    } elif a ==b : {continue}
    else : {
        a+= 1
    }
}

for i in range(10, 20, 2): {
    a += i
    }
""")
