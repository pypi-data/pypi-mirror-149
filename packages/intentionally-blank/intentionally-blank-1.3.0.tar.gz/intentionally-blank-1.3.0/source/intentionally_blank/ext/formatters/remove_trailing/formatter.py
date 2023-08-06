from intentionally_blank.formatter import Formatter


class RemoveTrailingFormatter(Formatter):
    """Remove any trailing whitespace except for a newline
    """

    def format(self, lines):
        """
        Args:
            lines: An iterable series of strings, each with a newline terminator.

        Yields:
            An iterable series of strings, each with a newline terminator.
        """
        return map(remove_trailing_whitespace, lines)


def remove_trailing_whitespace(line):
    """Removes trailing whitespace, but preserves the newline if present.
    """
    if line.endswith("\n"):
        return "{}\n".format(remove_trailing_whitespace(line[:-1]))
    return line.rstrip()
