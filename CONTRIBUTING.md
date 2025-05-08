# Contributing to Python Code Refactor Tool

Thank you for considering contributing to the Python Code Refactor Tool! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please help keep this project open and inclusive. By participating, you agree to respect all people involved in this project.

## How Can I Contribute?

### Reporting Bugs

- Check if the bug has already been reported in the issues
- Use the bug report template when creating a new issue
- Include detailed steps to reproduce the bug
- Include code examples if applicable
- Describe the expected behavior and what actually happened

### Suggesting Enhancements

- Check if the enhancement has already been suggested in the issues
- Use the feature request template when creating a new issue
- Provide a clear description of the proposed enhancement
- Explain why this enhancement would be useful to most users

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Submit a pull request

## Development Setup

1. Clone the repository
2. Install development dependencies:
   ```
   pip install -e ".[dev]"
   ```
3. Set up pre-commit hooks:
   ```
   pre-commit install
   ```

## Coding Conventions

- Follow PEP 8 style guide
- Use docstrings for all functions, classes, and modules
- Write unit tests for new features
- Keep functions small and focused on a single task
- Use clear variable and function names

## Adding New Refactoring Capabilities

When adding new refactoring capabilities:

1. Create appropriate functions in the relevant utility module
2. Update the documentation to reflect the new feature
3. Add tests to verify the feature works as expected
4. Update the UI to make the feature accessible to users

## Testing

- Run existing tests before submitting changes: `pytest`
- Add new tests for new features
- Ensure test coverage remains high

## Documentation

- Update the README.md when changing significant functionality
- Keep docstrings up-to-date
- Document complex code sections with inline comments

Thank you for your contributions!