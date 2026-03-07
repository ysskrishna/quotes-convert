# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0]

### Added
- **Command-Line Interface (CLI)**: New optional CLI tool for converting quotes in files and streams
  - Install with `pip install quotes-convert[cli]`
  - Supports stdin/stdout, file processing, and in-place editing
  - Options: `--single`/`-s`, `--double`/`-d`, `--in-place`/`-i`, `--output`/`-o`, `--version`/`-V`
- Comprehensive CLI documentation in dedicated `CLI.md` guide
- CLI Guide page in MkDocs documentation site
- Lazy loading of typer dependency for graceful error handling when CLI extras not installed
- Specific exception handling for file operations (FileNotFoundError, PermissionError, UnicodeDecodeError)

### Changed
- Minimum Python version updated to 3.9
- README CLI section simplified with link to full CLI Guide
- Added `cli` and `command-line` keywords to package metadata
- Added `Environment :: Console` classifier
- Added typer to dev dependencies for CLI testing
- 23 new CLI tests covering all functionality

**CLI Documentation:** [https://ysskrishna.github.io/quotes-convert/cli-guide/](https://ysskrishna.github.io/quotes-convert/cli-guide/)

## [1.1.0]

### Added
- Complete MkDocs documentation site with Material theme
- Interactive Pyodide-based playground for testing quote conversion in the browser
- API reference documentation with mkdocstrings
- Contributing guide with development setup instructions
- GitHub Actions workflow for automated documentation deployment (uv-based CI/CD)
- Theme overrides with SEO metadata, Open Graph, and Twitter card support
- Documentation badges and interactive playground links in README

**Documentation:** [https://ysskrishna.github.io/quotes-convert/](https://ysskrishna.github.io/quotes-convert/)

## [1.0.0]

### Added
- Initial release of quotes-convert Python package
- `single_quotes()` function to convert strings to use single quotes
- `double_quotes()` function to convert strings to use double quotes
- `single_quotes_stream()` function for streaming conversion to single quotes
- `double_quotes_stream()` function for streaming conversion to double quotes
- Stateful quote converter with proper escaping and unescaping
- Support for mixed quote types within strings
- Handles escaped quotes and backslashes correctly
- Type hints for better IDE support and type checking
- Zero dependencies for minimal overhead
- Comprehensive test suite with 59 tests covering edge cases
- Python 3.8+ compatibility

### Features
- Automatically converts between single and double quotes
- Properly escapes and unescapes quotes during conversion
- Stream processing support for large text processing
- Handles complex escaping scenarios

[1.2.0]: https://github.com/ysskrishna/quotes-convert/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/ysskrishna/quotes-convert/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ysskrishna/quotes-convert/releases/tag/v1.0.0
