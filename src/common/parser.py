from ply import yacc
from ply.yacc import LRParser

from common.lexer import Lexer
from common.util import Program, Variable, Paragraph, Statement


class Parser:
    tokens = Lexer.tokens

    def __init__(self):
        self.lexer = Lexer()
        self.lexer.build()
        self.parser = None
        self.program = None
        self.current_paragraph = None

    def p_program(self, p):
        '''program : identification_division data_division procedure_division'''
        self.program = Program(name=p[1], variables=p[2], paragraphs=p[3])
        p[0] = self.program

    def p_identification_division(self, p):
        '''identification_division : IDENTIFICATION DIVISION DOT PROGRAM_ID DOT IDENTIFIER DOT'''
        p[0] = p[6]

    # Data Division
    def p_data_division(self, p):
        '''data_division : DATA DIVISION DOT WORKING_STORAGE SECTION DOT variable_list
                        | DATA DIVISION DOT'''
        if len(p) == 8:
            p[0] = p[7]
        else:
            p[0] = []

    def p_variable_list(self, p):
        '''variable_list : variable_list variable
                        | variable'''
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    def p_variable(self, p):
        '''variable : NUMBER IDENTIFIER picture_clause value_clause DOT
                   | NUMBER IDENTIFIER picture_clause DOT
                   | NUMBER IDENTIFIER value_clause DOT
                   | NUMBER IDENTIFIER DOT'''
        level = int(p[1])
        var = Variable(level=level, name=p[2])
        for i in range(3, len(p)):
            if isinstance(p[i], dict):
                if 'picture' in p[i]:
                    var.picture = p[i]['picture']
                if 'value' in p[i]:
                    var.value = p[i]['value']
        p[0] = var

    def p_picture_clause(self, p):
        '''picture_clause : PIC picture_string
                         | PICTURE picture_string'''
        p[0] = {'picture': p[2]}

    def p_picture_string(self, p):
        '''picture_string : IDENTIFIER
                         | IDENTIFIER LPAREN NUMBER RPAREN
                         | IDENTIFIER LPAREN NUMBER RPAREN IDENTIFIER
                         | IDENTIFIER LPAREN NUMBER RPAREN IDENTIFIER LPAREN NUMBER RPAREN
                         | NUMBER LPAREN NUMBER RPAREN
                         | NUMBER LPAREN NUMBER RPAREN IDENTIFIER
                         | NUMBER LPAREN NUMBER RPAREN IDENTIFIER LPAREN NUMBER RPAREN
                         | NUMBER LPAREN NUMBER RPAREN IDENTIFIER NUMBER LPAREN NUMBER RPAREN'''
        # Reconstruct the picture string from the tokens
        pic_str = ''
        for i in range(1, len(p)):
            if p[i] == '(':
                pic_str += '('
            elif p[i] == ')':
                pic_str += ')'
            else:
                pic_str += str(p[i])
        p[0] = pic_str

    def p_value_clause(self, p):
        '''value_clause : VALUE NUMBER
                       | VALUE STRING
                       | VALUE IDENTIFIER'''
        p[0] = {'value': str(p[2])}

    # Procedure Division
    def p_procedure_division(self, p):
        '''procedure_division : PROCEDURE DIVISION DOT paragraph_list'''
        p[0] = p[4]

    def p_paragraph_list(self, p):
        '''paragraph_list : paragraph_list paragraph
                         | paragraph'''
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    def p_paragraph(self, p):
        '''paragraph : IDENTIFIER DOT statement_list'''
        p[0] = Paragraph(name=p[1], statements=p[3])

    def p_statement_list(self, p):
        '''statement_list : statement_list statement
                         | statement
                         | empty'''
        if p[1] is None:
            p[0] = []
        elif len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    # Statements
    def p_statement_move(self, p):
        '''statement : MOVE IDENTIFIER TO IDENTIFIER DOT
                    | MOVE NUMBER TO IDENTIFIER DOT
                    | MOVE STRING TO IDENTIFIER DOT'''
        p[0] = Statement('MOVE', {'source': str(p[2]), 'target': p[4]})

    def p_statement_add(self, p):
        '''statement : ADD IDENTIFIER TO IDENTIFIER DOT
                    | ADD NUMBER TO IDENTIFIER DOT
                    | ADD IDENTIFIER TO IDENTIFIER GIVING IDENTIFIER DOT'''
        if len(p) == 6:
            p[0] = Statement('ADD', {'operand1': str(p[2]), 'operand2': p[4], 'target': p[4]})
        else:
            p[0] = Statement('ADD', {'operand1': str(p[2]), 'operand2': p[4], 'target': p[6]})

    def p_statement_subtract(self, p):
        '''statement : SUBTRACT IDENTIFIER FROM IDENTIFIER DOT
                    | SUBTRACT NUMBER FROM IDENTIFIER DOT
                    | SUBTRACT IDENTIFIER FROM IDENTIFIER GIVING IDENTIFIER DOT
                    | SUBTRACT NUMBER FROM IDENTIFIER GIVING IDENTIFIER DOT
                    | SUBTRACT IDENTIFIER FROM IDENTIFIER
                    | SUBTRACT NUMBER FROM IDENTIFIER
                    | SUBTRACT IDENTIFIER FROM IDENTIFIER GIVING IDENTIFIER
                    | SUBTRACT NUMBER FROM IDENTIFIER GIVING IDENTIFIER
                    '''
        if len(p) == 6:
            p[0] = Statement('SUBTRACT', {'operand1': str(p[2]), 'operand2': p[4], 'target': p[4]})
        else:
            p[0] = Statement('SUBTRACT', {'operand1': str(p[2]), 'operand2': p[4], 'target': p[6]})

    def p_statement_multiply(self, p):
        '''statement : MULTIPLY IDENTIFIER BY IDENTIFIER DOT
                    | MULTIPLY NUMBER BY IDENTIFIER DOT
                    | MULTIPLY IDENTIFIER BY IDENTIFIER GIVING IDENTIFIER DOT
                    | MULTIPLY NUMBER BY IDENTIFIER GIVING IDENTIFIER DOT
                    | MULTIPLY IDENTIFIER BY NUMBER GIVING IDENTIFIER DOT
                    | MULTIPLY NUMBER BY NUMBER GIVING IDENTIFIER DOT
                    '''
        p[0] = Statement('MULTIPLY', {'operand1': str(p[2]), 'operand2': p[4], 'target': p[4]})

    def p_statement_compute(self, p):
        '''statement : COMPUTE IDENTIFIER EQUALS expression_list DOT
                     | COMPUTE IDENTIFIER EQUALS expression_list
                     '''
        p[0] = Statement('COMPUTE', {'target': p[2], 'expression': p[4]})

    def p_expression_list(self, p):
        '''expression_list : expression_list expression_term
                          | expression_term'''
        if len(p) == 3:
            p[0] = p[1] + ' ' + p[2]
        else:
            p[0] = p[1]

    def p_expression_term(self, p):
        '''expression_term : IDENTIFIER
                          | NUMBER
                          | PLUS
                          | MINUS
                          | TIMES
                          | DIVIDE
                          | LPAREN
                          | RPAREN'''
        p[0] = str(p[1])

    def p_statement_perform(self, p):
        '''statement : PERFORM IDENTIFIER DOT
                    | PERFORM IDENTIFIER THRU IDENTIFIER DOT
                    | PERFORM IDENTIFIER UNTIL condition DOT'''
        if len(p) == 4:
            p[0] = Statement('PERFORM', {'target': p[2]})
        elif len(p) == 6 and p[3] == 'THRU':
            p[0] = Statement('PERFORM', {'target': p[2], 'thru': p[4]})
        else:
            p[0] = Statement('PERFORM', {'target': p[2], 'until': p[4]})

    def p_condition(self, p):
        '''condition : IDENTIFIER GT NUMBER
                    | IDENTIFIER LT NUMBER
                    | IDENTIFIER EQUALS NUMBER
                    | IDENTIFIER GE NUMBER
                    | IDENTIFIER LE NUMBER
                    | IDENTIFIER GT IDENTIFIER
                    | IDENTIFIER LT IDENTIFIER
                    | IDENTIFIER EQUALS IDENTIFIER
                    | IDENTIFIER GE IDENTIFIER
                    | IDENTIFIER LE IDENTIFIER'''
        p[0] = f"{p[1]} {p[2]} {p[3]}"

    def p_statement_if(self, p):
        '''statement : IF condition THEN statement_list END_IF DOT
                    | IF condition statement_list END_IF DOT
                    | IF condition THEN statement_list ELSE statement_list END_IF DOT'''
        if len(p) == 7:
            p[0] = Statement('IF', {'condition': p[2], 'then': p[4]})
        elif len(p) == 6:
            p[0] = Statement('IF', {'condition': p[2], 'then': p[3]})
        else:
            p[0] = Statement('IF', {'condition': p[2], 'then': p[4], 'else': p[6]})

    def p_statement_display(self, p):
        '''statement : DISPLAY IDENTIFIER DOT
                    | DISPLAY STRING DOT
                    | DISPLAY NUMBER DOT'''
        p[0] = Statement('DISPLAY', {'item': str(p[2])})

    def p_statement_stop(self, p):
        '''statement : STOP RUN DOT
                    | EXIT DOT
                    | GOBACK DOT'''
        p[0] = Statement('STOP', {})

    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}' (line {p.lineno})")
        else:
            print("Syntax error at EOF")

    def build(self, **kwargs) -> LRParser:
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

    def parse(self, code):
        self.parser.parse(code, lexer=self.lexer.lexer, tracking=True)
        return self.program

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} <filename>', file=sys.stderr )
        raise SystemExit
    else:
        data = open( sys.argv[1] ).read()
        parser = Parser()
        parser.build(debug=True)
        program = parser.parse(data)
        # result = parser.parse(data, lexer=lexer.lexer, debug=False )
        # treeprint(result, 'unicode')
        print( 'Program ok.' , program)
