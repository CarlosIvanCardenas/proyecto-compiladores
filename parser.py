from sly import Parser as SlyParser
from lexer import Lexer

class Parser(SlyParser):

    start = 'program'

    # Get the token list from the lexer (required)
    tokens = Lexer.tokens

    # Grammar rules and actions
    @_('PROGRAM ID vars funs main')
    def program(self, p):
        print('Regla: program')
        return 'Programa Exitoso'

    @_('var vars', 'empty')
    def vars(self, p):
        print('Regla: vars')
        pass

    @_('VAR ID var1 ":" tipo')
    def var(self, p):
        print('Regla: var')
        pass

    @_('array_dec', 'empty')
    def var1(self, p):
        print('Regla: var1')
        pass

    @_('INT', 'FLOAT', 'CHAR')
    def tipo(self, p):
        print('Regla: tipo')
        pass

    @_('fun funs', 'fun_void funs', 'empty')
    def funs(self, p):
        print('Regla: funs')
        pass

    @_('FUN ID "(" params ")" ":" tipo "{" estatutos return_stmt "}"')
    def fun(self, p):
        print('Regla: fun')
        pass

    @_('FUN ID "(" params ")" ":" VOID bloque')
    def fun_void(self, p):
        print('Regla: fun_void')
        pass

    @_('RETURN "(" expresion ")"')
    def return_stmt(self, p):
        print('Regla: return_stmt')
        pass

    @_('param_list', 'empty')
    def params(self, p):
        print('Regla: params')
        pass

    @_('ID ":" tipo param_list1')
    def param_list(self, p):
        print('Regla: param_list')
        pass

    @_('"," param_list', 'empty')
    def param_list1(self, p):
        print('Regla: param_list1')
        pass

    @_('MAIN "(" ")" bloque')
    def main(self, p):
        print('Regla: main')
        pass

    @_('"{" estatutos "}"')
    def bloque(self, p):
        print('Regla: bloque')
        pass

    @_('estatuto estatutos1')
    def estatutos(self, p):
        print('Regla: estatutos')
        pass

    @_('estatutos', 'empty')
    def estatutos1(self, p):
        print('Regla: estatutos1')
        pass

    @_('asignacion', 'condicion', 'lectura', 'escritura', 'ciclo_for', 'ciclo_while', 'call_fun', 'var')
    def estatuto(self, p):
        print('Regla: estatuto')
        pass

    @_('ID "(" args ")"')
    def call_fun(self, p):
        print('Regla: call_fun')
        pass

    @_('arg_list', 'empty')
    def args(self, p):
        print('Regla: args')
        pass

    @_('exp arg_list1')
    def arg_list(self, p):
        print('Regla: arg_list')
        pass

    @_('"," arg_list', 'empty')
    def arg_list1(self, p):
        print('Regla: arg_list1')
        pass

    @_('ID ASSIGN expresion')
    def asignacion(self, p):
        print('Regla: asignacion')
        pass

    @_('IF "(" expresiones ")" bloque condicion1')
    def condicion(self, p):
        print('Regla: condicion')
        pass

    @_('ELSE bloque', 'empty')
    def condicion1(self, p):
        print('Regla: condicion1')
        pass

    @_('READ "(" ID lectura1 ")"')
    def lectura(self, p):
        print('Regla: lectura')
        pass

    @_('"," ID lectura1', 'empty')
    def lectura1(self, p):
        print('Regla: lectura1')
        pass

    @_('WRITE "(" constante ")"')
    def escritura(self, p):
        print('Regla: escritura')
        pass

    @_('FOR ID ASSIGN exp TO exp bloque')
    def ciclo_for(self, p):
        print('Regla: ciclo_for')
        pass

    @_('WHILE "(" expresiones ")" bloque')
    def ciclo_while(self, p):
        print('Regla: ciclo_while')
        pass

    @_('expresion expresiones1')
    def expresiones(self, p):
        print('Regla: expresiones')
        pass

    @_('AND expresiones', 'OR expresiones', 'empty')
    def expresiones1(self, p):
        print('Regla: expresiones1')
        pass

    @_('exp expresion1')
    def expresion(self, p):
        print('Regla: expresion')
        pass

    @_('expresion2 exp', 'empty')
    def expresion1(self, p):
        print('Regla: expresion1')
        pass

    @_('GT', 'LT', 'NE', 'EQ')
    def expresion2(self, p):
        print('Regla: expresion2')
        pass

    @_('termino exp1')
    def exp(self, p):
        print('Regla: exp')
        pass

    @_('exp2 exp', 'empty')
    def exp1(self, p):
        print('Regla: exp1')
        pass

    @_('"+"', '"-"')
    def exp2(self, p):
        print('Regla: exp2')
        pass

    @_('factor termino1')
    def termino(self, p):
        print('Regla: termino')
        pass

    @_('termino2 termino', 'empty')
    def termino1(self, p):
        print('Regla: termino1')
        pass

    @_('"*"', '"/"')
    def termino2(self, p):
        print('Regla: termino2')
        pass

    @_('"(" exp ")"', 'factor1 constante')
    def factor(self, p):
        print('Regla: factor')
        pass

    @_('"-"', 'empty')
    def factor1(self, p):
        print('Regla: factor1')
        pass

    @_('ID', 'CTE_I', 'CTE_F', 'CTE_S', 'CTE_C', 'array_usage')
    def constante(self, p):
        print('Regla: constante')
        pass

    @_('ID "[" CTE_I "]" array_dec1')
    def array_dec(self, p):
        print('Regla: array_dec')
        pass

    @_('"[" CTE_I "]"', 'empty')
    def array_dec1(self, p):
        print('Regla: array_dec1')
        pass

    @_('ID "[" exp "]" array_usage1')
    def array_usage(self, p):
        print('Regla: array_usage')
        pass

    @_('"[" exp "]"', 'empty')
    def array_usage1(self, p):
        print('Regla: array_usage1')
        pass

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
