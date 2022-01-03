    """
statements: ID EQ expression
                |   if expression COLON LBRACE statements RBRACE elsestatement
                |   WHILE expression COLON LBRACE statements RBRACE
                |   FOR ID IN RANGE LPRAN NUMBER RPRAN COLON LBRACE statements RBRACE
                | statements
    EXPRSTMT: EXPRSTMT OPERATOR EXPRSTMT
            | EXPRSTMT RELOP EXPRSTMT
            | (EXPR)
            | ID
            | NUMBER

        ELIFSTMT: ELIF EXPR COLON LBRACE STATEMENTS RBRACE ELIFSTMT
                | ELSE COLON LBRACE STATEMENTS RBRACE
                | EMPTY
"""