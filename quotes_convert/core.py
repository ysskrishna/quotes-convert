from typing import Iterable, Generator
from .converter import QuoteConverter
from .model import QuotePolicy, SINGLE, DOUBLE


def _convert_text(text: str, policy: QuotePolicy) -> str:
    if not isinstance(text, str):
        raise TypeError("expected str")

    converter = QuoteConverter(policy)
    out = []

    for ch in text:
        piece = converter.feed(ch)
        if piece:
            out.append(piece)

    tail = converter.flush()
    if tail:
        out.append(tail)

    return "".join(out)


def single_quotes(text: str) -> str:
    """Convert a string to use single quotes.
    
    Args:
        text: The string to convert
        
    Returns:
        String with single quotes
    """
    return _convert_text(text, SINGLE)


def double_quotes(text: str) -> str:
    """Convert a string to use double quotes.
    
    Args:
        text: The string to convert
        
    Returns:
        String with double quotes
    """
    return _convert_text(text, DOUBLE)


def _convert_stream(
    iterable: Iterable[str], policy: QuotePolicy
) -> Generator[str, None, None]:

    converter = QuoteConverter(policy)

    for chunk in iterable:
        if not isinstance(chunk, str):
            raise TypeError("stream must yield str")

        for ch in chunk:
            out = converter.feed(ch)
            if out:
                yield out

    tail = converter.flush()
    if tail:
        yield tail


def single_quotes_stream(stream: Iterable[str]) -> Generator[str, None, None]:
    """Convert a stream to use single quotes.
    
    Args:
        stream: An iterable yielding string chunks
        
    Yields:
        Converted string chunks with single quotes
    """
    return _convert_stream(stream, SINGLE)


def double_quotes_stream(stream: Iterable[str]) -> Generator[str, None, None]:
    """Convert a stream to use double quotes.
    
    Args:
        stream: An iterable yielding string chunks
        
    Yields:
        Converted string chunks with double quotes
    """
    return _convert_stream(stream, DOUBLE)
