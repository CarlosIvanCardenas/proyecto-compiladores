from dataclasses import dataclass
from enum import Enum

class Operator(Enum):
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'
    ASSIGN = '='
    AND = '&&'
    OR = '||'
    READ = 'read'
    WRITE = 'write'
    GOTO = 'goto'
    GOTOF = 'gotof'
    GOTOT = 'gotot'
    # Agregar los que faltan

class ConstType(Enum):
    int = int
    float = float
    string = str
    char = str

@dataclass
class Cuadruplo:
    operator: Operator
    left_operand: str # hay que remplazar los operandos por direcciones de memoria
    right_operand: str
    result: str