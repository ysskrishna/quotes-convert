# quotes-convert

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/ysskrishna/quotes-convert/blob/main/LICENSE)
![Tests](https://github.com/ysskrishna/quotes-convert/actions/workflows/test.yml/badge.svg)

Convert between single and double quotes in strings with proper escaping.

## Features

- **Simple API**: Four intuitive functions for quote conversion
- **Proper escaping**: Automatically handles quote escaping and unescaping
- **Stream support**: Process large texts efficiently with streaming
- **Zero dependencies**: Lightweight with no external dependencies
- **Fully typed**: Complete type hints for excellent IDE autocomplete
- **Battle-tested**: Comprehensive test suite with 59 tests covering edge cases

## Installation

```bash
pip install quotes-convert
```

## Usage Examples

### Basic Usage

```python
from quotes_convert import single_quotes, double_quotes

# Convert to single quotes
result = single_quotes('"hello world"')
print(result)  # 'hello world'

# Convert to double quotes
result = double_quotes("'hello world'")
print(result)  # "hello world"
```

### Handling Mixed Quotes

```python
# Automatically escapes inner quotes
result = single_quotes('"it\'s working"')
print(result)  # 'it\'s working'

result = double_quotes("'say \"hi\"'")
print(result)  # "say \"hi\""
```

### Multiple Quoted Strings

```python
code = 'x = "hello"; y = "world"'
result = single_quotes(code)
print(result)  # x = 'hello'; y = 'world'
```

### Stream Processing

Perfect for processing large files or continuous data:

```python
from quotes_convert import single_quotes_stream, double_quotes_stream

# Process text in chunks
chunks = ['"first', ' part" ', 'and "', 'second"']
result = "".join(single_quotes_stream(chunks))
print(result)  # 'first part' and 'second'

# Read and convert file in chunks
def read_file_chunks(filename):
    with open(filename) as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            yield chunk

converted = single_quotes_stream(read_file_chunks('input.txt'))
for chunk in converted:
    print(chunk, end='')
```

## API Reference

### Core Functions

#### `single_quotes(text: str) -> str`

Convert a string to use single quotes.

**Args:**
- `text`: The string to convert

**Returns:**
- String with single quotes

**Raises:**
- `TypeError`: If text is not a string

#### `double_quotes(text: str) -> str`

Convert a string to use double quotes.

**Args:**
- `text`: The string to convert

**Returns:**
- String with double quotes

**Raises:**
- `TypeError`: If text is not a string

### Stream Functions

#### `single_quotes_stream(stream: Iterable[str]) -> Generator[str, None, None]`

Convert a stream to use single quotes.

**Args:**
- `stream`: An iterable yielding string chunks

**Yields:**
- Converted string chunks with single quotes

**Raises:**
- `TypeError`: If stream yields non-string values

#### `double_quotes_stream(stream: Iterable[str]) -> Generator[str, None, None]`

Convert a stream to use double quotes.

**Args:**
- `stream`: An iterable yielding string chunks

**Yields:**
- Converted string chunks with double quotes

**Raises:**
- `TypeError`: If stream yields non-string values

## How It Works

The library uses a state machine to track whether it's currently inside quotes and what type of quotes are being used. This allows it to:

1. Convert outer quotes to the target type
2. Properly escape inner quotes of the target type
3. Unescape inner quotes of the source type
4. Handle backslash escaping correctly

## Real-World Examples

### Converting Code Formatting

```python
# Convert Python code to use single quotes
code = '''
def greet(name):
    return "Hello, " + name
'''

result = single_quotes(code)
# def greet(name):
#     return 'Hello, ' + name
```

### Processing JSON-like Strings

```python
json_str = "{'key': 'value', 'nested': {'inner': 'data'}}"
result = double_quotes(json_str)
# {"key": "value", "nested": {"inner": "data"}}
```

### Shell Script Processing

```python
script = 'echo "Hello $USER"; grep "pattern" file.txt'
result = single_quotes(script)
# echo 'Hello $USER'; grep 'pattern' file.txt
```

## Limitations

- Only handles single (`'`) and double (`"`) quotes, not backticks
- Processes character-by-character, which is safe but may be slower for very large texts
- Assumes standard backslash escaping conventions

## Changelog

See [CHANGELOG.md](https://github.com/ysskrishna/quotes-convert/blob/main/CHANGELOG.md) for a detailed list of changes and version history.

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/ysskrishna/quotes-convert/blob/main/CONTRIBUTING.md) for details.

## Support

If you find this library helpful:

- ⭐ Star the repository
- 🐛 Report issues
- 🔀 Submit pull requests
- 💝 [Sponsor on GitHub](https://github.com/sponsors/ysskrishna)

## License

MIT © [Y. Siva Sai Krishna](https://github.com/ysskrishna) - see [LICENSE](https://github.com/ysskrishna/quotes-convert/blob/main/LICENSE) file for details.

---

<p align="left">
  <a href="https://github.com/ysskrishna">Author's GitHub</a> •
  <a href="https://linkedin.com/in/ysskrishna">Author's LinkedIn</a> •
  <a href="https://github.com/ysskrishna/quotes-convert/issues">Report Issues</a>
</p>
