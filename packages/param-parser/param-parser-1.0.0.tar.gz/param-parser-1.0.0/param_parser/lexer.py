import abc
import typing

from .token import *


__all__ = [
    "Lexer",
    "ParamLexer",
    "ParamOptionsLexer",
    "ParamSequenceLexer",
]


class Lexer(abc.ABC):
    """
    Base class for all lexer implementations, such as a :class:`ParamLexer`. A lexer takes an input expression and
    produces tokens of it. Those tokens are consumed by a parser implementation.
    """

    def __init__(self, expression: str):
        """
        Init method for the class.

        :param expression: The expression the lexer should produce tokens from.
        """
        self._expression: str = expression
        self._position: int = 0

    @abc.abstractmethod
    def get_next_token(self) -> Token:
        """
        Produces the next token for the expression and advances the position pointer accordingly. This method should
        produce a :class:`Token` instance of type :attr:`Token.TYPE_EOF` if the end of the expression is reached.
        Subsequent calls to this method also produce an :attr:`Token.TYPE_EOF` token.

        :return: The next token produced for the expression.
        """
        pass

    @property
    def current_character(self) -> typing.Optional[str]:
        """
        Gets the current character the position pointer points to on the expression. If the position
        pointer exceeds the length of the expression, :data:`None` gets returned.

        :return: Character on the current position pointer.
        """
        if self._position >= len(self._expression):
            return None
        return self._expression[self._position]

    def advance(self):
        """
        Advances the position pointer by one. This method gets called by the :func:`read_single`
        and :func:`read_sequence` methods.

        :return:
        """
        self._position += 1

    def read_single(self, token_type: str) -> Token:
        """
        Reads the next character on the expression and produces a :class:`Token` of the given type from it. Advances the
        position pointer by one.

        :param token_type: The type of the token to produce.
        :return: The produced token instance.
        """
        token = Token(
            self._position, token_type, self.current_character, self.current_character
        )
        self.advance()

        return token

    def read_sequence(self, token_type: str, until: list = None) -> Token:
        """
        Reads a sequence of characters on the expression and produces a :class:`Token` of the given type from it. Reads
        until one of the given until-characters gets read as the current character or until the end of the expression is
        reached. The position pointer points to the character that ended the sequence after calling this method.

        :param token_type: The type of the token to produce.
        :param until: A list of characters that end the sequence.
        :return: The produced token instance.
        """
        until = (until or []) + [None]
        sequence = ""
        raw_sequence = ""
        position = self._position

        while self.current_character not in until:
            if self.current_character == "\\":
                raw_sequence += self.current_character
                self.advance()

            if self.current_character is not None:
                sequence += self.current_character
                raw_sequence += self.current_character
                self.advance()

        return Token(position, token_type, sequence, raw_sequence)

    def __repr__(self) -> str:
        return "{}({})".format(
            self.__class__.__name__,
            repr(self._expression),
        )


class ParamLexer(Lexer):
    """
    Lexer that produces tokens for a param expression. This is an expression that looks as follows:
    `"text:text:text:text"`
    """

    def get_next_token(self) -> Token:
        """
        Produces the next token for the input expression.

        :return: The next token produced for the expression.
        """
        current_character = self.current_character

        if current_character == ":":
            return self.read_single(Token.TYPE_COLON)
        elif current_character is None:
            return self.read_single(Token.TYPE_EOF)
        else:
            return self.read_sequence(Token.TYPE_SEQUENCE, [":"])


class ParamOptionsLexer(Lexer):
    """
    Lexer that produces tokens for a param options expression. This is an expression that looks as follows:
    `"text,text,text,text"`
    """

    def get_next_token(self) -> Token:
        """
        Produces the next token for the input expression.

        :return: The next token produced for the expression.
        """
        current_character = self.current_character

        if current_character == ",":
            return self.read_single(Token.TYPE_COMMA)
        elif current_character is None:
            return self.read_single(Token.TYPE_EOF)
        else:
            return self.read_sequence(Token.TYPE_SEQUENCE, [","])


class ParamSequenceLexer(Lexer):
    """
    Lexer that produces tokens for a param sequence expression. This is an expression that looks as follows:
    `"text{text}text{text}"`
    """

    def get_next_token(self) -> Token:
        """
        Produces the next token for the input expression.

        :return: The next token produced for the expression.
        """
        current_character = self.current_character

        if current_character == "{":
            return self.read_single(Token.TYPE_LC_BRACKET)
        elif current_character == "}":
            return self.read_single(Token.TYPE_RC_BRACKET)
        elif current_character is None:
            return self.read_single(Token.TYPE_EOF)
        else:
            return self.read_sequence(Token.TYPE_SEQUENCE, ["{", "}"])
