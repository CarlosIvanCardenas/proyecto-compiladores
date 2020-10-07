from lexer import Lexer
from parser import Parser


def main():
    input_file = open("test_success.txt", "r")
    input_text = input_file.read()
    print(input_text)

    # LEXER: Lexical Analysis
    print('\n\nLEXER Analysis:')
    lexer = Lexer()
    for tok in lexer.tokenize(input_text):
        print('type=%r, value=%r' % (tok.type, tok.value))

    # PARSER: Synctactic Analysis
    print('\n\nPARSER Analysis:')
    p = Parser()
    result = p.parse(lexer.tokenize(input_text))
    print(result)

    input_file.close()


if __name__ == '__main__':
    main()
