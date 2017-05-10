import unittest
from lexex import *

scheme_grammar = {
    ROOT: [
        (IGNORE,        '\\s+'),
        ('open-paren',  '\\(',      's-expr')
    ],

    's-expr': [
        (IGNORE,        '\\s+'),
        ('quote',       '`'),
        ('number',      '[0-9]*.?[0-9]+'),
        ('word',        '[-!?+*/A-Za-z_][-!?+*/A-Za-z_0-9]*'),
        ('open-paren',  '\\(',      PUSH),
        ('close-paren', '\\)',      POP)
    ]
}

scheme_code = """
    (def f (x) (
       (+ x .5))
    (print (f (f 1) 2.7))
""".strip()

expected_repr = """
{open-paren "(" @ <stdin>:0:0}
{word "def" @ <stdin>:0:1}
{word "f" @ <stdin>:0:5}
{open-paren "(" @ <stdin>:0:7}
{word "x" @ <stdin>:0:8}
{close-paren ")" @ <stdin>:0:9}
{open-paren "(" @ <stdin>:0:11}
{open-paren "(" @ <stdin>:1:7}
{word "+" @ <stdin>:1:8}
{word "x" @ <stdin>:1:10}
{number ".5" @ <stdin>:1:12}
{close-paren ")" @ <stdin>:1:14}
{close-paren ")" @ <stdin>:1:15}
{open-paren "(" @ <stdin>:2:4}
{word "print" @ <stdin>:2:5}
{open-paren "(" @ <stdin>:2:11}
{word "f" @ <stdin>:2:12}
{open-paren "(" @ <stdin>:2:14}
{word "f" @ <stdin>:2:15}
{number "1" @ <stdin>:2:17}
{close-paren ")" @ <stdin>:2:18}
{number "2.7" @ <stdin>:2:20}
{close-paren ")" @ <stdin>:2:23}
{close-paren ")" @ <stdin>:2:24}
""".strip()

#--------------------------------------------------------------------
class LexexTests(unittest.TestCase):
    def test_usage(self):
        """Test to verify that lexer works properly."""
        lex = Lexer(scheme_grammar)
        self.assertEqual(expected_repr, '\n'.join([str(x) for x in lex.tokenize(scheme_code)]))

#--------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

