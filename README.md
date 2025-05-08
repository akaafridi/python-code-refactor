# 🔧 Python Code Refactor Tool

A powerful, easy-to-use Python Code Refactoring Tool built with Replit. It automatically cleans, restructures, and optimizes Python code based on modern coding standards.

## 🚀 Features

- 🧹 **Code Cleanup** – Removes unused imports, dead code, and bad formatting.
- 🛠️ **Refactoring Engine** – Renames variables for clarity, extracts functions, and applies PEP8.
- 🪞 **Before vs After** – View side-by-side diffs to see exactly what's changed.
- 📁 **Batch Mode** – Upload single files or entire folders to refactor in bulk.
- 🔍 **Highlight Changes** – Color-coded differences to track refactoring impact.
- 📤 **Export Refactored Code** – Download cleaned code with one click.
- 🧠 Built using AI-powered code understanding and parsing tools.

## 🖥️ Built With

- Python 3.11+
- Streamlit (for web interface)
- `autopep8`, `black`, `isort` for code formatting
- Custom AST-based logic for advanced analysis
- Replit for seamless deployment

## 💻 Code Quality Checks

The tool performs numerous code quality checks including:

- Unused imports and variables
- Complex expressions and nested loops
- Long functions and code duplication
- Poorly named variables and magic numbers
- Missing docstrings and excessive line length
- Functions with too many arguments
- Global variables and improper structuring

## 🛠️ Refactoring Capabilities

- Automatic formatting to PEP8 standards
- Import organization and cleaning
- Variable renaming for better clarity
- Function extraction for repeated code
- Code simplification and organization
- Application of DRY (Don't Repeat Yourself) principles
- Comprehensive metrics and improvement reports

## 📸 Screenshots

| Before | After |
|--------|-------|
| `def do(a): print(a*a)` | `def square(x): """Calculate the square of a number.""" print(x * x)` |

## ⚙️ Usage

### 🔗 Live on Replit

> Click to run: [Run on Replit](https://replit.com/@YOUR_USERNAME/python-code-refactor)

### 🧪 Local Setup

```bash
git clone https://github.com/username/python-code-refactor.git
cd python-code-refactor
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure

```
├── app.py                 # Main Streamlit application
├── utils/
│   ├── __init__.py
│   ├── code_analyzer.py   # Code analysis functionality
│   ├── code_cleaner.py    # Code cleaning and formatting
│   ├── code_refactor.py   # Code refactoring logic
│   └── diff_generator.py  # Generates visual diff between original and refactored code
├── .streamlit/
│   └── config.toml        # Streamlit configuration
```

## 🔮 Future Improvements

- Automated docstring generation
- Unit test generation and recommendations
- Support for more programming languages
- Enhanced visualizations for code metrics
- Custom rule configurations
- Integration with GitHub and GitLab workflows

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Black](https://github.com/psf/black) - The uncompromising Python code formatter
- [isort](https://pycqa.github.io/isort/) - Python utility to sort imports
- [autopep8](https://github.com/hhatto/autopep8) - Python code formatter based on PEP 8
- [Streamlit](https://streamlit.io/) - Framework for building data apps