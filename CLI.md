# CLI Guide

The `quotes-convert` CLI provides a convenient way to convert quotes in files and streams directly from your terminal.

## Installation

The CLI requires the `typer` dependency, which is installed as an optional extra:

```bash
pip install quotes-convert[cli]
```

## Quick Start

```bash
# Convert to single quotes
echo 'x = "hello"' | quotes-convert --single

# Convert to double quotes
echo "x = 'hello'" | quotes-convert --double

# Use short flags
quotes-convert -s file.py
quotes-convert -d file.py

# Check version
quotes-convert --version
```

## Command Reference

```
quotes-convert [OPTIONS] [FILES]...
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--single` | `-s` | Convert matching quotes to single quotes |
| `--double` | `-d` | Convert matching quotes to double quotes |
| `--in-place` | `-i` | Edit files in place (requires file arguments) |
| `--output PATH` | `-o PATH` | Write output to specified file |
| `--version` | `-V` | Show version and exit |
| `--help` | | Show help message and exit |

### Arguments

| Argument | Description |
|----------|-------------|
| `FILES` | Files to convert. If not provided, reads from stdin. |

## Usage Patterns

### 1. Standard Input/Output (Pipes)

Process text from stdin and output to stdout:

```bash
# From echo
echo 'name = "Alice"' | quotes-convert -s
# Output: name = 'Alice'

# From file via cat
cat script.py | quotes-convert -s

# Chain with other commands
cat data.txt | quotes-convert -s | grep "pattern"
```

### 2. File to Standard Output

Preview changes before modifying files:

```bash
# Display converted content
quotes-convert -s myfile.py

# Check before applying
quotes-convert -s config.py | less
```

### 3. In-Place File Editing

Modify files directly:

```bash
# Single file
quotes-convert -s -i script.py

# Multiple files
quotes-convert -s -i file1.py file2.py file3.py

# Glob patterns (shell expansion)
quotes-convert -s -i src/*.py
quotes-convert -s -i *.py
```

> **Warning:** In-place editing modifies files directly. Always use version control (git) or create backups before batch editing.

### 4. Output to File

Save converted content to a new file:

```bash
# From stdin
echo 'x = "test"' | quotes-convert -s -o output.py

# From file
quotes-convert -s input.py -o output.py
```

## Real-World Examples

### Python Code Formatting

```bash
# Convert Python files to use single quotes
quotes-convert -s -i src/*.py tests/*.py

# Preview changes first
quotes-convert -s main.py > /tmp/preview.py
diff main.py /tmp/preview.py
```

### JavaScript/TypeScript Projects

```bash
# Convert to double quotes
quotes-convert -d -i src/*.ts src/*.js
```

### Batch Processing with Find

```bash
# Convert all Python files in a directory tree
find . -name "*.py" -type f -exec quotes-convert -s -i {} \;

# With progress indicator
find . -name "*.py" -type f | while read f; do
    echo "Processing: $f"
    quotes-convert -s -i "$f"
done
```

### Parallel Processing with xargs

```bash
# Process 4 files at a time in parallel
find . -name "*.py" | xargs -P 4 -n 1 quotes-convert -s -i
```

### Integration with Git

```bash
# Convert only staged Python files
git diff --cached --name-only | grep '\.py$' | xargs quotes-convert -s -i

# Convert files changed in current branch vs main
git diff --name-only main | grep '\.py$' | xargs quotes-convert -s -i
```

### Shell Aliases

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias sq='quotes-convert --single'
alias dq='quotes-convert --double'
alias sqi='quotes-convert --single --in-place'
alias dqi='quotes-convert --double --in-place'
```

Usage:

```bash
sq file.py           # preview
sqi file.py          # in-place
echo 'x="y"' | sq    # pipe
```

## Error Handling

The CLI provides clear error messages for common issues:

### Missing Quote Style

```bash
$ quotes-convert file.py
Error: Must specify either --single or --double
```

### Conflicting Options

```bash
$ quotes-convert -s -d file.py
Error: Cannot specify both --single and --double

$ quotes-convert -s -i -o output.py file.py
Error: Cannot specify both --in-place and --output
```

### File Not Found

```bash
$ quotes-convert -s nonexistent.txt
Error: Invalid value for '[FILES]...': Path 'nonexistent.txt' does not exist.
```

### Permission Denied

```bash
$ quotes-convert -s -i /root/protected.py
Error: Permission denied: /root/protected.py
```

### Non-UTF-8 Files

```bash
$ quotes-convert -s binary.dat
Error: Cannot decode file (not UTF-8): binary.dat
```

## Performance Tips

### Streaming Mode

The CLI uses streaming by default when not editing in-place, efficiently handling large files:

```bash
# Efficiently handles large files
quotes-convert -s huge_file.txt > output.txt
```

### Memory Usage

- **Streaming mode** (default): Low memory, handles any file size
- **In-place mode** (`-i`): Loads entire file into memory

### Parallel Processing

For many files, use parallel processing:

```bash
# Process 4 files at a time
find . -name "*.py" | xargs -P 4 -n 1 quotes-convert -s -i
```

## Troubleshooting

### CLI Command Not Found

If `quotes-convert` command is not found:

```bash
# Ensure CLI extras are installed
pip install quotes-convert[cli]

# Verify installation
pip show quotes-convert

# Check if it's in PATH
which quotes-convert

# Alternative: run with python -m
python -m quotes_convert.cli --help
```

### Import Errors

If you get "CLI dependencies not installed":

```bash
# Reinstall with CLI extras
pip install --force-reinstall quotes-convert[cli]
```

### Unexpected Results

```bash
# Check version
quotes-convert --version

# Test with simple input
echo 'test = "value"' | quotes-convert -s
```

## See Also

- [API Reference](https://ysskrishna.github.io/quotes-convert/api-reference/) - Library API documentation
- [Interactive Playground](https://ysskrishna.github.io/quotes-convert/playground/) - Try it in your browser
- [Contributing Guide](https://github.com/ysskrishna/quotes-convert/blob/main/CONTRIBUTING.md) - Help improve the CLI
