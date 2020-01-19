# --------------------------------------------------------------------
import collections
import re


# --------------------------------------------------------------------
IGNORE = "@ignore"
PUSH = "@push"
POP = "@pop"
ROOT = "@root"


# --------------------------------------------------------------------
class LexError(Exception):
    def __init__(self, message, state=None, line=0, col=0, filename="<stdin>"):
        if state is not None:
            super().__init__(
                message + " (in %s @ %s:%d:%d)" % (state, filename, line, col)
            )
        else:
            super().__init__(message)

        self.state = state
        self.line = line
        self.col = col


# --------------------------------------------------------------------
class LexemeType:
    def __init__(self, name, expr, next_state=None, data=None):
        self.name = name
        self.next_state = next_state
        self.data = data

        try:
            if isinstance(expr, (list, tuple)):
                self.regexes = [re.compile(ex) for ex in expr]
            else:
                self.regexes = [re.compile(expr)]
        except Exception as e:
            raise LexError(
                'Failed to parse a regular expression for lexeme type "%s" in grammar.'
                % name
            ) from e

    def match(self, content, offset):
        for regex in self.regexes:
            match = regex.match(content, offset)
            if match is not None:
                return match
        return None


# --------------------------------------------------------------------
class Lexeme:
    def __init__(self, type, content, line, col, filename):
        self.type = type
        self.content = content
        self.line = line
        self.col = col
        self.filename = filename

    def __str__(self):
        return '{%s "%s" @ %s:%d:%d}' % (
            self.type.name,
            self.content,
            self.filename,
            self.line,
            self.col,
        )


# --------------------------------------------------------------------
class Lexer:
    IGNORE = "@ignore"
    PUSH = "@push"
    POP = "@pop"
    ROOT = "@root"

    def __init__(self, grammar=None, filename="<stdin>"):
        self.state_lexeme_types_map = collections.defaultdict(list)
        self.filename = filename

        if grammar is not None:
            self.add_grammar(grammar)

    def add_grammar(self, grammar):
        for state, lexeme_types in grammar.items():
            self.add_state_lexeme_types(state, lexeme_types)
        return self

    def add_state_lexeme_types(self, state, lexeme_types):
        self.state_lexeme_types_map[state].extend(
            [LexemeType(*lex_tuple) for lex_tuple in lexeme_types]
        )
        return self

    def tokenize(self, content):
        state_stack = [ROOT]
        lexemes = []
        n = 0
        line = 0
        col = 0

        while n < len(content):
            state = state_stack[-1]
            lexeme, match = self._get_next_lexeme(state, content, n, line, col)
            lexemes.append(lexeme)
            next_state = lexeme.type.next_state
            if next_state is not None:
                if next_state == PUSH:
                    if state == ROOT:
                        raise LexError("Cannot push instances of the @root state.")
                    state_stack.append(state)
                elif next_state == POP:
                    if state == ROOT:
                        raise LexError("Cannot pop off the @root state.")
                    state_stack.pop()
                else:
                    state_stack.append(next_state)

            next_n = match.end(0)
            for x in range(n, next_n):
                if content[x] == "\n":
                    line += 1
                    col = 0
                else:
                    col += 1
            n = next_n

        return [lex for lex in lexemes if lex.type.name != IGNORE]

    def _get_next_lexeme(self, state, content, n, line, col):
        lexeme_types = self.state_lexeme_types_map[state]
        if not lexeme_types:
            raise LexError(
                "No lexeme classes defined for state.", state, line, col, self.filename
            )
        for lexeme_type in lexeme_types:
            match = lexeme_type.match(content, n)
            if match is not None:
                lexeme_content = match.group(0)
                return (
                    Lexeme(lexeme_type, lexeme_content, line, col, self.filename),
                    match,
                )
        else:
            raise LexError(
                "Unknown character sequence.", state, line, col, self.filename
            )
