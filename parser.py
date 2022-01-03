from lexer import P2CLexer as __
import ply.yacc as yacc


class P2CParser(object):
    tokens = __.tokens
    _ = __()
    lexer = _.lexer

    def __init__(self):
        self.parser = yacc.yacc(module=self)

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
            print(p[0])

    def p_statement(self, p):
        """
        statement : assignment
        | if
        | expr
        """
        p[0] = p[1]

    def p_if(self, p):
        """
        if : IF expr COLON LBRACE statements RBRACE
        """
        p[0] = tuple((p[1], p[2], p[5]))

    def p_assignment(self, p):
        """
        assignment : ID EQ expr
        """
        p[0] = tuple((p[2], p[1], p[3]))

    def p_expr_operator_relop(self, p):
        """
        expr : expr operator expr
        | expr relop expr
        | expr logic expr
        | ID
        | NUMBER
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
        result = self.parser.parse(input_data, lexer=self.lexer)


parser = P2CParser()
parser.test("""
(a + b) * 4 + c
a + b
m + n

if a > b : 
{
    passed = True
    m = a + b
}

""")
