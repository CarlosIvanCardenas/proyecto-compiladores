from compiler.lexer import CompLexer
from compiler.parser import CompParser
from common.debug_flags import DEBUG_UI, DEBUG_LEXER
import sys

def main():
    if DEBUG_UI:
        # Lee código como un argumento del sistema
        code = sys.argv[1]
    else:
        # Lee codigo desde un archivo especificado
        input_file = open("examples/fun_declaration_and_call", "r")
        code = input_file.read()
        print(code + '\n')
        input_file.close()

    # LEXER: Lexical Analysis
    lexer = CompLexer()
    for tok in lexer.tokenize(code):
        if not DEBUG_UI and DEBUG_LEXER:
            print('type=%r, value=%r' % (tok.type, tok.value))

    # PARSER: Syntactic Analysis
    parser = CompParser()
    result = parser.parse(lexer.tokenize(code))
    print('Result: ' + result)


if __name__ == '__main__':
    main()
