import abc
import typing


__all__ = [
    "Node",
    "ParamNode",
    "SequenceNode",
]


class Node(abc.ABC):
    """
    Base class for all node implementations, such as a :class:`SequenceNode`. A node represents a parsed section of an
    input expression produced by the :class:`.parser.ParamSequenceParser`.
    """

    def __repr__(self) -> str:
        return "{}()".format(
            self.__class__.__name__,
        )


class ParamNode(Node):
    """
    A param node represents a section in the input expression that defines a param with all its metadata. A param
    always has a name, might have a type and has a list of options.
    """

    def __init__(
        self,
        param_name: str,
        param_type: typing.Optional[str],
        param_options: typing.Optional[list],
    ):
        """
        Init method for the class.

        :param param_name: The name of the param.
        :param param_type: The optional type of the param.
        :param param_options: The list of options of the param. Becomes an empty list if passed :data:`None`.
        """
        self._param_name: str = param_name
        self._param_type: typing.Optional[str] = param_type or None
        self._param_options: typing.List[str] = param_options or []

    @property
    def param_name(self) -> str:
        """
        Gets the name of the param.

        :return: The name of the param.
        """
        return self._param_name

    @property
    def param_type(self) -> typing.Optional[str]:
        """
        Gets the type of the param.

        :return: The type of the param.
        """
        return self._param_type

    @property
    def param_options(self) -> typing.List[str]:
        """
        Gets the list of options of the param. Each option is a string.

        :return: The name of the param.
        """
        return self._param_options

    def __repr__(self) -> str:
        return "{}({}, {}, {})".format(
            self.__class__.__name__,
            repr(self._param_name),
            repr(self._param_type),
            repr(self._param_options),
        )


class SequenceNode(Node):
    """
    A sequence node represents a section in the input expression that is a plain text sequence.
    """

    def __init__(self, sequence_value: str):
        """
        Init method for the class.

        :param sequence_value: The value of the sequence.
        """
        self._sequence_value = sequence_value

    @property
    def sequence_value(self) -> str:
        """
        Gets the value of the sequence.

        :return: The value of the sequence.
        """
        return self._sequence_value

    def __repr__(self) -> str:
        return "{}({})".format(
            self.__class__.__name__,
            repr(self._sequence_value),
        )
