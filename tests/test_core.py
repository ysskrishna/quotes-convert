import pytest
from quotes_convert import single_quotes, double_quotes


class TestSingleQuotes:
    def test_simple_double_to_single(self):
        assert single_quotes('"hello"') == "'hello'"
        
    def test_simple_single_remains(self):
        assert single_quotes("'hello'") == "'hello'"
        
    def test_empty_string(self):
        assert single_quotes("") == ""
        
    def test_no_quotes(self):
        assert single_quotes("hello world") == "hello world"
        
    def test_escaped_quotes_inside(self):
        assert single_quotes('"say \\"hi\\""') == '\'say "hi"\''
        
    def test_mixed_quotes(self):
        assert single_quotes('"it\'s"') == "'it\\'s'"
        
    def test_double_backslash(self):
        assert single_quotes('"\\\\"') == "'\\\\'"
        
    def test_text_with_quotes(self):
        result = single_quotes('x = "hello"')
        assert result == "x = 'hello'"


class TestDoubleQuotes:
    def test_simple_single_to_double(self):
        assert double_quotes("'hello'") == '"hello"'
        
    def test_simple_double_remains(self):
        assert double_quotes('"hello"') == '"hello"'
        
    def test_empty_string(self):
        assert double_quotes("") == ""
        
    def test_no_quotes(self):
        assert double_quotes("hello world") == "hello world"
        
    def test_escaped_quotes_inside(self):
        assert double_quotes("'say \\'hi\\''") == '"say \'hi\'"'
        
    def test_mixed_quotes(self):
        assert double_quotes("'it\"s'") == '"it\\"s"'
        
    def test_double_backslash(self):
        assert double_quotes("'\\\\'") == '"\\\\"'
        
    def test_text_with_quotes(self):
        result = double_quotes("x = 'hello'")
        assert result == 'x = "hello"'


class TestEdgeCases:
    def test_only_quote(self):
        assert single_quotes('"') == "'"
        assert double_quotes("'") == '"'
        
    def test_only_backslash(self):
        assert single_quotes("\\") == "\\"
        assert double_quotes("\\") == "\\"
        
    def test_unmatched_quote(self):
        result = single_quotes('"hello')
        assert result == "'hello"
        
    def test_consecutive_quotes(self):
        assert single_quotes('""') == "''"
        assert double_quotes("''") == '""'


class TestTypeErrors:
    def test_single_quotes_not_string(self):
        with pytest.raises(TypeError):
            single_quotes(123)
            
    def test_double_quotes_not_string(self):
        with pytest.raises(TypeError):
            double_quotes(None)


class TestComplexEscaping:
    def test_multiple_escaped_quotes(self):
        result = single_quotes('"a\\"b\\"c"')
        assert result == '\'a"b"c\''
        
    def test_backslash_before_non_quote(self):
        result = single_quotes('"test\\n"')
        assert result == "'test\\n'"
        
    def test_quote_inside_quote(self):
        result = double_quotes("'can\\'t'")
        assert result == '"can\'t"'


class TestMultipleQuotedStrings:
    def test_two_strings(self):
        result = single_quotes('"first" "second"')
        assert result == "'first' 'second'"
        
    def test_mixed_quote_types(self):
        result = single_quotes('"double" and \'single\'')
        assert result == "'double' and 'single'"
        
    def test_nested_structure(self):
        result = single_quotes('x = "value"; y = "other"')
        assert result == "x = 'value'; y = 'other'"
