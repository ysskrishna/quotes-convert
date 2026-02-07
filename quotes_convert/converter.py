from typing import Optional, Tuple
from .model import SINGLE_QUOTE, DOUBLE_QUOTE, BACKSLASH, QuotePolicy


class QuoteConverter:
    def __init__(self, policy: QuotePolicy):
        self.target = policy.target
        self.source = policy.source

        self.is_between_quotes = False
        self.quote_character: Optional[str] = None
        self._pending: Optional[str] = None

    def feed(self, char: str) -> str:
        if self._pending is None:
            self._pending = char
            return ""

        current = self._pending
        next_char = char

        out, consumed = self._process(current, next_char)
        self._pending = None if consumed else next_char
        return out

    def flush(self) -> str:
        if self._pending is None:
            return ""

        ch = self._pending
        self._pending = None
        out, _ = self._process(ch, None)
        return out

    def _process(
        self, current: str, next_char: Optional[str]
    ) -> Tuple[str, bool]:

        if current in (SINGLE_QUOTE, DOUBLE_QUOTE):
            if not self.is_between_quotes:
                self.quote_character = current
                self.is_between_quotes = True
                return self.target, False

            if self.quote_character == current:
                self.is_between_quotes = False
                return self.target, False

            return BACKSLASH + self.target, False

        if current == BACKSLASH and next_char in (SINGLE_QUOTE, DOUBLE_QUOTE):
            if next_char == self.target:
                if (
                    self.is_between_quotes
                    and self.quote_character == self.target
                ):
                    return BACKSLASH + self.target, True

                return BACKSLASH + BACKSLASH + self.target, True

            if next_char == self.source:
                return (
                    self.source if self.is_between_quotes else self.target,
                    True,
                )

        if current == BACKSLASH and next_char == BACKSLASH:
            return BACKSLASH + BACKSLASH, True

        return current, False
