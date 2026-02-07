import pytest
from quotes_convert import single_quotes_stream, double_quotes_stream


class TestSingleQuotesStream:
    def test_simple_conversion(self):
        stream = ['"hel', 'lo"']
        result = "".join(single_quotes_stream(stream))
        assert result == "'hello'"
        
    def test_single_chunk(self):
        stream = ['"hello"']
        result = "".join(single_quotes_stream(stream))
        assert result == "'hello'"
        
    def test_many_chunks(self):
        stream = ['"', 'h', 'e', 'l', 'l', 'o', '"']
        result = "".join(single_quotes_stream(stream))
        assert result == "'hello'"
        
    def test_empty_stream(self):
        stream = []
        result = "".join(single_quotes_stream(stream))
        assert result == ""
        
    def test_empty_strings_in_stream(self):
        stream = ['', '"hello"', '']
        result = "".join(single_quotes_stream(stream))
        assert result == "'hello'"
        
    def test_quote_split_across_chunks(self):
        stream = ['"hel', 'lo wo', 'rld"']
        result = "".join(single_quotes_stream(stream))
        assert result == "'hello world'"
        
    def test_backslash_at_chunk_boundary(self):
        stream = ['"test\\', '"end"']
        result = "".join(single_quotes_stream(stream))
        # Backslash before quote
        assert "'" in result


class TestDoubleQuotesStream:
    def test_simple_conversion(self):
        stream = ["'hel", "lo'"]
        result = "".join(double_quotes_stream(stream))
        assert result == '"hello"'
        
    def test_single_chunk(self):
        stream = ["'hello'"]
        result = "".join(double_quotes_stream(stream))
        assert result == '"hello"'
        
    def test_many_chunks(self):
        stream = ["'", 'h', 'e', 'l', 'l', 'o', "'"]
        result = "".join(double_quotes_stream(stream))
        assert result == '"hello"'
        
    def test_empty_stream(self):
        stream = []
        result = "".join(double_quotes_stream(stream))
        assert result == ""


class TestStreamEdgeCases:
    def test_mixed_quotes_across_chunks(self):
        stream = ['"it', "\'s", ' ok"']
        result = "".join(single_quotes_stream(stream))
        assert result == "'it\\'s ok'"
        
    def test_escape_sequence_split(self):
        stream = ['"test', '\\"', 'end"']
        result = "".join(single_quotes_stream(stream))
        # Should handle escape properly
        assert "'" in result
        
    def test_multiple_strings_in_stream(self):
        stream = ['"first" and ', "'second'"]
        result = "".join(single_quotes_stream(stream))
        assert result == "'first' and 'second'"


class TestStreamTypeErrors:
    def test_stream_with_non_string(self):
        stream = ['"hello"', 123]
        with pytest.raises(TypeError):
            list(single_quotes_stream(stream))
            
    def test_stream_with_none(self):
        stream = ['"hello"', None]
        with pytest.raises(TypeError):
            list(double_quotes_stream(stream))


class TestStreamGenerator:
    def test_is_generator(self):
        stream = ['"hello"']
        result = single_quotes_stream(stream)
        assert hasattr(result, '__iter__')
        assert hasattr(result, '__next__')
        
    def test_lazy_evaluation(self):
        called = []
        
        def gen():
            called.append(1)
            yield '"hel'
            called.append(2)
            yield 'lo"'
            
        result = single_quotes_stream(gen())
        # Generator not executed yet
        assert len(called) == 0
        
        # Consume generator
        list(result)
        assert len(called) == 2
