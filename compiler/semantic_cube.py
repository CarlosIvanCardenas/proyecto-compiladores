from compiler.symbol_table import VarType
from compiler.quadruple import Operator

class SemanticCube:
    semantic_cube = {
        VarType.INT: {
            VarType.INT: {
                Operator.ASSIGN: VarType.INT, Operator.PLUS: VarType.INT, Operator.MINUS: VarType.INT, Operator.TIMES: VarType.INT, Operator.DIVIDE: VarType.FLOAT, Operator.LESSTHAN: VarType.BOOL, Operator.GREATERTHAN: VarType.BOOL, Operator.EQUAL: VarType.BOOL, Operator.NOTEQUAL: VarType.BOOL, Operator.AND: VarType.BOOL, Operator.OR: VarType.BOOL
            },
            VarType.FLOAT: {
                Operator.ASSIGN: VarType.INT, Operator.PLUS: VarType.FLOAT, Operator.MINUS: VarType.FLOAT, Operator.TIMES: VarType.FLOAT, Operator.DIVIDE: VarType.FLOAT, Operator.LESSTHAN: VarType.BOOL, Operator.GREATERTHAN: VarType.BOOL, Operator.EQUAL: VarType.BOOL, Operator.NOTEQUAL: VarType.BOOL, Operator.AND: VarType.BOOL, Operator.OR: VarType.BOOL
            },
            VarType.CHAR: {
                Operator.ASSIGN: "error", Operator.PLUS: "error", Operator.MINUS: "error", Operator.TIMES: "error", Operator.DIVIDE: "error", Operator.LESSTHAN: "error", Operator.GREATERTHAN: "error", Operator.EQUAL: "error", Operator.NOTEQUAL: "error", Operator.AND: "error", Operator.OR: "error"
            },
            VarType.BOOL: {
                Operator.ASSIGN: "error", Operator.PLUS: "error", Operator.MINUS: "error", Operator.TIMES: "error", Operator.DIVIDE: "error", Operator.LESSTHAN: "error", Operator.GREATERTHAN: "error", Operator.EQUAL: "error", Operator.NOTEQUAL: "error", Operator.AND: "error", Operator.OR: "error"
            }
        },
        VarType.FLOAT: {
            VarType.INT: {
                Operator.ASSIGN: VarType.FLOAT, Operator.PLUS: VarType.FLOAT, Operator.MINUS: VarType.FLOAT, Operator.TIMES: VarType.FLOAT, Operator.DIVIDE: VarType.FLOAT, Operator.LESSTHAN: VarType.BOOL, Operator.GREATERTHAN: VarType.BOOL, Operator.EQUAL: VarType.BOOL, Operator.NOTEQUAL: VarType.BOOL, Operator.AND: VarType.BOOL, Operator.OR: VarType.BOOL
            },
            VarType.FLOAT: {
                Operator.ASSIGN: VarType.FLOAT, Operator.PLUS: VarType.FLOAT, Operator.MINUS: VarType.FLOAT, Operator.TIMES: VarType.FLOAT, Operator.DIVIDE: VarType.FLOAT, Operator.LESSTHAN: VarType.BOOL, Operator.GREATERTHAN: VarType.BOOL, Operator.EQUAL: VarType.BOOL, Operator.NOTEQUAL: VarType.BOOL, Operator.AND: VarType.BOOL, Operator.OR: VarType.BOOL
            },
            VarType.CHAR: {
                Operator.ASSIGN: "error", Operator.PLUS: "error", Operator.MINUS: "error", Operator.TIMES: "error", Operator.DIVIDE: "error", Operator.LESSTHAN: "error", Operator.GREATERTHAN: "error", Operator.EQUAL: "error", Operator.NOTEQUAL: "error", Operator.AND: "error", Operator.OR: "error"
            },
            VarType.BOOL: {
                Operator.ASSIGN: "error", Operator.PLUS: "error", Operator.MINUS: "error", Operator.TIMES: "error", Operator.DIVIDE: "error", Operator.LESSTHAN: "error", Operator.GREATERTHAN: "error", Operator.EQUAL: "error", Operator.NOTEQUAL: "error", Operator.AND: "error", Operator.OR: "error"
            }
        },
        VarType.CHAR: {
            VarType.INT: {
                Operator.ASSIGN: "error", Operator.PLUS: "error", Operator.MINUS: "error", Operator.TIMES: "error", Operator.DIVIDE: "error", Operator.LESSTHAN: "error", Operator.GREATERTHAN: "error", Operator.EQUAL: "error", Operator.NOTEQUAL: "error", Operator.AND: "error", Operator.OR: "error"
            },
            VarType.FLOAT: {
                Operator.ASSIGN: "error", Operator.PLUS: "error", Operator.MINUS: "error", Operator.TIMES: "error", Operator.DIVIDE: "error", Operator.LESSTHAN: "error", Operator.GREATERTHAN: "error", Operator.EQUAL: "error", Operator.NOTEQUAL: "error", Operator.AND: "error", Operator.OR: "error"
            },
            VarType.CHAR: {
                Operator.ASSIGN: VarType.CHAR, Operator.PLUS: VarType.CHAR, Operator.MINUS: VarType.CHAR, Operator.TIMES: "error", Operator.DIVIDE: "error", Operator.LESSTHAN: VarType.BOOL, Operator.GREATERTHAN: VarType.BOOL, Operator.EQUAL: VarType.BOOL, Operator.NOTEQUAL: VarType.BOOL, Operator.AND: "error", Operator.OR: "error"
            },
            VarType.BOOL: {
                Operator.ASSIGN: "error", Operator.PLUS: "error", Operator.MINUS: "error", Operator.TIMES: "error", Operator.DIVIDE: "error", Operator.LESSTHAN: "error", Operator.GREATERTHAN: "error", Operator.EQUAL: "error", Operator.NOTEQUAL: "error", Operator.AND: "error", Operator.OR: "error"
            }
        },
        VarType.BOOL: {
            VarType.INT: {
                Operator.ASSIGN: "error", Operator.PLUS: "error", Operator.MINUS: "error", Operator.TIMES: "error", Operator.DIVIDE: "error", Operator.LESSTHAN: "error", Operator.GREATERTHAN: "error", Operator.EQUAL: "error", Operator.NOTEQUAL: "error", Operator.AND: "error", Operator.OR: "error"
            },
            VarType.FLOAT: {
                Operator.ASSIGN: "error", Operator.PLUS: "error", Operator.MINUS: "error", Operator.TIMES: "error", Operator.DIVIDE: "error", Operator.LESSTHAN: "error", Operator.GREATERTHAN: "error", Operator.EQUAL: "error", Operator.NOTEQUAL: "error", Operator.AND: "error", Operator.OR: "error"
            },
            VarType.CHAR: {
                Operator.ASSIGN: "error", Operator.PLUS: "error", Operator.MINUS: "error", Operator.TIMES: "error", Operator.DIVIDE: "error", Operator.LESSTHAN: "error", Operator.GREATERTHAN: "error", Operator.EQUAL: "error", Operator.NOTEQUAL: "error", Operator.AND: "error", Operator.OR: "error"
            },
            VarType.BOOL: {
                Operator.ASSIGN: VarType.BOOL, Operator.PLUS: "error", Operator.MINUS: "error", Operator.TIMES: "error", Operator.DIVIDE: "error", Operator.LESSTHAN: "error", Operator.GREATERTHAN: "error", Operator.EQUAL: VarType.BOOL, Operator.NOTEQUAL: VarType.BOOL, Operator.AND: VarType.BOOL, Operator.OR: VarType.BOOL
            }
        }
    }

    def type_match(self, left_type, right_type, operator):
        return self.semantic_cube[left_type][right_type][operator]
