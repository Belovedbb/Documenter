import sys

import ply.lex

class Lexer:
    reserved = {
        'IDENTIFICATION': 'IDENTIFICATION',
        'DIVISION': 'DIVISION',
        'PROGRAM-ID': 'PROGRAM_ID',
        'DATA': 'DATA',
        'WORKING-STORAGE': 'WORKING_STORAGE',
        'SECTION': 'SECTION',
        'PIC': 'PIC',
        'PICTURE': 'PICTURE',
        'VALUE': 'VALUE',
        'PROCEDURE': 'PROCEDURE',
        'MOVE': 'MOVE',
        'TO': 'TO',
        'ADD': 'ADD',
        'SUBTRACT': 'SUBTRACT',
        'MULTIPLY': 'MULTIPLY',
        'BY': 'BY',
        'GIVING': 'GIVING',
        'COMPUTE': 'COMPUTE',
        'IF': 'IF',
        'THEN': 'THEN',
        'ELSE': 'ELSE',
        'END-IF': 'END_IF',
        'PERFORM': 'PERFORM',
        'UNTIL': 'UNTIL',
        'THRU': 'THRU',
        'DISPLAY': 'DISPLAY',
        'FROM': 'FROM',
        'STOP': 'STOP',
        'RUN': 'RUN',
        'EXIT': 'EXIT',
        'GOBACK': 'GOBACK',
    }

    tokens = [
                 'IDENTIFIER',
                 'NUMBER',
                 'STRING',
                 'DOT',
                 'LPAREN',
                 'RPAREN',
                 'EQUALS',
                 'PLUS',
                 'MINUS',
                 'TIMES',
                 'DIVIDE',
                 'GT',
                 'LT',
                 'GE',
                 'LE',
             ] + list(reserved.values())

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_EQUALS = r'='
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_GT = r'>'
    t_LT = r'<'
    t_GE = r'>='
    t_LE = r'<='

    t_ignore = ' \t\r'

    def __init__(self):
        self.lexer = None

    def t_COMMENT(self, t):
        r'\*.*'
        pass

    def t_STRING(self, t):
        r'\"[^\"]*\"|\'[^\']*\''
        t.value = t.value[1:-1]
        return t


    def t_IDENTIFIER(self, t):
        r'[A-Za-z][A-Za-z0-9\-]*'
        t.type = self.reserved.get(t.value.upper(), 'IDENTIFIER')
        return t

    def t_NUMBER(self, t):
        r'\d+\.\d+|\d+'
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    t_DOT = r'\.'
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = ply.lex.lex(module=self, debug=False, **kwargs)
        return self.lexer

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} <filename>', file=sys.stderr )
        raise SystemExit
    else:
        with open( sys.argv[1], 'r' ) as INFILE:
            data = INFILE.read()
        lex = Lexer()
        lexer = lex.build()
        lexer.input( data )

        while True:
            token = lexer.token()
            if token is None:
                break
            print( token )
        print("Program ok.")
