from compilador.cubo_semantico import CuboSemantico
from compilador.directorio_procedimientos import ElementoDirectorioFunciones, ElementoTablaVariables, TipoVariable
from compilador.cuadruplo import Operator, ConstType, Cuadruplo


class AccionesSemanticas:
    cubo_semantico = CuboSemantico()
    tabla_funciones = dict()            # Tabla que almacena la informacion de las funciones
    variables_globales = dict()         # Tabla de variables globales
    variables_actuales: dict()          # Tabla de variables activa. Cambia cuando cambia el scope (tabla global o nueva funcion)
    scope_actual = 'global'             # Scope activo
    lista_cuadruplos = []               # 
    pila_operandos = []                 # 
    pila_operadores = []                # 
    pila_tipos = []                     # 
    pila_saltos = []                    # 
    cont = 0                            # 

    def get_var(self, v):
        var = self.variables_actuales.get(v)
        if var is None:
            var = self.variables_globales.get(v)
        return var

    def set_variables_globales(self):
        """
        Configuracion de la tabla actual de variables a variables globales y el scope actual a global
        """
        self.variables_actuales = self.variables_globales
        self.scope_actual = 'global'

    def set_scope_funcion(self, scope, tipo_retorno):
        """
        Configuracion de la tabla actual de varaibles a varaibles globales y el scope actual a global
        """
        self.scope_actual = scope
        self.tabla_funciones[scope] = ElementoDirectorioFunciones(
            name=scope,
            return_type=tipo_retorno,
            param_table=[])
        self.variables_actuales = dict()

        if tipo_retorno != 'void':
            funcion = "fun_" + scope
            self.variables_globales[funcion] = ElementoTablaVariables(
                name=funcion,
                type=TipoVariable(tipo_retorno),
                size=1)

    def agregar_variable(self, var, tipo, dims):
        """
        Añade variable a la tabla actual de variables
        """
        tipo_variable = TipoVariable(tipo)

        if len(dims) == 0:
            size = 1
            dimensiones = (0, 0)
        elif len(dims) == 1:
            size = dims[0]
            dimensiones = (dims[0], 0)
        else:
            size = dims[0] * dims[1]
            dimensiones = (dims[0], dims[1])

        self.variables_actuales[var] = ElementoTablaVariables(
            name=var,
            type=tipo_variable,
            dims=dimensiones,
            size=size)

    def agregar_parametro(self, param, tipo):
        """
        Añade parametros de funcion a la tabla actual de variables
        """
        tipo_variable = TipoVariable(tipo)

        self.tabla_funciones[self.scope_actual].param_table.append((param, tipo))

        self.variables_actuales[param] = ElementoTablaVariables(
            name=param,
            type=tipo_variable,
            size=1)

    def termina_funcion(self):
        self.set_variables_globales()

    def generarate_quad(self):
        right_operand = self.pila_operandos.pop()
        right_type = self.pila_tipos.pop()
        left_operand = self.pila_operandos.pop()
        left_type = self.pila_tipos.pop()
        operator = Operator(self.pila_operadores.pop())
        result_type = self.cubo_semantico.typematch(left_type, right_type, operator)
        if result_type != "error":
            result = "temp_" + str(self.cont)  # Pedir dirección de memoria para el resultado
            self.cont += 1
            self.agregar_variable(result, result_type, [])
            self.lista_cuadruplos.append(Cuadruplo(operator, left_operand, right_operand, result))
            self.pila_operandos.append(result)
            self.pila_tipos.append(result_type)
        else:
            raise Exception("Type mismatch")

    def push_var_operand(self, operand):
        var = self.get_var(operand)
        if var is None:
            raise Exception("Undeclared variable")
        else:
            self.pila_operandos.append(var.name)
            self.pila_tipos.append(var.type)

    def push_const_operand(self, operand):
        self.pila_operandos.append(operand)
        self.pila_tipos.append(ConstType(type(operand)).name)
