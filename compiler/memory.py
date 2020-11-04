from compiler.symbol_table import VarType
from common.scope_size import GLOBAL_ADDRESS_RANGE, LOCAL_ADDRESS_RANGE, CONST_ADDRESS_RANGE, TEMP_ADDRESS_RANGE


class AddressBlock:
    """
    Clase que representa un bloque de direcciones virtuales de memoria, particionado en los 4 tipos de dato disponibles
    para el lenguaje.

    Atributos:
        int_addr_idx:     Indice de direcciones de memoria para la partición int.
        float_addr_idx:   Indice de direcciones de memoria para la partición float.
        char_addr_idx:    Indice de direcciones de memoria para la partición char.
        bool_addr_idx:    Indice de direcciones de memoria para la partición bool.
    """

    def __init__(self, start_addr, end_addr):
        partition_size = (end_addr - start_addr + 1) // 4
        self.int_addr_idx = start_addr
        self.float_addr_idx = start_addr + partition_size
        self.char_addr_idx = self.float_addr_idx + partition_size
        self.bool_addr_idx = self.char_addr_idx + partition_size

    def allocate_addr(self, var_type):
        """
        Método para asignar direcciones virtuales de memoria a una variable en una partición acorde a su tipo de dato.

        :param var_type: El tipo de dato de la variable a guardar en memoria.
        :return: Una dirección virual de memoria disponible para asignar la variable.
        """
        if var_type == VarType.INT:
            address = self.int_addr_idx
            self.int_addr_idx += 1
        elif var_type == VarType.FLOAT:
            address = self.float_addr_idx
            self.float_addr_idx += 1
        elif var_type == VarType.CHAR:
            address = self.char_addr_idx
            self.char_addr_idx += 1
        else:  # VarType.BOOL
            address = self.bool_addr_idx
            self.bool_addr_idx += 1
        return address

    def allocate_addr_block(self, var_type, block_size):
        """
        Método para asignar un bloque de direcciones virtuales de memoria a una variable en una partición acorde a su
        tipo de dato.

        :param var_type: El tipo de dato de la variable a guardar en memoria.
        :param block_size: Tamaño del bloque de direcciones necesario.
        :return: Una dirección virual de memoria disponible para asignar la variable.
        """
        if var_type == VarType.INT:
            address = self.int_addr_idx
            self.int_addr_idx += block_size
        elif var_type == VarType.FLOAT:
            address = self.float_addr_idx
            self.float_addr_idx += block_size
        elif var_type == VarType.CHAR:
            address = self.char_addr_idx
            self.char_addr_idx += block_size
        else:  # VarType.BOOL
            address = self.bool_addr_idx
            self.bool_addr_idx += block_size
        return address

class VirtualMemoryManager:
    """
    Clase encargada de administrar las direcciones virtuales de memoria particionadas por scope.

    Atributos:
        global_addr:    Bloque de direcciones globales.
        local_addr:     Bloque de direcciones locales.
        const_addr:     Bloque de direcciones para constantes.
        temp_addr:      Bloque de direcciones temporales.
    """
    def __init__(self):
        self.global_addr = AddressBlock(GLOBAL_ADDRESS_RANGE[0], GLOBAL_ADDRESS_RANGE[1])
        self.local_addr = AddressBlock(LOCAL_ADDRESS_RANGE[0], LOCAL_ADDRESS_RANGE[1])
        self.const_addr = AddressBlock(CONST_ADDRESS_RANGE[0], CONST_ADDRESS_RANGE[1])
        self.temp_addr = AddressBlock(TEMP_ADDRESS_RANGE[0], TEMP_ADDRESS_RANGE[1])

    def clear_mem(self):
        """
        Restablece los bloques de direcciones locales y temporales.
        """
        self.local_addr = AddressBlock(LOCAL_ADDRESS_RANGE[0], LOCAL_ADDRESS_RANGE[1])
        self.temp_addr = AddressBlock(TEMP_ADDRESS_RANGE[0], TEMP_ADDRESS_RANGE[1])
