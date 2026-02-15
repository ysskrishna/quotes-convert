# quotes-convert

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ysskrishna/quotes-convert/blob/main/LICENSE)
![Tests](https://github.com/ysskrishna/quotes-convert/actions/workflows/test.yml/badge.svg)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/quotes-convert)](https://pypi.org/project/quotes-convert/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/quotes-convert?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/quotes-convert)
[![Documentation](https://img.shields.io/badge/docs-ysskrishna.github.io%2Fquotes--convert-blue.svg)](https://ysskrishna.github.io/quotes-convert/)
[![Interactive Playground](https://img.shields.io/badge/demo-Try%20it%20now!-green.svg)](https://ysskrishna.github.io/quotes-convert/playground/)

Convert matching double-quotes to single-quotes or vice versa in strings and streams. Inspired by the popular [to-single-quotes](https://github.com/sindresorhus/to-single-quotes) npm package.

> 🚀 **Try it interactively in your browser!** Test the library with our [Interactive Playground](https://ysskrishna.github.io/quotes-convert/playground/) - no installation required.

## Features

- **Multiple input types**: Convert quotes in strings and streams
- **Proper escaping**: Automatically handles quote escaping and unescaping
- **Memory efficient**: Process large texts with streaming without loading everything into memory
- **Zero dependencies**: Lightweight with no external dependencies
- **Type safe**: Full type hints for excellent IDE support

## Why use this library?

Why not just use `.replace('"', "'")`? Because simply replacing quotes breaks strings that contain escaped quotes.

```python
# The problem with simple replace
original = r'He said "Don\'t do it"'
broken   = original.replace('"', "'")
# Result: 'He said 'Don\'t do it'' -> Syntax Error!

# The solution: quotes-convert handles escaping correctly
from quotes_convert import single_quotes
fixed    = single_quotes(original)
# Result: 'He said "Don\'t do it"' -> Correctly preserves meaning
```

## Installation

```bash
pip install quotes-convert
```

## Usage Examples

### Basic Usage

```python
from quotes_convert import single_quotes, double_quotes

result = single_quotes('x = "hello"; y = "world"')
print(result)  # x = 'hello'; y = 'world'


result = double_quotes('x = "hello"; y = "world"')
print(result)  # x = "hello"; y = "world"
```

### Handling Mixed Quotes

```python
from quotes_convert import single_quotes, double_quotes

# Automatically escapes inner quotes
result = single_quotes('"it\'s working"')
print(result)  # 'it\'s working'

result = double_quotes("'say \"hi\"'")
print(result)  # "say \"hi\""
```

### Processing JSON-like Strings

Useful for normalizing JSON strings or Python dict definitions.

```python
from quotes_convert import double_quotes

json_str = "{'key': 'value', 'nested': {'inner': 'data'}}"
result = double_quotes(json_str) # {"key": "value", "nested": {"inner": "data"}}
```

### Shell Script Processing

```python
from quotes_convert import single_quotes

script = 'echo "Hello $USER"; grep "pattern" file.txt'
result = single_quotes(script) # echo 'Hello $USER'; grep 'pattern' file.txt
```

## Streaming Large Texts

Process large files or streams efficiently without loading the entire content into memory.

```python
from quotes_convert import single_quotes_stream

def line_generator():
    yield 'line 1: "hello"\n'
    yield 'line 2: "world"\n'

# Process the stream chunk by chunk
for chunk in single_quotes_stream(line_generator()):
    print(chunk, end='')

# Output:
# line 1: 'hello'
# line 2: 'world'
```

## API Reference

| Function | Description |
|----------|-------------|
| `single_quotes(text: str) -> str` | Convert matching double-quotes to single-quotes. |
| `double_quotes(text: str) -> str` | Convert matching single-quotes to double-quotes. |
| `single_quotes_stream(stream: Iterable[str]) -> Generator[str, None, None]` | Convert matching double-quotes to single-quotes in a stream, yielding chunks. |
| `double_quotes_stream(stream: Iterable[str]) -> Generator[str, None, None]` | Convert matching single-quotes to double-quotes in a stream, yielding chunks. |


## Acknowledgments

Inspired by [Sindre Sorhus](https://github.com/sindresorhus)'s [to-single-quotes](https://github.com/sindresorhus/to-single-quotes) npm package.

## Changelog

See [CHANGELOG.md](https://github.com/ysskrishna/quotes-convert/blob/main/CHANGELOG.md) for a detailed list of changes and version history.

## Contributing

Contributions are welcome! Please read our [Contributing Guide](https://github.com/ysskrishna/quotes-convert/blob/main/CONTRIBUTING.md) for details on our code of conduct, development setup, and the process for submitting pull requests.

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
  <a href="https://github.com/ysskrishna/quotes-convert/issues">Report Issues</a> •
  <a href="https://pypi.org/project/quotes-convert/">Package on PyPI</a> •
  <a href="https://ysskrishna.github.io/quotes-convert/">Package Documentation</a> •
  <a href="https://ysskrishna.github.io/quotes-convert/playground/">Package Playground</a>
</p>
