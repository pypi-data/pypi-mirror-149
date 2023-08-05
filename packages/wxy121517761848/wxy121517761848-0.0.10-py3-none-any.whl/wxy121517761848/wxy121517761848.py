"""Main module."""


def echo(s: str) -> str:
    """This funtion echos a string.

    Args:
        s (str): string to echo

    Returns:
        str: the input string
    """
    return s


def rev(s: str) -> str:
    """This funtion reverses a string.

    Args:
        s (str): string to echo

    Returns:
        str: the input string
    """
    return s[::-1]


class SomeClass:
    """Just a class, trying to get by."""

    def __init__(self, mandatory_p: str, optional_p: int = 42) -> None:
        """Simple class constructor.

        Args:
            mandatory_p (String): a mandatory string param.
            optional_p (int, optional): an optional integer param. Defaults to 42.
        """
        self.mandatory_p = mandatory_p
        self.optional_p = optional_p

    def __str__(self) -> str:
        """Generate a string representation of the object.

        Returns:
            str: _description_
        """
        s = f"mandatory_p -> {self.mandatory_p}, optional_p -> {self.optional_p}"
        return s
