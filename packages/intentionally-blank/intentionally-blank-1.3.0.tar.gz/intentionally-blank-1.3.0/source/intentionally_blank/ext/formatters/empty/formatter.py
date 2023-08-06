from intentionally_blank.formatter import Formatter
from intentionally_blank.text import split_indent, is_partitioned_line_blank


class EmptyBlankLineFormatter(Formatter):
    """Blank lines have no whitespace other than the terminating newline.
    """

    def format(self, lines):
        """
        Args:
            lines: An iterable series of strings, each with a newline terminator.

        Yields:
            An iterable series of strings, each with a newline terminator.
        """
        for line in lines:
            indent, text = split_indent(line)
            if not is_partitioned_line_blank(indent, text):
                yield line
            else:
                yield "\n"
