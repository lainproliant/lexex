from lexex import Lexer, LexemeType
import sys

def main():
    lexer = Lexer()
    lexer.declare(Lexer.ROOT, [
        (LexemeType.IGNORE, '\\s+'),
        ('name', '[A-Za-z]+'),
        ('number', '[0-9]+'),
        ('open_bracket', '{', None, 'bracket')
    ])
    lexer.declare('bracket', [
        (LexemeType.IGNORE, '\\s+'),
        ('words', '\\w+'),
        ('open_bracket', '{', None, Lexer.PUSH),
        ('close_bracket', '}', None, Lexer.POP)
    ])
    
    for lexeme in lexer.parse(sys.stdin.read()):
        print(str(lexeme))

if __name__ == '__main__':
    main()
