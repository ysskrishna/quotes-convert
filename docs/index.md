# quotes_convert

Convert matching double-quotes to single-quotes or vice versa in strings and streams.

## Installation

```bash
pip install quotes-convert
```

## Quick start

```python
from quotes_convert import single_quotes, double_quotes, single_quotes_stream

# Convert a single string to single quotes
text = '{"name": "Alice", "msg": "He said \\"Hello\\""}'
print(single_quotes(text))

# Convert a stream (generator of chunks)
def chunks():
    yield '{"a": "b",'
    yield ' "c": "d"}'

for out_chunk in single_quotes_stream(chunks()):
    print(out_chunk, end="")
```

## Features

- Convert strings to single or double quotes
- Stream-safe incremental conversion for large inputs
- Zero dependencies, typed package

## Contributing

See the repository `CONTRIBUTING.md` for contribution guidelines.

