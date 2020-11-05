class SemanticCube:
    semantic_cube = {
        "int": {
            "int": {
                "+": "int", "-": "int", "*": "int", "/": "float", "<": "bool", ">": "bool", "==": "bool", "!=": "bool", "&&": "bool", "||": "bool"
            },
            "float": {
                "+": "float", "-": "float", "*": "float", "/": "float", "<": "bool", ">": "bool", "==": "bool", "!=": "bool", "&&": "bool", "||": "bool"
            },
            "char": {
                "+": "error", "-": "error", "*": "error", "/": "error", "<": "error", ">": "error", "==": "error", "!=": "error", "&&": "error", "||": "error"
            },
            "bool": {
                "+": "error", "-": "error", "*": "error", "/": "error", "<": "error", ">": "error", "==": "error", "!=": "error", "&&": "error", "||": "error"
            }
        },
        "float": {
            "int": {
                "+": "float", "-": "float", "*": "float", "/": "float", "<": "bool", ">": "bool", "==": "bool", "!=": "bool", "&&": "bool", "||": "bool"
            },
            "float": {
                "+": "float", "-": "float", "*": "float", "/": "float", "<": "bool", ">": "bool", "==": "bool", "!=": "bool", "&&": "bool", "||": "bool"
            },
            "char": {
                "+": "error", "-": "error", "*": "error", "/": "error", "<": "error", ">": "error", "==": "error", "!=": "error", "&&": "error", "||": "error"
            },
            "bool": {
                "+": "error", "-": "error", "*": "error", "/": "error", "<": "error", ">": "error", "==": "error", "!=": "error", "&&": "error", "||": "error"
            }
        },
        "char": {
            "int": {
                "+": "error", "-": "error", "*": "error", "/": "error", "<": "error", ">": "error", "==": "error", "!=": "error", "&&": "error", "||": "error"
            },
            "float": {
                "+": "error", "-": "error", "*": "error", "/": "error", "<": "error", ">": "error", "==": "error", "!=": "error", "&&": "error", "||": "error"
            },
            "char": {
                "+": "char", "-": "char", "*": "error", "/": "error", "<": "bool", ">": "bool", "==": "bool", "!=": "bool", "&&": "error", "||": "error"
            },
            "bool": {
                "+": "error", "-": "error", "*": "error", "/": "error", "<": "error", ">": "error", "==": "error", "!=": "error", "&&": "error", "||": "error"
            }
        },
        "bool": {
            "int": {
                "+": "error", "-": "error", "*": "error", "/": "error", "<": "error", ">": "error", "==": "error", "!=": "error", "&&": "error", "||": "error"
            },
            "float": {
                "+": "error", "-": "error", "*": "error", "/": "error", "<": "error", ">": "error", "==": "error", "!=": "error", "&&": "error", "||": "error"
            },
            "char": {
                "+": "error", "-": "error", "*": "error", "/": "error", "<": "error", ">": "error", "==": "error", "!=": "error", "&&": "error", "||": "error"
            },
            "bool": {
                "+": "error", "-": "error", "*": "error", "/": "error", "<": "error", ">": "error", "==": "bool", "!=": "bool", "&&": "bool", "||": "bool"
            }
        }
    }

    def type_match(self, left_type, right_type, operator):
        return self.semantic_cube[left_type][right_type][operator]