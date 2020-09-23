from lexer import Lexer
from parser import Parser

if __name__ == '__main__':
    inputFile = open("test_fail.txt", "r")
    inputText = inputFile.read()
    print(inputText)

    # LEXER: Lexical Analysis
    print('\n\nLEXER Analysis:')
    lexer = Lexer()
    for tok in lexer.tokenize(inputText):
        print('type=%r, value=%r' % (tok.type, tok.value))

    # PARSER: Synctactic Analysis
    print('\n\nPARSER Analysis:')
    parser = Parser()
    result = parser.parse(lexer.tokenize(inputText))
    print(result)

    inputFile.close()
