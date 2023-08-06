import more_itertools

from intentionally_blank.formatter import Formatter
from intentionally_blank.text import is_blank_line


class RemoveTrailingLinesFormatter(Formatter):
    """Remove lines at the end of the file which contain only whitespace.
    """

    def format(self, lines):
        """
        Args:
            lines: An iterable series of strings, each with a newline terminator.

        Yields:
            An iterable series of strings, each with a newline terminator.
        """
        return more_itertools.rstrip(lines, is_blank_line)


def remove_trailing_whitespace(line):
    """Removes trailing whitespace, but preserves the newline if present.
    """
    if line.endswith("\n"):
        return "{}\n".format(remove_trailing_whitespace(line[:-1]))
    return line.rstrip()
