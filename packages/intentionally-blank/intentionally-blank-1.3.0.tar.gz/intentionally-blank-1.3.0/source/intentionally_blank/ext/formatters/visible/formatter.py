from functools import partial

from intentionally_blank.formatter import Formatter


class VisibleWhitespaceFormatter(Formatter):
    """Display whitespace using visible characters. Fixed tab size of eight.
    """

    def format(self, lines):
        """
        Args:
            lines: An iterable series of strings, each with a newline terminator.
        
        Yields:
            An iterable series of strings, each with a newline terminator.
        """
        return map(partial(transliterate_whitespace, tab_size=self.tab_size), lines)


def transliterate_whitespace(text, tab_size):
    return text.translate(str.maketrans({" ": "␣", "\t": "-" * tab_size + "→", "\n": "↵\n"}))
