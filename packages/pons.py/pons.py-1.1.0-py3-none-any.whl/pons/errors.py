class PONSException(Exception):
    """Base class for all API errors."""

    def __init__(self) -> None:
        super().__init__(self.__doc__)


class DictionaryNotFound(PONSException):
    """The dictionary does not exist."""


class LimitReached(PONSException):
    """The daily limit has been reached."""


class Unauthorized(PONSException):
    """The supplied credentials could not be verified or the access to a dictionary is not allowed."""
