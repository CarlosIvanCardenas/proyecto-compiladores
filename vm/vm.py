from vm.memory import AddressBlock
from common.scope_size import GLOBAL_ADDRESS_RANGE, LOCAL_ADDRESS_RANGE, CONST_ADDRESS_RANGE, TEMP_ADDRESS_RANGE


class VM:
    """
    Clase para simular la ejecución de una maquina virtual.

    Atributos:
        global_memory:      Partición de memoria para el scope global.
        temp_memory:        Partición de memoria para mantener valores auxiliares.
        execution_stack:    Lista de bloques de memoria para cada función del directorio de funciones.
        quad_list:          Lista de cuadruplos a ejecutar.
        const_memory:       Partición de memoria para los valores constantes (read-only).
        fun_dir:            Tabla que almacena la informacion de las funciones a ejecutar.
    """
    def __init__(self, quad_list, const_table, fun_dir):
        """
        Inicializa los atributos de la clase VM.

        :param quad_list: Lista de cuadruplos a ejecutar.
        :param const_table: Tabla que asocia las constantes con una dirección de memoria.
        :param fun_dir: Tabla que almacena la informacion de las funciones a ejecutar.
        """
        self.global_memory = AddressBlock(GLOBAL_ADDRESS_RANGE[0], GLOBAL_ADDRESS_RANGE[1])
        self.temp_memory = AddressBlock(TEMP_ADDRESS_RANGE[0], TEMP_ADDRESS_RANGE[1])
        self.execution_stack = [AddressBlock(LOCAL_ADDRESS_RANGE[0], LOCAL_ADDRESS_RANGE[1])]

        self.quad_list = quad_list
        self.const_memory = dict(map(lambda c: (c[1], c[0]), const_table.values()))
        self.fun_dir = fun_dir

    def write(self, addr, value):
        """
        Función auxiliar para escribir un valor en una dirección de memoria.
        Verifica a que partición de memoria por scope pertenece la dirección.

        :param addr: Dirección (absoluta) en la cual se desea escribir.
        :param value: Valor que se desea escribir en memoria.
        """
        if GLOBAL_ADDRESS_RANGE[0] <= addr < GLOBAL_ADDRESS_RANGE[1]:
            self.global_memory.write(addr, value)
        elif LOCAL_ADDRESS_RANGE[0] <= addr < LOCAL_ADDRESS_RANGE[1]:
            # TODO: Get memory for current execution stack/function
            return
        elif CONST_ADDRESS_RANGE[0] <= addr < CONST_ADDRESS_RANGE[1]:
            raise MemoryError('Cannot to write to read-only memory')
        elif TEMP_ADDRESS_RANGE[0] <= addr < TEMP_ADDRESS_RANGE[1]:
            self.temp_memory.write(addr, value)
        else:
            raise MemoryError('Address out of bounds')

    def read(self, addr):
        """
        Función auxiliar para leer el valor asignado a una dirección de memoria.
        Verifica a que partición de memoria por scope pertenece la dirección.

        :param addr: Dirección (absoluta) de la cual se desea leer un valor.
        :return: El valor asignado en la dirección "addr".
        """
        if GLOBAL_ADDRESS_RANGE[0] <= addr < GLOBAL_ADDRESS_RANGE[1]:
            return self.global_memory.read(addr)
        elif LOCAL_ADDRESS_RANGE[0] <= addr < LOCAL_ADDRESS_RANGE[1]:
            # TODO: Get memory for current execution stack/function
            return
        elif CONST_ADDRESS_RANGE[0] <= addr < CONST_ADDRESS_RANGE[1]:
            return self.const_memory[addr]
        elif TEMP_ADDRESS_RANGE[0] <= addr < TEMP_ADDRESS_RANGE[1]:
            return self.temp_memory.read(addr)
        else:
            raise MemoryError('Address out of bounds')

    def read_block(self, addr, size):
        """
        Función auxiliar para leer los valores asignados a un bloque continuo de direcciones de memoria.
        Verifica a que partición de memoria por scope pertenece la dirección.

        :param addr: Dirección (absoluta) de la cual se desea leer un valor.
        :param size: Tamaño del bloque.
        :return: El valor asignado en la dirección "addr".
        """
        if GLOBAL_ADDRESS_RANGE[0] <= addr < GLOBAL_ADDRESS_RANGE[1]:
            return self.global_memory.read_block(addr,size)
        elif LOCAL_ADDRESS_RANGE[0] <= addr < LOCAL_ADDRESS_RANGE[1]:
            # TODO: Get memory for current execution stack/function
            return
        elif CONST_ADDRESS_RANGE[0] <= addr < CONST_ADDRESS_RANGE[1]:
            raise MemoryError('There is not const arrays')
        elif TEMP_ADDRESS_RANGE[0] <= addr < TEMP_ADDRESS_RANGE[1]:
            return self.temp_memory.read_block(addr, size)
        else:
            raise MemoryError('Address out of bounds')
