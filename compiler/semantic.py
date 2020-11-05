from compiler.semantic_cube import SemanticCube
from compiler.symbol_table import FunctionsDirectoryItem, VarTableItem, VarType, ConstType, ReturnType
from compiler.quadruple import Operator, Quadruple
from compiler.memory import VirtualMemoryManager


class SemanticActions:
    """
    Clase para manejar las acciones de los puntos neuralgicos del parser.

    Atributos:
        v_memory_manager:       Instancia de la clase VirtualMemoryManager.
        semantic_cube:          Instancia de la clase CuboSemantico.
        functions_directory:    Tabla que almacena la informacion de las funciones.
        global_var_table:       Tabla de variables globales.
        current_var_table:      Tabla de variables activa. Cambia cuando cambia el scope (tabla global o nueva funcion).
        const_table:            Tabla que asocia las constantes con una dirección de memoria.
        current_scope:          Scope activo.
        quad_list:              Lista de cuadruplos.
        operands_stack:         Pila de operandos.
        operators_stack:        Pila de operadores.
        types_stack:            Pila de tipos.
        jumps_stack:            Pila de saltos logicos en la lista de operandos.
        temp_vars_index:        Contador de variables temporales.
    """

    def __init__(self):
        self.v_memory_manager = VirtualMemoryManager()
        self.semantic_cube = SemanticCube()
        self.functions_directory = dict()
        self.global_var_table = dict()
        self.current_var_table = dict()
        self.const_table = dict()
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
        self.v_memory_manager.clear_mem()

    def set_current_scope(self, scope, return_type):
        """
        Configuracion de la tabla actual de variables a variables locales y el scope actual al nombre del
        modulo actual

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

        addr: int
        if self.current_scope == 'global':
            addr = self.v_memory_manager.global_addr.allocate_addr_block(var_type, size)
        else:
            addr = self.v_memory_manager.local_addr.allocate_addr_block(var_type, size)
        
        self.current_var_table[var_name] = VarTableItem(
            name = var_name,
            type = VarType(var_type),
            dims = dimensions,
            size = size,
            address = addr)

    def add_temp(self, var_name, var_type):
        """
        Añade variable temporal a la tabla actual de variables

        :param var_name: Nombre de la variable temporal a declarar
        :param var_type: Tipo de dato de la variable temporal
        :return: Dirección asignada a la nueva variable temporal
        """
        addr = self.v_memory_manager.temp_addr.allocate_addr_block(var_type, size)

        self.current_var_table[var_name] = VarTableItem(
            name = var_name,
            type = VarType(var_type),
            dims = (0, 0),
            size = 1,
            address = addr)

        return addr

    def get_const(self, const_value, const_value):
        """
        Busca constante en tabla de constantes y si no existe la registra

        :param const_value: Valor de la constante a registrar
        :param const_type: Tipo de dato de la constante
        :return: Dirección asignada a la constante
        """
        const = self.const_table.get(str(const_value))
        if const is None:
            return self.add_const(const_value, const_value)
        else:
            return const.address

    def add_const(self, const_value, const_type):
        """
        Añade constante a la tabla de constantes

        :param const_value: Valor de la constante a registrar
        :param const_type: Tipo de dato de la constante
        :return: Dirección asignada a la constante
        """
        if const_type == VarType.INT or const_type == VarType.FLOAT:
            addr = self.v_memory_manager.const_addr.allocate_addr_block(const_type)
            self.const_table[str(const_value)] = VarTableItem(
                                                    name = str(const_value),
                                                    type = VarType(const_type),
                                                    dims = (0, 0),
                                                    size = 1,
                                                    address = addr)
        else:
            addr = self.v_memory_manager.const_addr.allocate_addr_block(VarType.CHAR, len(const_value))
            self.const_table[str(const_value)] = VarTableItem(
                                                    name = str(const_value),
                                                    type = VarType(const_type),
                                                    dims = (len(const_value), 0),
                                                    size = len(const_value),
                                                    address = addr)
        return addr

    def add_params(self, params):
        """
        Añade parametros de funcion a la tabla actual de variables y registra los parametros en la tabla de 
        funciones (los parametros no pueden ser arreglos ni matrices).

        :param params: Lista de parametros a declarar. Tupla (param_name, param_type)
        """
        params.reverse()
        for (param_name, param_type) in params:
            self.functions_directory[self.current_scope].param_table.append(param_type)

            self.current_var_table[param_name] = VarTableItem(
                name=param_name,
                type=param_type,
                dims = (0, 0),
                size=1,
                address = self.v_memory_manager.local_addr.allocate_addr_block(param_type, 1))

    def generarate_quad(self):
        """
        Función para generar un cuadruplo utilizando las pilas de operadores, operandos y tipos
        """
        if len(self.operands_stack) >= 2 and len(self.types_stack) >= 2 
        and len(self.operators_stack) >= 1 and self.operators_stack[-1] != '(':
            right_operand = self.get_var(self.operands_stack.pop())
            right_type = self.types_stack.pop()  # TODO: Still necessary?
            left_operand = self.get_var(self.operands_stack.pop())
            left_type = self.types_stack.pop() # TODO: Still necessary?
            operator = Operator(self.operators_stack.pop())
            result_type = self.semantic_cube.type_match(left_type, right_type, operator)
            if result_type != "error":
                result = "temp_" + str(self.temp_vars_index)
                self.temp_vars_index += 1
                self.quad_list.append(Quadruple(operator, left_operand.address, right_operand.address, self.add_temp(result, result_type)))
                self.operands_stack.append(result)
                self.types_stack.append(result_type) # TODO: Still necessary?
            else:
                raise Exception("Type mismatch")
        else:
            raise Exception("Operation stack error")

    def push_var_operand(self, operand):
        """
        Añade una variable y su tipo a las pilas para generar cuadruplos

        :param operand: Operando a añadir
        """
        var = self.get_var(operand)
        self.operands_stack.append(var.name)
        self.types_stack.append(var.type) # TODO: Still necessary?

    def push_const_operand(self, operand):
        """
        Añade una constanto y su tipo a las pilas para generar cuadruplos

        :param operand: Operando a añadir
        """
        self.operands_stack.append(str(operand))
        self.types_stack.append(ConstType(type(operand)).name)

    def generar_lectura(self, var_name):
        """
        Genera cuadruplo con operando de read y direccion de la variable que recibe el valor

        :var_name: Variable donde se guardara el valor a leer
        """
        var = self.get_var(var_name)
        self.quad_list.append(Quadruple(Operator.READ, '', '', var.address))

    def generar_escritura(self, value):
        """
        Genera cuadruplo con operando de write y el valor a escribir

        :value: Constante que se va a escribir
        """
        self.quad_list.append(Quadruple(Operator.WRITE, '', '', value))
        # TODO: Terminar funcion

    def start_if(self):
        """
        Genera cuadruplos necesarios al principio de un if
        """
        if self.types_stack and self.types_stack.pop() == 'bool': # TODO: Still necessary?
            if self.operands_stack:
                res = self.operands_stack.pop()
                var_res = self.get_var(res)
                self.quad_list.append(Quadruple(Operator.GOTOF, var_res.address, '', ''))
                self.jumps_stack.append(len(self.quad_list) - 1)
            else:
                raise Exception("Operand stack error")
        else:   
            raise Exception("Type mismatch")

    def start_else(self):
        """
        Genera cuadruplos necesarios al principio de un else
        """
        self.quad_list.append(Quadruple(Operator.GOTO, '', '', ''))
        if self.jumps_stack:
            false = self.jumps_stack.pop()
            self.jumps_stack.append(len(self.quad_list) - 1)
            self.finish_jump(false, len(self.quad_list))
        else:
            raise Exception("Jump stack error")

    def end_if(self):
        """
        Genera cuadruplos necesarios al final de un if
        """
        if self.jumps_stack:
            end = self.jumps_stack.pop()
            self.finish_jump(end, len(self.quad_list))
        else:
            raise Exception("Jump stack error")

    def start_while(self):
        """
        Establece saltos necesarios al principio de ciclo while
        """
        self.jumps_stack.append(len(self.quad_list))

    def expresion_while(self):
        """
        Genera cuadruplos necesarios al final de la expresion del while
        """
        if self.types_stack and self.types_stack.pop() == 'bool': # TODO: Still necessary?
            res = self.operands_stack.pop()
            var_res = self.get_var(res)
            self.quad_list.append(Quadruple(Operator.GOTOF, var_res.address, '', ''))
            self.jumps_stack.append(len(self.quad_list) - 1)
        else:   
            raise Exception("Type mismatch")

    def end_while(self):
        """
        Completa saltos necesarios al final del ciclo while
        """
        if len(self.jumps_stack) >= 2:
            end = self.jumps_stack.pop()
            ret = self.jumps_stack.pop()
            self.quad_list.append(Quadruple(Operator.GOTO, '', '', ret))
            self.finish_jump(end, len(self.quad_list))
        else:
            raise Exception("Jump stack error")

    def start_for(self, id):
        """
        Verificaciones iniciales del ciclo for. Verifica que exista la vaaible de control y la agrega a los stacks

        :param id: nombre de la variable de control
        """
        var = self.get_var(id)
        if var.type == VarType.INT or var.type == VarType.FLOAT:
            self.operands_stack.append(var.name)
            self.types_stack.append(var.type) # TODO: Still necessary?
        else:
            raise Exception("Type mismatch")

    def valor_inicial_for(self):
        """
        Inicializa variable de control del ciclo for con valor de expresion
        """
        if len(self.types_stack) >= 2 and len(self.operands_stack) >= 2 and 
        (self.types_stack[-1] == 'int' or self.types_stack[-1] == 'float'): # TODO: Still necessary?
            tipo_exp = self.types_stack.pop() # TODO: Still necessary?
            exp = self.operands_stack.pop()
            var_exp = self.get_var(exp)
            tipo_control = self.types_stack.pop() # TODO: Still necessary?
            control = self.operands_stack.pop()
            var_control = self.get_var(control)
            tipo_res = self.semantic_cube.type_match(tipo_control, tipo_exp, '=')
            if tipo_res == 'int' or tipo_res == 'float':
                self.quad_list.append(Quadruple(Operator('='), var_exp.address, '', var_control.address))
                self.operands_stack.append(control)
                self.types_stack.append(tipo_res)
            else:
                raise Exception("Type mismatch")
        else:   
            raise Exception("Type mismatch")

    def valor_final_for(self):
        """
        Establece valor final del ciclo for con valor de expresion
        """
        if len(self.types_stack) >= 2 and len(self.operands_stack) >= 2 and 
        (self.types_stack[-1] == 'int' or self.types_stack[-1] == 'float'): # TODO: Still necessary?
            tipo_exp = self.types_stack.pop() # TODO: Still necessary?
            exp = self.operands_stack.pop()
            var_exp = self.get_var(exp)
            tipo_control = self.types_stack.pop() # TODO: Still necessary?
            control = self.operands_stack.pop()
            var_control = self.get_var(control)
            if tipo_exp == 'int' or tipo_exp == 'float':
                final = "_final_" + control
                final_address = self.add_temp(final, tipo_exp)
                self.quad_list.append(Quadruple(Operator('='), var_exp.address, '', final_address))
                temp = "temp_" + str(self.temp_vars_index)
                self.temp_vars_index += 1
                temp_address = self.add_temp(temp, "bool")
                self.quad_list.append(Quadruple(Operator('<'), var_control.address, final_address, temp_address))
                self.jumps_stack.append(len(self.quad_list) - 1)
                self.quad_list.append(Quadruple(Operator('gotof'), temp_address, '', ''))
                self.jumps_stack.append(len(self.quad_list) - 1)
                self.operands_stack.append(control)
                self.types_stack.append(tipo_control) # TODO: Still necessary?
            else:
                raise Exception("Type mismatch")
        else:   
            raise Exception("Type mismatch")

    def end_for(self):
        """
        Completa saltos necesarios al final del ciclo for
        """
        if len(self.jumps_stack) >= 2 and self.types_stack and self.operands_stack:
            tipo_control = self.types_stack.pop() # TODO: Still necessary?
            control = self.operands_stack.pop()
            var_control = self.get_var(control)
            temp = "temp_" + str(self.temp_vars_index)  # Pedir dirección de memoria para el resultado
            self.temp_vars_index += 1
            tipo_res = self.semantic_cube.type_match(tipo_control, 'int', '+')
            temp_address = self.add_temp(temp, tipo_res)
            self.quad_list.append(Quadruple(Operator('+'), var_control.address, self.get_const(1, VarType.INT), temp_address))
            self.quad_list.append(Quadruple(Operator('='), temp_address, '', var_control.address))
            end = self.jumps_stack.pop()
            ret = self.jumps_stack.pop()
            self.quad_list.append(Quadruple(Operator('goto'), '', '', ret))
            self.finish_jump(end, len(self.quad_list))
        else:
            raise Exception("Stack error")

    def finish_jump(self, quad, jump):
        """
        Completa cuadruplo de salto con la informacion necesaria restante

        :param quad: Quad a completar
        :param jump: Informacion faltante de quad sobre a donde se hara el salto
        """
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
