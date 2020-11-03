from compiler.semantic_cube import SemanticCube
from compiler.symbol_table import FunctionsDirectoryItem, VarTableItem, VarType, ConstType, ReturnType
from compiler.quadruple import Operator, Quadruple


class SemanticActions:
    """
    Clase para manejar las acciones de los puntos neuralgicos del parser.

    Atributos:
        semantic_cube:     Instancia de la clase CuboSemantico.
        functions_directory:    Tabla que almacena la informacion de las funciones.
        global_var_table: Tabla de variables globales.
        current_var_table: Tabla de variables activa. Cambia cuando cambia el scope (tabla global o nueva funcion).
        current_scope:       Scope activo.
        quad_list:   Lista de cuadruplos.
        operands_stack:     Pila de operandos.
        operators_stack:    Pila de operadores.
        types_stack:         Pila de tipos.
        jumps_stack:        Pila de saltos logicos en la lista de operandos.
        temp_vars_index:    Contador de variables temporales.
    """

    def __init__(self):
        self.semantic_cube = SemanticCube()
        self.functions_directory = dict()
        self.global_var_table = dict()
        self.current_var_table = dict()
        self.current_scope = 'global'
        self.quad_list = []
        self.operands_stack = []
        self.operators_stack = []
        self.types_stack = []
        self.jumps_stack = []
        self.temp_vars_index = 0

    def get_var(self, var_name):
        """
        Recuperar variable del diccionario de variables globales o del scope actual.
        Lanza una excepción si no se encuentra.

        :param var_name: Variable a buscar.
        :return: Una instancia de la clase VarTableItem.
        """
        var = self.current_var_table.get(var_name)
        if var is None:
            var = self.global_var_table.get(var_name)
            if var is None:
                raise Exception("Undeclared variable: " + var_name)
        return var

    def get_fun(self, fun_name):
        """
        Recuperar función del diccionario de funciones.
        Lanza una excepción si no se encuentra.

        :param fun_name: Función a buscar.
        :return: Una instancia de la clase FunctionsDirectoryItem.
        """
        fun = self.functions_directory.get(fun_name)
        if fun is None:
            raise Exception('Undeclared function: ' + fun_name)
        return fun

    def set_global_scope(self):
        """
        Configuracion de la tabla actual de variables a variables globales y el scope actual a global
        """
        self.current_var_table = self.global_var_table
        self.current_scope = 'global'

    def set_current_scope(self, scope, return_type):
        """
        Configuracion de la tabla actual de variables a variables globales y el scope actual a global

        :param scope: Nombre del scope/función actual a declarar
        :param return_type: Tipo de retorno de la función
        """
        self.current_scope = scope
        self.functions_directory[scope] = FunctionsDirectoryItem(
            name=scope,
            return_type=return_type,
            param_table=[])
        self.current_var_table = dict()

        if return_type != 'void':
            function_id = "fun_" + scope
            self.global_var_table[function_id] = VarTableItem(
                name=function_id,
                type=VarType(return_type),
                size=1)

    def add_var(self, var_name, var_type, dims):
        """
        Añade variable a la tabla actual de variables

        :param var_name: Nombre de la variable a declarar
        :param var_type: Tipo de dato de la variable
        :param dims: Dimensiones de la variable (Si es de una dimensión, arreglo o matríz)
        """
        if len(dims) == 0:
            size = 1
            dimensions = (0, 0)
        elif len(dims) == 1:
            size = dims[0]
            dimensions = (dims[0], 0)
        else:
            size = dims[0] * dims[1]
            dimensions = (dims[0], dims[1])

        self.current_var_table[var_name] = VarTableItem(
            name=var_name,
            type=VarType(var_type),
            dims=dimensions,
            size=size)

    def add_params(self, params):
        """
        Añade parametros de funcion a la tabla actual de variables

        :param params: Lista de parametros a declarar. Tupla (param_name, param_type)
        """
        params.reverse()
        for (param_name, param_type) in params:
            self.functions_directory[self.current_scope].param_table.append((param_name, param_type))

            self.current_var_table[param_name] = VarTableItem(
                name=param_name,
                type=param_type,
                size=1)

    def generarate_quad(self):
        """
        Función para generar un cuadruplo utilizando las pilas de operadores, operandos y tipos
        """
        right_operand = self.operands_stack.pop()
        right_type = self.types_stack.pop()
        left_operand = self.operands_stack.pop()
        left_type = self.types_stack.pop()
        operator = Operator(self.operators_stack.pop())
        result_type = self.semantic_cube.type_match(left_type, right_type, operator)
        if result_type != "error":
            result = "temp_" + str(self.temp_vars_index)  # TODO: Pedir dirección de memoria para el resultado
            self.temp_vars_index += 1
            self.add_var(result, result_type, [])
            self.quad_list.append(Quadruple(operator, left_operand, right_operand, result))
            self.operands_stack.append(result)
            self.types_stack.append(result_type)
        else:
            raise Exception("Type mismatch")

    def push_var_operand(self, operand):
        """
        Añade una variable y su tipo a las pilas para generar cuadruplos

        :param operand: Operando a añadir
        """
        var = self.get_var(operand)
        self.operands_stack.append(var.name)
        self.types_stack.append(var.type)

    def push_const_operand(self, operand):
        """
        Añade una constanto y su tipo a las pilas para generar cuadruplos

        :param operand: Operando a añadir
        """
        self.operands_stack.append(str(operand))
        self.types_stack.append(ConstType(type(operand)).name)

    def generar_lectura(self):
        if self.operands_stack:
            value = self.operands_stack.pop()
            self.quad_list.append(Quadruple(Operator.READ, '', '', value))
        else:
            raise Exception("Operand stack error")

    def generar_escritura(self, value):
        self.quad_list.append(Quadruple(Operator.WRITE, '', '', value))

    def start_if(self):
        exp_type = self.types_stack.pop()
        if self.types_stack and exp_type == 'bool':
            res = self.operands_stack.pop()
            self.quad_list.append(Quadruple(Operator.GOTOF, res, '', ''))
            self.jumps_stack.append(len(self.quad_list) - 1)
        else:   
            raise Exception("Type mismatch")

    def start_else(self):
        tipo = self.types_stack.pop()
        res = self.operands_stack.pop()
        self.quad_list.append(Quadruple(Operator.GOTO, res, '', ''))
        if self.jumps_stack:
            false = self.jumps_stack.pop()
        else:
            raise Exception("Jump stack error")
        self.jumps_stack.append(len(self.quad_list) - 1)
        self.finish_jump(false, len(self.quad_list))

    def end_if(self):
        if self.jumps_stack:
            end = self.jumps_stack.pop()
            self.finish_jump(end, len(self.quad_list))
        else:
            raise Exception("Jump stack error")

    def start_while(self):
        self.jumps_stack.append(len(self.quad_list))

    def expresion_while(self):
        if self.types_stack and self.types_stack[-1] == 'bool':
            tipo = self.types_stack.pop()
            res = self.operands_stack.pop()
            self.quad_list.append(Quadruple(Operator.GOTOF, res, '', ''))
            self.jumps_stack.append(len(self.quad_list) - 1)
        else:   
            raise Exception("Type mismatch")

    def end_while(self):
        if len(self.jumps_stack) >= 2:
            end = self.jumps_stack.pop()
            ret = self.jumps_stack.pop()
            self.quad_list.append(Quadruple(Operator.GOTO, '', '', ret))
            self.finish_jump(end, len(self.quad_list))
        else:
            raise Exception("Jump stack error")

    def start_for(self, id):
        var = self.get_var(id)
        if var.type == VarType.INT or var.type == VarType.FLOAT:
            self.operands_stack.append(var.name)
            self.types_stack.append(var.type)
        else:
            raise Exception("Type mismatch")

    def valor_inicial_for(self):
        if self.types_stack and (self.types_stack[-1] == 'int' or self.types_stack[-1] == 'float'):
            tipo_exp = self.types_stack.pop()
            exp = self.operands_stack.pop()
            tipo_control = self.types_stack.pop()
            control = self.operands_stack.pop()
            tipo_res = self.semantic_cube.type_match(tipo_control, tipo_exp, '=')
            if tipo_res == 'int' or tipo_res == 'float':
                self.quad_list.append(Quadruple(Operator('='), exp, '', control))
                self.operands_stack.append(control)
                self.types_stack.append(tipo_res)
            else:
                raise Exception("Type mismatch")
        else:   
            raise Exception("Type mismatch")

    def valor_final_for(self):
        if self.types_stack and (self.types_stack[-1] == 'int' or self.types_stack[-1] == 'float'):
            tipo_exp = self.types_stack.pop()
            exp = self.operands_stack.pop()
            tipo_control = self.types_stack.pop()
            control = self.operands_stack.pop()
            tipo_res = self.semantic_cube.type_match(tipo_control, tipo_exp, '=')
            if tipo_res == 'int' or tipo_res == 'float':
                self.add_var("final_" + control, tipo_res, [])
                self.quad_list.append(Quadruple(Operator('='), exp, '', "final_" + control))
                temp = "temp_" + str(self.temp_vars_index)  # Pedir dirección de memoria para el resultado
                self.temp_vars_index += 1
                self.add_var(temp, "bool", [])
                self.quad_list.append(Quadruple(Operator('<'), control, "final_" + control, temp))
                self.jumps_stack.append(len(self.quad_list) - 1)
                self.quad_list.append(Quadruple(Operator('gotof'), temp, '', ''))
                self.jumps_stack.append(len(self.quad_list) - 1)
                self.operands_stack.append(control)
                self.types_stack.append(tipo_control)
            else:
                raise Exception("Type mismatch")
        else:   
            raise Exception("Type mismatch")

    def end_for(self):
        if len(self.jumps_stack) >= 2:
            tipo_control = self.types_stack.pop()
            control = self.operands_stack.pop()
            temp = "temp_" + str(self.temp_vars_index)  # Pedir dirección de memoria para el resultado
            self.temp_vars_index += 1
            tipo_res = self.semantic_cube.type_match(tipo_control, 'int', '+')
            self.add_var(temp, tipo_res, [])
            self.quad_list.append(Quadruple(Operator('+'), control, 1, temp))
            self.quad_list.append(Quadruple(Operator('='), temp, '', control))
            end = self.jumps_stack.pop()
            ret = self.jumps_stack.pop()
            self.quad_list.append(Quadruple(Operator('goto'), '', '', ret))
            self.finish_jump(end, len(self.quad_list))
        else:
            raise Exception("Jump stack error")

    def finish_jump(self, quad, jump):
        if len(self.quad_list) > quad:
            self.quad_list[quad].result = jump
        else:   
            raise Exception("Quadruple error, index out of bounds")

    def fun_call(self, fun_name, arg_list):
        """
        Genera las acciones necesarias para llamar a una función.
        Verifica coherencia en tipos y número de argumentos.

        :param fun_name: Nombre o identificador de la función a llamar.
        :param arg_list: Lista de argumentos de la llamada a función.
        """
        # Verify that the function exists into the DirFunc
        fun = self.get_fun(fun_name)
        # Verify coherence in number of parameters
        if len(fun.param_list) != len(arg_list):
            raise Exception('Incorrect number of arguments in function call: ' + fun_name)
        # TODO: Generate action ERA size
        for param_index, ((param_name, param_type), (arg_name, arg_type)) in enumerate(zip(fun.param_list, arg_list)):
            # Verify coherence in types
            if param_type == arg_type:
                self.quad_list.append(Quadruple(Operator.PARAMETER, arg_name, '', param_index))
            else:
                raise Exception('Type mismatch, expected: ' + param_type + " got: " + arg_type)

        # Generate action GOSUB
        self.quad_list.append(Quadruple(Operator.GOSUB, fun_name, '', ''))  # TODO: Add initial address
