import pytest
from quotes_convert.converter import QuoteConverter
from quotes_convert.model import SINGLE, DOUBLE


class TestQuoteConverterState:
    def test_initial_state(self):
        converter = QuoteConverter(SINGLE)
        assert converter.is_between_quotes is False
        assert converter.quote_character is None
        
    def test_entering_quotes(self):
        converter = QuoteConverter(SINGLE)
        converter.feed('"')
        # State changes only after processing, need second feed
        converter.feed('x')
        assert converter.is_between_quotes is True
        assert converter.quote_character == '"'
        
    def test_exiting_quotes(self):
        converter = QuoteConverter(SINGLE)
        converter.feed('"')
        converter.feed('"')
        converter.flush()
        assert converter.is_between_quotes is False
        
    def test_quote_tracking(self):
        converter = QuoteConverter(SINGLE)
        # Enter double quotes
        result1 = converter.feed('"')
        assert result1 == ""  # buffered
        
        # Regular char
        result2 = converter.feed('h')
        assert result2 == "'"  # outputs opening quote
        
        result3 = converter.feed('i')
        assert result3 == "h"
        
        # Exit quotes
        result4 = converter.feed('"')
        assert result4 == "i"
        
        # Flush
        result5 = converter.flush()
        assert result5 == "'"


class TestQuoteConverterEdgeCases:
    def test_backslash_at_end(self):
        converter = QuoteConverter(SINGLE)
        converter.feed('"')
        converter.feed('\\')
        result = converter.flush()
        assert "\\" in "".join([converter.feed('"'), result])
        
    def test_multiple_backslashes(self):
        converter = QuoteConverter(SINGLE)
        converter.feed('"')
        converter.feed('\\')
        converter.feed('\\')
        converter.feed('"')
        result = converter.flush()
        # Should handle double backslash
        
    def test_nested_different_quotes(self):
        converter = QuoteConverter(SINGLE)
        # "it's" -> 'it\'s'
        parts = []
        for ch in '"it\'s"':
            out = converter.feed(ch)
            if out:
                parts.append(out)
        parts.append(converter.flush())
        result = "".join(parts)
        assert result == "'it\\'s'"


class TestQuoteConverterFeedFlush:
    def test_feed_returns_empty_initially(self):
        converter = QuoteConverter(SINGLE)
        result = converter.feed('a')
        assert result == ""
        
    def test_flush_outputs_pending(self):
        converter = QuoteConverter(SINGLE)
        converter.feed('a')
        result = converter.flush()
        assert result == "a"
        
    def test_double_flush_empty(self):
        converter = QuoteConverter(SINGLE)
        converter.feed('a')
        converter.flush()
        result2 = converter.flush()
        assert result2 == ""
        
    def test_feed_after_flush(self):
        converter = QuoteConverter(SINGLE)
        converter.feed('a')
        converter.flush()
        # Start again
        converter.feed('b')
        result = converter.flush()
        assert result == "b"


class TestComplexPatterns:
    def test_alternating_quotes(self):
        converter = QuoteConverter(SINGLE)
        # "'""'"
        result = []
        for ch in '\'""\'"':
            out = converter.feed(ch)
            if out:
                result.append(out)
        result.append(converter.flush())
        output = "".join(result)
        assert "'" in output
        
    def test_escaped_backslash_before_quote(self):
        converter = QuoteConverter(SINGLE)
        # "\\" followed by quote
        result = []
        for ch in '"\\\\"':
            out = converter.feed(ch)
            if out:
                result.append(out)
        result.append(converter.flush())
        output = "".join(result)
        assert output == "'\\\\'"
