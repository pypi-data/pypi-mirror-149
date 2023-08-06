from intentionally_blank.formatter import Formatter


class IdentityFormatter(Formatter):
    """The identity formatter. No changes are made.
    """
    
    def format(self, lines):
        """
        Args:
            lines: An iterable series of strings, each with a newline terminator.
        
        Yields:
            An iterable series of strings, each with a newline terminator.
        """
        yield from lines
