import typing


__all__ = [
    "Token",
]


class Token:
    """
    A token represents a sequence of characters that build up the structure of an expression. Tokens are produced by a
    lexer.
    """

    TYPE_EOF = "EOF"
    TYPE_SEQUENCE = "SEQUENCE"
    TYPE_LC_BRACKET = "LC_BRACKET"
    TYPE_RC_BRACKET = "RC_BRACKET"
    TYPE_COLON = "COLON"
    TYPE_COMMA = "COMMA"

    def __init__(
        self,
        token_position: int,
        token_type: str,
        token_value: typing.Optional[str],
        token_raw_value: typing.Optional[str],
    ):
        """
        Init method for the class.

        :param token_position: The position of the token within the expression.
        :param token_type: The type of the token, such as `'LC_BRACKET'` or `'COMMA'`.
        :param token_value: The value of the token without escape characters.
        :param token_raw_value: The raw value of the token with escape characters.
        """
        self._token_position = token_position
        self._token_type = token_type
        self._token_value = token_value
        self._token_raw_value = token_raw_value

    @property
    def token_position(self) -> int:
        """
        Gets the position of the token within the expression.

        :return: The position of the token within the expression.
        """
        return self._token_position

    @property
    def token_type(self) -> str:
        """
        Gets the type of the token, such as `'LC_BRACKET'` or `'COMMA'`.

        :return: The type of the token.
        """
        return self._token_type

    @property
    def token_value(self) -> typing.Optional[str]:
        """
        Gets the value of the token without the escape characters. `'EOF'` tokens have a :data:`None` value.

        :return: The value of the token without the escape characters.
        """
        return self._token_value

    @property
    def token_raw_value(self) -> typing.Optional[str]:
        """
        Gets the raw value of the token without the escape characters. `'EOF'` tokens have a :data:`None` value.

        :return: The raw value of the token without the escape characters.
        """
        return self._token_raw_value

    def __repr__(self) -> str:
        return "{}({}, {}, {}, {})".format(
            self.__class__.__name__,
            repr(self._token_position),
            repr(self._token_type),
            repr(self._token_value),
            repr(self._token_raw_value),
        )
