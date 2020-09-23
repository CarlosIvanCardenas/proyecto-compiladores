from sly import Lexer as SlyLexer

class Lexer(SlyLexer):
    # Set of token names
    tokens = {PROGRAM, ID, VAR, INT, FLOAT, CHAR, FUN, VOID, RETURN, MAIN, IF, ELSE, READ, WRITE, FOR, TO, WHILE,
              AND, OR, EQ, NE, LT, GT, ASSIGN, CTE_S, CTE_I, CTE_F, CTE_C}

    # Set of literal tokens
    literals = {'(', ')', '{', '}', ';', ':', ',', '+', '-', '*', '/'}

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Regular expression rules for tokens
    AND = r'&&'
    OR = r'\|\|'
    EQ = r'=='
    ASSIGN = r'='
    NE = r'!='
    LT = r'<'
    GT = r'>'
    CTE_S = r'\".+\"'
    CTE_I = r'\d+'
    CTE_F = r'\d+\.\d+'
    CTE_C = r'\'.\''

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['program'] = PROGRAM
    ID['var'] = VAR
    ID['int'] = INT
    ID['float'] = FLOAT
    ID['char'] = CHAR
    ID['fun'] = FUN
    ID['void'] = VOID
    ID['return'] = RETURN
    ID['main'] = MAIN
    ID['if'] = IF
    ID['else'] = ELSE
    ID['read'] = READ
    ID['write'] = WRITE
    ID['for'] = FOR
    ID['to'] = TO
    ID['while'] = WHILE

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('LEXICAL ERROR! Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
