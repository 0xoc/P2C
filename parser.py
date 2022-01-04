import json

from lexer import P2CLexer as __
import ply.yacc as yacc


class P2CParser(object):
    tokens = __.tokens
    _ = __()
    lexer = _.lexer
    precedence = (
        ('nonassoc', 'GTE', 'GT', 'LTE', 'LT', 'EQU', 'NEQU', 'AND', 'OR'),  # Nonassociative operators
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIV', 'MOD'),

    )

    def build(self):
        self.parser = yacc.yacc(module=self)

    def __init__(self):
        self.parser = None
        self.parse_tree = None
        self.three_address_code = None

        self.assign_symbols = ['=', '+=', '-=', '*=']
        self.operation_symbols = ['+', '-', '*', '/', '&&', '||',
                                  '>', '>=', '<', '<=', '!=', '%']
        self.keywords = self._.reserved.keys()

        self.symbol_table = {}

        self.t_number = 0

    def get_temp(self):
        self.t_number += 1
        return "t%d" % self.t_number

    # grammar rules start *********************

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
                   | ID DIV_EQUAL expr
        """
        p[0] = tuple((p[2], p[1], p[3]))

    def p_expr_operator_relop(self, p):
        """
        expr : expr PLUS expr
        | expr MINUS expr
        | expr TIMES expr
        | expr DIV expr
        | expr MOD expr
        | expr AND expr
        | expr OR expr
        | expr LT expr
        | expr LTE expr
        | expr GT expr
        | expr GTE expr
        | expr EQU expr
        | expr NEQU expr
        | ID
        | NUMBER
        | TRUE
        | FALSE
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = tuple([p[2], p[1], p[3]])

    def p_expr_pran(self, p):
        """
        expr : LPRAN expr RPRAN

        """
        p[0] = p[2]

    def p_num_or_id(self, p):
        """
        num_or_id : NUMBER
                | ID
        """
        p[0] = p[1]

    def p_empty(self, p):
        'empty :'
        p[0] = None

    # grammar rules end $$$$$$$$$$$$$$$$$$$$

    def parse(self, input_data):
        self.parser.parse(input_data, lexer=self.lexer)
        return self.parse_tree

    def tac_id_or_num(self, _id_or_num):
        return _id_or_num

    def get_tac(self, line):
        if type(line) != tuple:
            return "", line

        if line[0] in self.assign_symbols:
            return self.tac_assign(line)

        elif line[0] in self.operation_symbols and len(line) == 3:
            return self.tac_operator(line)
        elif line[0] in self.operation_symbols and len(line) == 2:
            return self.tac_operator_unary(line)
        else:
            raise Exception("Invalid line: %s" % str(line))

    def tac_operator_unary(self, line):
        a = line[1]
        op = line[0]
        a_tac_str, a_root = self.get_tac(a)
        temp = self.get_temp()
        return a_tac_str + f"float {temp} = {op}{a_root}\n", temp

    def tac_operator(self, line):
        a = line[1]
        b = line[2]
        op = line[0]

        a_tac_str, a_root = self.get_tac(a)
        b_tac_str, b_root = self.get_tac(b)

        temp = self.get_temp()

        _str = a_tac_str + b_tac_str
        _str += f"float {temp} = {a_root} {op} {b_root}\n"

        return _str, temp

    def tac_assign(self, line):
        lhs = line[1]
        rhs = line[2]
        op = line[0]

        if lhs in self.symbol_table.keys():
            # symbol defined before, no need to add type
            _type = ''
        else:
            _type = 'float '
            self.symbol_table[lhs] = 'float'

        rhs_str, rhs_root = self.get_tac(rhs)
        tac_str = f"{_type}{lhs} {op} {rhs_root}\n"
        return rhs_str + tac_str, lhs

    def generate_three_address_code(self):
        result = ""
        for line in self.parse_tree:
            _str, _root = self.get_tac(line)
            result += _str
        return result

    def test(self, input_data):
        print(self.parse(input_data))


class Parser2(object):
    tokens = P2CParser.tokens
    _ = __()
    lexer = _.lexer

    precedence = [
        ('left', 'PLUS'),
    ]

    def p_expr(self, p):
        """
        expr : expr PLUS expr
        | empty
        """
        if len(p) == 4:
            p[0] = tuple((p[2], p[1], p[3]))
            self.parse_tree = p[0]

    def p_op(self, p):
        """
        op : PLUS
        """
        p[0] = p[1]

    def p_expr_terminal(self, p):
        """
        expr : ID
            | NUMBER
        """
        p[0] = p[1]

    def p_empty(self, p):
        """empty : """
        p[0] = None

    def __init__(self):
        self.parser = yacc.yacc(module=self)
        self.parse_tree = None

    def parse(self, input_data):
        self.parser.parse(input_data, lexer=self.lexer)
        print(self.parse_tree)


def test_parse_tree_generation():
    test_input = """
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

        """
    test_output = """

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

    # clean test_output
    test_output = test_output.replace(' ', '').replace('\n', '')

    _parser = P2CParser()
    _parser.build()
    result = _parser.parse(test_input)

    # clean result
    result = str(result).replace(' ', '').replace('\n', '')

    return test_output == result


if __name__ == '__main__':
    # p2 = Parser2()
    # p2.parse("""
    # a + 4
    # """)

    if not test_parse_tree_generation():
        raise Exception("[PARSER] Parse tree test filed")

    # parser = P2CParser()
    # test_input = """
    # a = 3+-3*4+-(7*8/2)
    # """
    # parser.parse(test_input)
    # print(parser.generate_three_address_code())
