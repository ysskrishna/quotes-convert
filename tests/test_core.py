import pytest
import json
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
    
    def test_consecutive_empty_quotes(self):
        assert single_quotes('""') == "''"
    
    def test_single_quoted_text(self):
        assert single_quotes('"foo"') == "'foo'"
    
    def test_mixed_quotes_in_text(self):
        assert single_quotes('bar "foo" baz') == "bar 'foo' baz"
    
    def test_multiple_quoted_segments(self):
        assert single_quotes('\'bar\' "foo" \'baz\'') == "'bar' 'foo' 'baz'"


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
    
    def test_consecutive_empty_quotes(self):
        assert double_quotes("''") == '""'
    
    def test_no_change_string(self):
        assert double_quotes("foo") == "foo"
    
    def test_already_double_quoted(self):
        assert double_quotes('""') == '""'
    
    def test_double_quoted_text(self):
        assert double_quotes('"foo"') == '"foo"'
    
    def test_mixed_quotes_no_change(self):
        assert double_quotes('bar "foo" baz') == 'bar "foo" baz'
    
    def test_multiple_quoted_segments(self):
        assert double_quotes('\'bar\' "foo" \'baz\'') == '"bar" "foo" "baz"'
    
    def test_escaped_single_quotes(self):
        assert double_quotes("\\'foo\\'") == '"foo"'


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
    
    def test_escaped_quotes_at_boundaries(self):
        result = single_quotes('\\"abc\\"')
        assert result == "'abc'"
        
    def test_escaped_quote_only(self):
        result = single_quotes('\\"')
        assert result == "'"
        result = double_quotes("\\'")
        assert result == '"'


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


class TestJSONStringification:
    """Test cases with JSON.stringify equivalents from JS packages"""
    
    def test_single_to_double_json_with_nested_quotes(self):
        input_str = "{'a':'<a href=\\'addr\\'>'}"
        expected = json.dumps({"a": "<a href='addr'>"}, separators=(',', ':'))
        assert double_quotes(input_str) == expected
    
    def test_single_to_double_json_with_newline_and_nested_quotes(self):
        input_str = "{'a':'aa\\n<a href=\\'addr\\'>'}"
        expected = json.dumps({"a": "aa\n<a href='addr'>"}, separators=(',', ':'))
        assert double_quotes(input_str) == expected
    
    def test_single_to_double_json_with_doubled_quotes(self):
        input_str = json.dumps({"a": 'b""c'}, separators=(',', ':'))
        expected = '{"a":"b\\"\\"c"}'
        assert double_quotes(input_str) == expected
    
    def test_double_to_single_json_with_nested_quotes(self):
        input_str = json.dumps({"a": '<a href="addr">'}, separators=(',', ':'))
        expected = "{'a':'<a href=\"addr\">'}"
        assert single_quotes(input_str) == expected
    
    def test_double_to_single_json_with_newline_and_nested_quotes(self):
        input_str = json.dumps({"a": 'aa\n<a href="addr">'}, separators=(',', ':'))
        expected = "{'a':'aa\\n<a href=\"addr\">'}"
        assert single_quotes(input_str) == expected
    
    def test_double_to_single_json_with_doubled_single_quotes(self):
        input_str = json.dumps({"a": "b''c"}, separators=(',', ':'))
        expected = "{'a':'b\\'\\'c'}"
        assert single_quotes(input_str) == expected


class TestComplexBackslashHandling:
    """Test cases for complex backslash scenarios from JS packages"""
    
    def test_single_to_double_backslash_before_quote_first_position(self):
        assert double_quotes("'1\\\"'") == '"1\\\\""'
    
    def test_single_to_double_backslash_before_quote(self):
        assert double_quotes("'\\\"'") == '"\\\\""'
    
    def test_single_to_double_double_backslash(self):
        assert double_quotes("'\\\\\"'") == '"\\\\\\""'
    
    def test_single_to_double_backslash_repetition(self):
        assert double_quotes("'\\\\\" \\\\\"'") == '"\\\\\\" \\\\\\""'
    
    def test_single_to_double_backslash_with_escape_char(self):
        assert double_quotes("'\\\\n \\\\\"'") == '"\\\\n \\\\\\""'
    
    def test_double_to_single_backslash_before_quote_first_position(self):
        assert single_quotes('"1\\\'"') == "'1\\\\''"
    
    def test_double_to_single_backslash_before_quote(self):
        assert single_quotes('"\\\'"') == "'\\\\''"
    
    def test_double_to_single_double_backslash(self):
        assert single_quotes('"\\\\\'"') == "'\\\\\\''"
    
    def test_double_to_single_backslash_repetition(self):
        assert single_quotes('"\\\\\' \\\\\'"') == "'\\\\\\' \\\\\\''"
    
    def test_double_to_single_backslash_with_escape_char(self):
        assert single_quotes('"\\\\n \\\\\'"') == "'\\\\n \\\\\\''"


class TestFixtureBased:
    """Test cases based on fixture files from JS packages"""
    
    def test_dont_touch_escaped_backslashes(self):
        input_str = '(function () {\n\tvar foo = "\\\\", bar = "\\\\\\\\";\n})();'
        expected = "(function () {\n\tvar foo = '\\\\', bar = '\\\\\\\\';\n})();"
        assert single_quotes(input_str) == expected


class TestInnerQuoteHandling:
    """Test cases for handling quotes within already-quoted strings"""
    
    def test_inner_double_quotes_in_single_quoted_string(self):
        assert single_quotes('\'bar "foo" baz\'') == "'bar \\'foo\\' baz'"


class TestReadmeExamples:
    """Test cases that match examples shown in README.md"""
    
    def test_why_use_this_library_example(self):
        """Verify the 'Why use this library?' example from README"""
        # The example from README lines 27-37
        original = '"result = \'test\'"'
        
        # Simple replace is broken (unmatched quotes)
        broken = original.replace('"', "'")
        assert broken == "'result = 'test''"  # Visibly broken
        
        # Library handles it correctly
        fixed = single_quotes(original)
        assert fixed == "'result = \\'test\\''", "Should properly escape inner quotes"
        
        # Verify content is preserved
        assert eval(original) == eval(fixed), "Content should be preserved"
