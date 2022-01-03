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
        params : num_or_id
            |   num_or_id SEP num_or_id
            | num_or_id SEP num_or_id SEP num_or_id
        """
        if len(p) == 2:
            p[0] = tuple((0, p[1], 1))
        elif len(p) == 4:
            p[0] = tuple((p[1], p[3], 1))
        elif len(p) == 6:
            p[0] = tuple((p[1], p[3], p[5]))

    def p_num_or_id(self, p):
        """
        num_or_id : NUMBER
                | ID
        """
        p[0] = p[1]

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

    def parse(self, input_data):
        self.parser.parse(input_data, lexer=self.lexer)
        return self.parse_tree

    def test(self, input_data):
        print(self.parse(input_data))


parser = P2CParser()
parser.test("""
a = 10
b = 120

while a < b: {
    if a == 20: { continue }
    a += 1
}   

# a should be 120 by now

b *= 2  # b = 240
c = 0

for i in range(a, b, 2): {
    c = i + a
    if c > 200 : { break }
    elif c == 200 : { continue }
    else: {} 
}

result = 24 * ((a+b)-c/10)

""")
"""

[
    ('=', 'a', 10.0), 
    ('=', 'b', 120.0),
    ('while', ('<', 'a', 'b'), 
        [
            ('if', ('==', 'a', 20.0), ['continue'], None), 
            ('+=', 'a', 1.0)
        ]), 
     
     ('*=', 'b', 2.0), 
     ('=', 'c', 0.0), 
     
     ('for', ('a', 'b', 2.0), 
         [
            ('=', 'c', ('+', 'i', 'a')),
            ('if', ('>', 'c', 200.0), ['break'], ('elif', ('==', 'c', 200.0), ['continue'], ('else', None)))
          ]), 
      ('=', 'result', ('*', 24.0, ('-', ('+', 'a', 'b'), ('/', 'c', 10.0))))
]

"""