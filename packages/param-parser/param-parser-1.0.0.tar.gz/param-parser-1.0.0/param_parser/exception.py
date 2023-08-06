__all__ = [
    "ParserSyntaxException",
]


class ParserSyntaxException(Exception):
    """
    Class for exceptions that are raised on unexpected tokens.
    """

    def __init__(self, message: str):
        self._message = message

        super().__init__(self._message)

    def __repr__(self) -> str:
        return "{}({})".format(
            self.__class__.__name__,
            repr(self._message),
        )
