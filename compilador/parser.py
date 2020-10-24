from sly import Parser as SlyParser
from compilador.lexer import Tokens
from compilador.semantica import AccionesSemanticas

class CompParser(SlyParser):
    # Define starting grammar
    start = 'program'
    # Get the token list from the lexer
    tokens = Tokens

    semantica = AccionesSemanticas()

    # Grammar rules and actions
    @_('PROGRAM ID vars funs main')
    def program(self, p):
        print('Regla: program')
        return 'Programa Exitoso'

    @_('var vars', 'empty')
    def vars(self, p):
        self.semantica.set_variables_globales()
        print('Regla: vars')
        pass

    @_('VAR ID array_dec ":" tipo')
    def var(self, p):
        self.semantica.agregar_variable(var=p.ID, tipo=p.tipo, dims=p.array_dec)
        print('Regla: var')
        pass

    @_('INT', 'FLOAT', 'CHAR')
    def tipo(self, p):
        print('Regla: tipo')
        return p[0]

    @_('fun funs', 'fun_void funs', 'empty')
    def funs(self, p):
        print('Regla: funs')
        pass

    @_('FUN ID "(" params ")" ":" tipo "{" estatutos return_stmt "}"')
    def fun(self, p):
        self.semantica.set_scope_funcion(p.ID, p.tipo)
        print('Regla: fun')
        pass

    @_('FUN ID "(" params ")" ":" VOID bloque')
    def fun_void(self, p):
        self.semantica.set_scope_funcion(p.ID, "void")
        self.semantica.termina_funcion()
        print('Regla: fun_void')
        pass

    @_('RETURN "(" expresion ")"')
    def return_stmt(self, p):
        print('Regla: return_stmt')
        pass

    @_('param_list')
    def params(self, p):
        print('Regla: params')
        return p.param_list

    @_('empty')
    def params(self, p):
        print('Regla: params empty')
        return []

    @_('ID ":" tipo param_list1')
    def param_list(self, p):
        self.semantica.agregar_parametro(p.ID, p.tipo)
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
        if self.semantica.pila_operadores[-1] == '+' or self.semantica.pila_operadores[-1] == '-':
            self.semantica.generar_cuadruplo()
        pass

    @_('exp2 exp', 'empty')
    def exp1(self, p):
        print('Regla: exp1')
        pass

    @_('"+"', '"-"')
    def exp2(self, p):
        print('Regla: exp2')
        self.semantica.pila_operadores.append(p[0])
        pass

    @_('factor termino1')
    def termino(self, p):
        print('Regla: termino')
        if self.semantica.pila_operadores[-1] == '*' or self.semantica.pila_operadores[-1] == '/':
            self.semantica.generar_cuadruplo()
        pass

    @_('termino2 termino', 'empty')
    def termino1(self, p):
        print('Regla: termino1')
        pass

    @_('"*"', '"/"')
    def termino2(self, p):
        print('Regla: termino2')
        self.semantica.pila_operadores.append(p[0])
        pass

    @_('"(" exp ")"', 'factor1 constante')
    def factor(self, p):
        print('Regla: factor')
        pass

    @_('"-"', 'empty')
    def factor1(self, p):
        print('Regla: factor1')
        pass

    @_('ID')
    def constante(self, p):
        print('Regla: constante')
        self.semantica.añadir_operando(p[0])
        pass

    @_('CTE_I', 'CTE_F', 'CTE_S', 'CTE_C')
    def constante(self, p):
        print('Regla: constante')
        self.semantica.añadir_operando(p[0])
        pass

    @_('array_usage')
    def constante(self, p):
        print('Regla: constante')
        self.semantica.añadir_operando(p[0])
        pass

    @_('"[" CTE_I "]"')
    def array_dec(self, p):
        print('Regla: array_dec 1 dim')
        return [p[1]]

    @_('"[" CTE_I "]" "[" CTE_I "]"')
    def array_dec(self, p):
        print('Regla: array_dec 2 dims')
        return [p[1], p[4]]

    @_('empty')
    def array_dec(self, p):
        print('Regla: array_dec empty')
        return []

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
