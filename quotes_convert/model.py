from dataclasses import dataclass

SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'
BACKSLASH = "\\"


@dataclass(frozen=True)
class QuotePolicy:
    target: str
    source: str


SINGLE = QuotePolicy(target=SINGLE_QUOTE, source=DOUBLE_QUOTE)
DOUBLE = QuotePolicy(target=DOUBLE_QUOTE, source=SINGLE_QUOTE)
