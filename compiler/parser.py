from sly import Parser as SlyParser
from compiler.lexer import Tokens
from compiler.semantic import SemanticActions
from compiler.symbol_table import ReturnType, VarType

class CompParser(SlyParser):
    # Define starting grammar
    start = 'program'
    # Get the token list from the lexer
    tokens = Tokens

    semantica = SemanticActions()

    # Grammar rules and actions
    @_('PROGRAM ID set_global vars funs main')
    def program(self, p):
        print('Regla: program')
        return 'Programa Exitoso'
    
    @_('')
    def set_global(self, p):
        self.semantica.set_global_scope()
        print('Regla: program')
        return 'Programa Exitoso'

    # Declaracion de VARIABLES GLOBALES
    @_('var vars', 'empty')
    def vars(self, p):
        print('Regla: vars')
        pass

    @_('VAR ID array_dec ":" tipo')
    def var(self, p):
        self.semantica.add_var(var_name=p.ID, var_type=p.tipo, dims=p.array_dec)
        print('Regla: var')
        pass

    # TIPO de variables
    @_('INT', 'FLOAT', 'CHAR')
    def tipo(self, p):
        print('Regla: tipo')
        return p[0]

    # Declaracion de FUNCIONES
    @_('fun funs', 'empty')
    def funs(self, p):
        print('Regla: funs')
        pass

    @_('fun_header bloque')
    def fun(self, p):
        print('Regla: fun')
        self.semantica.set_global_scope()
        pass

    @_('FUN ID param_list return_type')
    def fun_header(self, p):
        print('Regla: fun_header')
        self.semantica.set_current_scope(p.ID, ReturnType(p.return_type))
        self.semantica.add_params(p.param_list)
        pass

    @_('":" tipo', '":" VOID')
    def return_type(self, p):
        print('Regla: return_type')
        return p[1]

    @_('RETURN "(" expresion ")"')
    def return_stmt(self, p):
        print('Regla: return_stmt')
        pass

    # Declaracion de PARAMETROS
    @_('"(" params ")"')
    def param_list(self, p):
        print('Regla: param_list')
        return p.params

    @_('"(" empty ")"')
    def param_list(self, p):
        print('Regla: param_list is empty')
        return []

    @_('ID ":" tipo params_aux')
    def params(self, p):
        print('Regla: params')
        p.params_aux.append((p.ID, VarType(p.tipo)))
        return p.params_aux

    @_('"," params')
    def params_aux(self, p):
        print('Regla: params_aux')
        return params

    @_('empty')
    def params_aux(self, p):
        print('Regla: params_aux is empty')
        return []

    # MAIN
    @_('MAIN "(" ")" bloque')
    def main(self, p):
        print('Regla: main')
        pass

    @_('"{" estatutos "}"')
    def bloque(self, p):
        print('Regla: bloque')
        pass

    @_('"{" estatutos return_stmt "}"')
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

    # LLAMADA A FUNCIÓN
    @_('ID arg_list')
    def call_fun(self, p):
        print('Regla: call_fun')
        self.semantica.fun_call(p[0], p.arg_list)
        pass

    # ARGUMENTOS DE LLAMADA A FUNCIÓN
    @_('"(" args ")"')
    def arg_list(self, p):
        print('Regla: args')
        return p.args

    @_('empty')
    def arg_list(self, p):
        print('Regla: args')
        return []

    @_('exp args_aux')
    def args(self, p):
        print('Regla: arg_list')
        p.args_aux.append((self.semantica.operands_stack.pop(),
                           VarType(self.semantica.types_stack.pop())))
        return p.args_aux

    @_('"," args')
    def args_aux(self, p):
        print('Regla: arg_list1')
        return p.args

    @_('empty')
    def args_aux(self, p):
        print('Regla: arg_list1')
        return []

    # ASIGNACIÓN
    @_('ID ASSIGN expresion')
    def asignacion(self, p):
        print('Regla: asignacion')
        if self.semantica.operators_stack and self.semantica.operators_stack[-1] in ['+', '-']:
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
        self.semantica.start_if()
        print('Regla: condicion')
        pass

    @_('inicio_else bloque', 'empty')
    def condicion1(self, p):
        print('Regla: condicion1')
        pass

    @_('ELSE')
    def inicio_else(self, p):
        self.semantica.start_else()
        print('Regla: condicion1')
        pass

    # LECTURA
    @_('READ "(" id_lectura lectura1 ")"')
    def lectura(self, p):
        print('Regla: lectura')
        pass

    @_('ID')
    def id_lectura(self, p):
        self.semantica.generar_lectura(p.ID)
        print('Regla: lectura')
        pass

    @_('"," ID lectura1')
    def lectura1(self, p):
        self.semantica.generar_lectura(p.ID)
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
    @_('inicio_for initial_value_for end_value_for bloque')
    def ciclo_for(self, p):
        self.semantica.end_for()
        print('Regla: ciclo_for')
        pass

    @_('FOR ID')
    def inicio_for(self, p):
        self.semantica.start_for(p.ID)
        print('Regla: inicio_for')
        pass

    @_('ASSIGN exp')
    def initial_value_for(self, p):
        self.semantica.valor_inicial_for()
        print('Regla: valor_inicial_for')
        pass

    @_('TO exp')
    def end_value_for(self, p):
        self.semantica.valor_final_for()
        print('Regla: valor_final_for')
        pass

    @_('inicio_while expresion_while bloque')
    def ciclo_while(self, p):
        self.semantica.end_while()
        print('Regla: ciclo_while')
        pass

    @_('WHILE')
    def inicio_while(self, p):
        self.semantica.start_while()
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
        self.semantica.operators_stack.append(p[0])
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
        if self.semantica.operators_stack[-1] in ['>', '<', '!=', '==']:
            self.semantica.generarate_quad()
        pass

    @_('empty')
    def expresion1(self, p):
        print('Regla: expresion1')
        pass

    @_('GT', 'LT', 'NE', 'EQ')
    def expresion2(self, p):
        print('Regla: expresion2')
        self.semantica.operators_stack.append(p[0])
        pass

    # EXP
    @_('termino exp1')
    def exp(self, p):
        print('Regla: exp')
        if self.semantica.operators_stack and self.semantica.operators_stack[-1] in ['+', '-']:
            self.semantica.generarate_quad()
        pass

    @_('exp2 exp', 'empty')
    def exp1(self, p):
        print('Regla: exp1')
        pass

    @_('"+"', '"-"')
    def exp2(self, p):
        print('Regla: exp2')
        self.semantica.operators_stack.append(p[0])
        pass

    # TERMINO
    @_('factor termino1')
    def termino(self, p):
        print('Regla: termino')
        if self.semantica.operators_stack and self.semantica.operators_stack[-1] in ['*', '/']:
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
        self.semantica.operators_stack.append(p[0])
        pass
    
    # FACTOR
    @_('"(" add_par exp ")"')
    def factor(self, p):
        print('Regla: factor')
        self.semantica.operators_stack.pop()
        pass

    @_('')
    def add_par(self, p):
        print('Regla: add_par')
        self.semantica.operators_stack.append(p[0])
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
        print('Regla: Empty')
        pass

    def error(self, p):
        if p:
            print("Syntactical ERROR! Error at token ", p.type)
            self.errok()
        else:
            print("Syntactical ERROR! Error at EOF")