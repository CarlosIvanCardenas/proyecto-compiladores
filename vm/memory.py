from compiler.symbol_table import VarType

class AddressBlock:
    """
    Clase que representa un bloque de direcciones de memoria, particionado en los 4 tipos de dato disponibles
    para el lenguaje.
    Contiene métodos para leer y escribir en direcciones o bloques de memoria.

    Atributos:
        start_addr:         Dirección de memoria en la cual inicia el bloque.
        partition_size:     Tamaño por default para las 4 particiones por tipo de dato.
        int_addr_block:     Bloque de direcciones de memoria para la partición int.
        float_addr_block:   Bloque de direcciones de memoria para la partición float.
        char_addr_block:    Bloque de direcciones de memoria para la partición char.
        bool_addr_block:    Bloque de direcciones de memoria para la partición bool.
    """
    def __init__(self, start_addr, end_addr, int_size=None, float_size=None, char_size=None, bool_size=None):
        self.start_addr = start_addr
        self.default_size = (end_addr - start_addr + 1) // 4

        self.int_addr_block = [None] * (self.default_size if int_size is None else int_size)
        self.float_addr_block = [None] * (self.default_size if float_size is None else float_size)
        self.char_addr_block = [None] * (self.default_size if char_size is None else char_size)
        self.bool_addr_block = [None] * (self.default_size if bool_size is None else bool_size)

    def get_partition(self, addr):
        """
        Regresa a que partición del AddressBlock pertenece cierta dirección de memoria.

        :param addr: La dirección de la cual se quiere saber a que partición pertenece.
        :return: La partición a la cual pertenece, utilizando el Enumerable VarType.
        """
        # Convertir addr a una dirección de memoria relativa a la instancia actual de AddressBlock.
        rel_addr = addr - self.start_addr
        if 0 <= rel_addr < self.default_size:
            return VarType.INT
        elif self.default_size <= rel_addr < self.default_size*2:
            return VarType.FLOAT
        elif self.default_size*2 <= rel_addr < self.default_size*3:
            return VarType.CHAR
        elif self.default_size*3 <= rel_addr < self.default_size*4:
            return VarType.BOOL
        else:
            raise MemoryError(f'Address: {addr} out of bounds')

    def get_address(self, addr, partition):
        """
        Regresa la dirección de memoria relativa a la partición a la que pertenece según su tipo de dato.

        :param addr: La dirección (absoluta) de la cual se quiere saber la dirección relativa a la partición.
        :param partition: La partición a la cual pertenece, instancia de VarType.
        :return: La dirección relativa a la partición.
        """
        rel_addr = addr - self.start_addr
        if partition == VarType.INT:
            return int(rel_addr)
        elif partition == VarType.FLOAT:
            return int(rel_addr - self.default_size)
        elif partition == VarType.CHAR:
            return int(rel_addr - self.default_size*2)
        elif partition == VarType.BOOL:
            return int(rel_addr - self.default_size*3)

    def write(self, addr, value):
        """
        Escribe un valor en una dirección de memoria.

        :param addr: Dirección (absoluta) en la cual se desea escribir.
        :param value: Valor que se desea escribir en memoria.
        """
        partition = self.get_partition(addr)
        if partition == VarType.INT:
            self.int_addr_block[self.get_address(addr, partition)] = int(value)
        elif partition == VarType.FLOAT:
            self.float_addr_block[self.get_address(addr, partition)] = float(value)
        elif partition == VarType.CHAR:
            self.char_addr_block[self.get_address(addr, partition)] = value
        elif partition == VarType.BOOL:
            self.bool_addr_block[self.get_address(addr, partition)] = value

    def read(self, addr):
        """
        Lee el valor asignado a una dirección de memoria.

        :param addr: Dirección (absoluta) de la cual se desea leer un valor.
        :return: El valor asignado en la dirección "addr".
        """
        partition = self.get_partition(addr)
        if partition == VarType.INT:
            return self.int_addr_block[self.get_address(addr, partition)]
        elif partition == VarType.FLOAT:
            return self.float_addr_block[self.get_address(addr, partition)]
        elif partition == VarType.CHAR:
            return self.char_addr_block[self.get_address(addr, partition)]
        elif partition == VarType.BOOL:
            return self.bool_addr_block[self.get_address(addr, partition)]

    def read_block(self, addr, size):
        """
        Lee los valores asignados a un bloque continuo de direcciones de memoria.

        :param addr: Dirección (absoluta) de la cual se desea leer un valor.
        :param size: Tamaño del bloque.
        :return: El valor asignado en la dirección "addr".
        """
        partition = self.get_partition(addr)
        addr = self.get_address(addr, partition)
        if partition == VarType.INT:
            return self.int_addr_block[addr:addr + size]
        elif partition == VarType.FLOAT:
            return self.float_addr_block[addr:addr + size]
        elif partition == VarType.CHAR:
            return self.char_addr_block[addr:addr + size]
        elif partition == VarType.BOOL:
            return self.bool_addr_block[addr:addr + size]
