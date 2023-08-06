import re

from asq import query
from more_itertools import tail

LEADING_PATTERN = r"^(\s*)(.*)$"
LEADING_REGEX = re.compile(LEADING_PATTERN)


def is_blank_line(line: str) -> bool:
    """Determine whether a line contains any non-whitespace characters.

    Args:
        line: The string to be tested.

    Returns:
        True if the string is empty or contains only whitespace, otherwise False.
    """
    indent, text = split_indent(line)
    return is_partitioned_line_blank(indent, text)


def split_indent(line):
    m = LEADING_REGEX.match(line)
    assert m is not None
    indent, text = m.groups()
    return indent, text


def is_partitioned_line_blank(indent: str, text: str) -> bool:
    """Determine whether an indent-partitioned line is blank.

    Args:
        indent: The leading indent of a line. May be empty.
        text: Text following the leading indent. May be empty.

    Returns:
        True if no text follows the indent.
    """
    return len(text) == 0


def strip_lines(text):
    """Remove leading and trailing blank lines."""
    is_blank = lambda line: line.isspace() or not line
    return '\n'.join(
        query(text.splitlines())
            .skip_while(is_blank)
            .reverse()
            .skip_while(is_blank)
            .reverse()
    )

def chomp(s):
    """Remove any trailing carriage-return or newline terminator."""
    if s.endswith("\r\n"): return s[:-2]
    if s.endswith("\n") or s.endswith("\r"): return s[:-1]
    return s


def split_on_newlines(s, keepends=False):
    "Split on newline only (not other characters, like str.splitlines()."
    if len(s) == 0:
        return
    lines = chomp(s).split("\n")

    for index, line in enumerate(lines):
        if keepends:
            if index == len(lines) - 1:
                # Last line
                if s.endswith("\n"):
                    end = "\n"
                else:
                    end = ""
            else:
                end = "\n"
        else:
            end = ""

        yield f"{line}{end}"