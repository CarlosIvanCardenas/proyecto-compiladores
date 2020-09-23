from sly import Parser as SlyParser
from lexer import Lexer

class Parser(SlyParser):
    def __init__(self):
        self.env = {}

    start = 'program'

    # Get the token list from the lexer (required)
    tokens = Lexer.tokens

    # TODO: change grammar
    # Grammar rules and actions
    @_('PROGRAM ID ";" program1 bloque')
    def program(self, p):
        print ('Regla: Program')
        return 'Programa Exitoso'

    @_('')
    def empty(self, p):
        print ('Regla: Empty')
        pass

    def error(self, p):
        if p:
            print("Syntactical ERROR! Error at token ", p.type)
            self.errok()
        else:
            print("Syntactical ERROR! Error at EOF")