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
    @_('PROGRAM ID set_global vars funs main')
    def program(self, p):
        print('Regla: program')
        return 'Programa Exitoso'
    
    @_('')
    def set_global(self, p):
        self.semantica.set_variables_globales()
        print('Regla: program')
        return 'Programa Exitoso'

    # Declaracion de VARIABLES GLOBALES
    @_('var vars', 'empty')
    def vars(self, p):
        print('Regla: vars')
        pass

    @_('VAR ID array_dec ":" tipo')
    def var(self, p):
        self.semantica.agregar_variable(var=p.ID, tipo=p.tipo, dims=p.array_dec)
        print('Regla: var')
        pass

    # TIPO de variables
    @_('INT', 'FLOAT', 'CHAR')
    def tipo(self, p):
        print('Regla: tipo')
        return p[0]

    # Declaracion de FUNCIONES
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
        # Manejo de Memoria
        self.semantica.termina_funcion()
        print('Regla: fun_void')
        pass

    @_('RETURN "(" expresion ")"')
    def return_stmt(self, p):
        print('Regla: return_stmt')
        pass

    # Declaracion de PARAMETROS
    @_('param_list')
    def params(self, p):
        print('Regla: params')
        pass

    @_('empty')
    def params(self, p):
        print('Regla: params empty')
        pass

    @_('ID ":" tipo param_list1')
    def param_list(self, p):
        self.semantica.agregar_parametro(p.ID, p.tipo)
        print('Regla: param_list')
        pass

    @_('"," param_list', 'empty')
    def param_list1(self, p):
        print('Regla: param_list1')
        pass

    # MAIN
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
        if self.semantica.pila_operadores and (self.semantica.pila_operadores[-1] == '+' or self.semantica.pila_operadores[-1] == '-'):
            self.semantica.generarate_quad()
        pass

    # ESTATUTOS CONDICIONALES
    @_('start_if bloque condicion1')
    def condicion(self, p):
        self.semantica.end_if()
        print('Regla: condicion')
        pass

    @_('IF "(" expresiones ")"')
    def start_if(self, p):
        self.semantica.iniciar_if()
        print('Regla: condicion')
        pass

    @_('inicio_else bloque', 'empty')
    def condicion1(self, p):
        print('Regla: condicion1')
        pass

    @_('ELSE')
    def inicio_else(self, p):
        self.semantica.iniciar_else()
        print('Regla: condicion1')
        pass

    # LECTURA
    @_('READ "(" id_lectura lectura1 ")"')
    def lectura(self, p):
        print('Regla: lectura')
        pass

    @_('ID')
    def id_lectura(self, p):
        self.semantica.generar_lectura()
        print('Regla: lectura')
        pass

    @_('"," ID lectura1')
    def lectura1(self, p):
        self.semantica.generar_lectura()
        print('Regla: lectura1')
        pass

    @_('empty')
    def lectura1(self, p):
        print('Regla: lectura1 empty')
        pass

    # ESCRITURA
    @_('WRITE "(" constante ")"')
    def escritura(self, p):
        self.semantica.generar_escritura(p.constante)
        print('Regla: escritura')
        pass

    # CICLOS CONDICIONALES
    @_('FOR ID ASSIGN exp TO exp bloque')
    def ciclo_for(self, p):
        print('Regla: ciclo_for')
        pass

    @_('inicio_while expresion_while bloque')
    def ciclo_while(self, p):
        self.semantica.fin_while()
        print('Regla: ciclo_while')
        pass

    @_('WHILE')
    def inicio_while(self, p):
        self.semantica.iniciar_while()
        print('Regla: inicio_while')
        pass

    @_('"(" expresiones ")"')
    def expresion_while(self, p):
        self.semantica.expresion_while()
        print('Regla: expresion_while')
        pass

    # EXPRESIONES
    @_('expresion expresiones1')
    def expresiones(self, p):
        print('Regla: expresiones')
        pass

    @_('AND expresiones', 'OR expresiones')
    def expresiones1(self, p):
        print('Regla: expresiones1')
        self.semantica.pila_operadores.append(p[0])
        pass

    @_('empty')
    def expresiones1(self, p):
        print('Regla: expresiones1')
        pass

    @_('exp expresion1')
    def expresion(self, p):
        print('Regla: expresion')
        pass

    @_('expresion2 exp')
    def expresion1(self, p):
        print('Regla: expresion1')
        if self.semantica.pila_operadores[-1] in ['>', '<', '!=', '==']:
            self.semantica.generarate_quad()
        pass

    @_('empty')
    def expresion1(self, p):
        print('Regla: expresion1')
        pass

    @_('GT', 'LT', 'NE', 'EQ')
    def expresion2(self, p):
        print('Regla: expresion2')
        self.semantica.pila_operadores.append(p[0])
        pass

    @_('termino exp1')
    def exp(self, p):
        print('Regla: exp')
        if self.semantica.pila_operadores and (self.semantica.pila_operadores[-1] == '+' or self.semantica.pila_operadores[-1] == '-'):
            self.semantica.generarate_quad()
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
        if self.semantica.pila_operadores and (self.semantica.pila_operadores[-1] == '*' or self.semantica.pila_operadores[-1] == '/'):
            self.semantica.generarate_quad()
        pass

    @_('termino2 termino')
    def termino1(self, p):
        print('Regla: termino1')
        pass

    @_('empty')
    def termino1(self, p):
        print('Regla: termino1')
        pass

    @_('"*"', '"/"')
    def termino2(self, p):
        print('Regla: termino2')
        self.semantica.pila_operadores.append(p[0])
        pass

    @_('"(" add_par exp ")"')
    def factor(self, p):
        print('Regla: factor')
        self.semantica.pila_operadores.pop()
        pass

    @_('')
    def add_par(self, p):
        print('Regla: add_par')
        self.semantica.pila_operadores.append(p[0])
        pass

    @_('factor1 constante')
    def factor(self, p):
        print('Regla: factor')
        pass

    @_('"-"', 'empty')
    def factor1(self, p):
        print('Regla: factor1')
        pass

    @_('ID')
    def constante(self, p):
        self.semantica.push_var_operand(p[0])
        print('Regla: constante')
        pass

    @_('CTE_I', 'CTE_F', 'CTE_S', 'CTE_C')
    def constante(self, p):
        print('Regla: constante')
        self.semantica.push_const_operand(p[0])
        pass

    @_('array_usage')
    def constante(self, p):
        print('Regla: constante')
        pass


    # Operaciones con ARREGLOS
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
