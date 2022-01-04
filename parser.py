import json

from lexer import P2CLexer as __
import ply.yacc as yacc
import re


class P2CParser(object):
    tokens = __.tokens
    _ = __()
    lexer = _.lexer
    precedence = (
        ('nonassoc', 'GTE', 'GT', 'LTE', 'LT', 'EQU', 'NEQU', 'AND', 'OR'),  # Nonassociative operators
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIV', 'MOD'),
        ('right', 'UMINUS', 'UPLUS'),

    )

    def __init__(self):
        self.parser = yacc.yacc(module=self)
        self.parse_tree = None
        self.three_address_code = None

        self.assign_symbols = ['=', '+=', '-=', '*=']
        self.operation_symbols = ['+', '-', '*', '/', '&&', '||',
                                  '==',
                                  '>', '>=', '<', '<=', '!=', '%']
        self.keywords = self._.reserved.keys()

        self.symbol_table = {}

        self.t_number = 0
        self.l_number = 0

    def get_temp(self):
        self.t_number += 1
        return "t%d" % self.t_number

    def get_label(self):
        self.l_number += 1
        return "l%d" % self.l_number

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
        p[0] = tuple((p[1], p[2], p[6], p[10]))

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

    def p_exr_unary_minus(self, p):
        """
         expr : MINUS expr %prec UMINUS
        """
        p[0] = tuple((p[1], p[2]))

    def p_exr_unary_plus(self, p):
        """
         expr : PLUS expr %prec UPLUS
        """
        p[0] = tuple((p[1], p[2]))

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

    def get_tac(self, line):
        if type(line) != tuple:
            return "", line

        if line[0] in self.assign_symbols:
            return self.tac_assign(line)

        elif line[0] in self.operation_symbols and len(line) == 3:
            return self.tac_operator(line)
        elif line[0] in self.operation_symbols and len(line) == 2:
            return self.tac_operator_unary(line)
        elif line[0] == 'if':
            return self.tac_if_elif_else(line)
        elif line[0] == 'while':
            return self.tac_while(line)
        elif line[0] == 'for':
            return self.tac_for(line)
        else:
            raise Exception("Invalid line: %s" % str(line))

    def tac_for(self, line):
        for_var = line[1]
        start, end, step = line[2]
        statements = self.tac_program(line[3])

        start_label = self.get_label()
        end_label = self.get_label()

        structure = ""

        # define for variable if not defined before
        if for_var not in self.symbol_table:
            structure += f"float {for_var};\n"
            self.symbol_table[for_var] = 'float'

        # initialize the for variable
        structure += f"{for_var} = {start};\n"
        op = '>=' if step > 0 else '<='

        structure += f"{start_label}:\n" \
                     f"if ({for_var} {op} {end}) goto {end_label};\n" \
                     f"{statements}\n" \
                     f"{for_var} += {step};\n" \
                     f"goto {start_label};\n" \
                     f"{end_label}:;\n"
        return structure, None

    def tac_while(self, line):
        condition = line[1]
        statements = line[2]

        condition_tac_str, condition_root = self.get_tac(condition)
        statements_tac_str = self.tac_program(statements)

        start_label = self.get_label()
        end_label = self.get_label()

        structure = f"{start_label}: \n" \
                    f"if (!{condition_root}) goto {end_label};\n" \
                    f"{statements_tac_str}\n" \
                    f"goto {start_label};\n" \
                    f"{end_label}:;\n"

        return condition_tac_str + structure, None

    def tac_if_elif_else(self, line):
        data = []
        _line = line
        while _line:
            keyword = _line[0]

            if keyword == 'else':
                data.append({
                    'keyword': 'else',
                    'statements': self.tac_program(_line[1])
                })
                break

            if keyword == 'elif':
                keyword = 'else if'
            data.append({
                'keyword': keyword,
                'condition': self.get_tac(_line[1]),
                'statements': self.tac_program(_line[2])
            })

            _line = _line[3]

        # all the conditions first
        conditions = ""
        structure = ""
        if_done_label = self.get_label()

        for part in data:
            keyword = part.get('keyword')
            if keyword == 'else':
                structure += f"{part.get('statements')}\n"
                continue
            _condition, condition_root = part.get('condition')
            conditions += f"{_condition}\n"

            statements_end = self.get_label()

            structure += f"if (!{condition_root}) goto {statements_end};\n" \
                         f"{part.get('statements')}\n" \
                         f"goto {if_done_label};\n" \
                         f"{statements_end}:;\n"

        structure += f"{if_done_label}:;\n"
        return conditions + structure, None

    def tac_operator_unary(self, line):
        a = line[1]
        op = line[0]
        a_tac_str, a_root = self.get_tac(a)
        temp = self.get_temp()
        return a_tac_str + f"float {temp} = {op}{a_root};\n", temp

    def tac_operator(self, line):
        a = line[1]
        b = line[2]
        op = line[0]

        a_tac_str, a_root = self.get_tac(a)
        b_tac_str, b_root = self.get_tac(b)

        temp = self.get_temp()

        _str = a_tac_str + b_tac_str
        _str += f"float {temp} = {a_root} {op} {b_root};\n"

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
        tac_str = f"{_type}{lhs} {op} {rhs_root};\n"
        return rhs_str + tac_str, lhs

    def tac_program(self, program):
        if not program:
            return "\n"
        result = ""
        for line in program:
            _line, root = self.get_tac(line)
            result += _line

        return result

    def generate_three_address_code(self):
        body = self.tac_program(self.parse_tree)
        c_tac_code = "#include <stdio.h>\nint main () {\n%s\nreturn 0;\n}" % body
        c_tac_code = re.sub(' +', ' ', c_tac_code)
        c_tac_code = re.sub('\n+', '\n', c_tac_code)
        return c_tac_code

    def test(self, input_data):
        print(self.parse(input_data))


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

             ('for', 'i', ('a', 'b', 2.0), 
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
    result = _parser.parse(test_input)

    # clean result
    result = str(result).replace(' ', '').replace('\n', '')
    return test_output == result


if __name__ == '__main__':
    if not test_parse_tree_generation():
        raise Exception("[PARSER] Parse tree test filed")

    parser = P2CParser()
    _input = open('program.py.txt')
    test_input = _input.read()
    parser.parse(test_input)
    _out = open('program.c', 'w')
    _out.write(parser.generate_three_address_code())
    _input.close()
    _out.close()
