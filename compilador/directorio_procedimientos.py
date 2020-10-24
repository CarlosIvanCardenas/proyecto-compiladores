from dataclasses import dataclass
from enum import Enum

class TipoVariable(Enum):
  INT = 'int'
  FLOAT = 'float'
  CHAR = 'char'
  BOOL = 'bool'

class TipoRetorno(Enum):
  VOID = 'void'
  INT = 'int'
  FLOAT = 'float'
  CHAR = 'char'

'''
Se tendra un diccionario que actue como Directorio de Procedimientos que almacene tuplas del tipo 
(ElementoDirectorioFunciones, list(ElementoTablaVariables)) por cada funcion del programa ademas del registro global.
'''
@dataclass
class ElementoDirectorioFunciones:
    name: str
    return_type: TipoRetorno
    param_table: list

'''
Se tendra un objeto ElementoTablaVariables por cada variable declarada dentro de un procedimiento, misma que se
almacenara en su correspondiente lista dentro del Directorio de Procedimientos
'''
@dataclass
class ElementoTablaVariables:
    name: str
    type: TipoVariable
    size: int
    dimensiones: (int, int) = (None, None)
