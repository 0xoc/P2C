from lexer import P2CLexer as __
import ply.yacc as yacc


class P2CParser(object):
    tokens = __.tokens
    _ = __()
    lexer = _.lexer

    def __init__(self):
        self.parser = yacc.yacc(module=self)

    def p_program_assignment(self, p):
        f"""
        program : {self._.ID} {self._.EQ} expr
        | expr
        | empty
        """
        if len(p) == 4:
            p[0] = ['=', p[1], p[3]]
        elif len(p) == 2:
            p[0] = p[1]
        print(p[0])

    def p_expr_operator_relop(self, p):
        """
        expr : expr OPERATOR expr
        | expr RELOP expr
        | expr LOGIC expr
        | ID
        | NUMBER
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = [p[2], p[1], p[3]]

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
(a + b) + c and 5
""")
