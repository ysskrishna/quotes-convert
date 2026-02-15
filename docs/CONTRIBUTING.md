---
title: Contributing Guide
description: "Learn how to contribute to quotes-convert. Guidelines for reporting issues, submitting pull requests, and improving the library."
keywords:
  - contributing
  - contribution guide
  - pull requests
  - issues
  - development
---

# Contributing to quotes-convert

We welcome contributions! This guide will help you get started.

## Reporting Issues

If you find a bug or have a feature request, please [open an issue](https://github.com/ysskrishna/quotes-convert/issues) on GitHub.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ysskrishna/quotes-convert.git
   cd quotes-convert
   ```

2. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```

3. Run tests:
   ```bash
   pytest
   ```

## Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests to ensure everything passes
5. Commit your changes: `git commit -m "Add my feature"`
6. Push to your fork: `git push origin feature/my-feature`
7. Open a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Add type hints to all functions
- Write docstrings for public APIs
- Keep the code simple and readable

## Testing

- Write tests for new features
- Ensure all existing tests pass
- Aim for high code coverage

## Questions?

Feel free to open an issue or reach out to the maintainers!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
