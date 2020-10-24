from dataclasses import dataclass
from enum import Enum

class Operator(Enum):
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'
    ASSIGN = '='
    # Agregar los que faltan


@dataclass
class Cuadruplo:
    operator: Operator
    left_operand: str # hay que remplazar los operandos por direcciones de memoria
    right_operand: str
    result: str