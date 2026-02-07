from typing import Iterable, Generator
from quotes_convert.converter import QuoteConverter
from quotes_convert.model import QuotePolicy, SINGLE, DOUBLE


def _convert_text(text: str, policy: QuotePolicy) -> str:
    """Convert quotes in text according to the given policy.
    
    Args:
        text: The string to convert
        policy: The quote conversion policy
        
    Returns:
        Converted string
        
    Raises:
        TypeError: If text is not a string
    """
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
    """Convert quotes in a stream according to the given policy.
    
    Args:
        iterable: An iterable yielding string chunks
        policy: The quote conversion policy
        
    Yields:
        Converted string chunks
        
    Raises:
        TypeError: If stream yields non-string values
    """
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
