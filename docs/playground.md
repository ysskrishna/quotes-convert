---
title: Interactive Demo
description: "Try quotes-convert Python library examples. See how to convert quotes in strings and process streams efficiently."
keywords:
  - interactive demo
  - examples
  - quote conversion
  - streaming
  - code examples
---

# Interactive Playground

Try out `quotes-convert` with these examples! You can copy and run them in your Python environment.

## Basic Quote Conversion

```python
from quotes_convert import single_quotes, double_quotes

# Convert to single quotes
text = 'x = "hello"; y = "world"'
result = single_quotes(text)
print(result)  # x = 'hello'; y = 'world'

# Convert to double quotes
text = "x = 'hello'; y = 'world'"
result = double_quotes(text)
print(result)  # x = "hello"; y = "world"
```

## Handling Escaping

```python
from quotes_convert import single_quotes, double_quotes

# Automatically escapes inner quotes
text = '"it\'s working"'
result = single_quotes(text)
print(result)  # 'it\'s working'

# Reverse conversion
text = "'say \"hi\"'"
result = double_quotes(text)
print(result)  # "say \"hi\""
```

## Processing Streams

```python
from quotes_convert import single_quotes_stream

def line_generator():
    yield 'line 1: "hello"\n'
    yield 'line 2: "world"\n'
    yield 'line 3: "foo bar"\n'

# Process the stream chunk by chunk
for chunk in single_quotes_stream(line_generator()):
    print(chunk, end='')

# Output:
# line 1: 'hello'
# line 2: 'world'
# line 3: 'foo bar'
```

## JSON Normalization

```python
from quotes_convert import double_quotes

# Convert Python-style dict to JSON-style
python_dict = "{'key': 'value', 'nested': {'inner': 'data'}}"
json_style = double_quotes(python_dict)
print(json_style)
# {"key": "value", "nested": {"inner": "data"}}
```

## Large File Processing

```python
from quotes_convert import single_quotes_stream

def read_file_chunks(filename, chunk_size=8192):
    with open(filename, 'r') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Process large file without loading it all into memory
with open('output.txt', 'w') as out:
    for converted_chunk in single_quotes_stream(read_file_chunks('input.txt')):
        out.write(converted_chunk)
```

## Try it Yourself

Install the library and try these examples:

```bash
pip install quotes-convert
```

Then run the examples in your Python REPL or script!

## Need Help?

- Check the [API Reference](api-reference.md) for detailed function documentation
- See the [GitHub repository](https://github.com/ysskrishna/quotes-convert) for more examples
- [Report issues](https://github.com/ysskrishna/quotes-convert/issues) if you find bugs
