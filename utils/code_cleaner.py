import ast
import re
import autopep8
import black
import isort
from io import StringIO

def clean_code(code):
    """
    Clean the given Python code by:
    1. Sorting imports
    2. Formatting to PEP8 standards
    3. Removing unused imports
    4. Removing unused variables
    
    Args:
        code (str): The Python code to clean
        
    Returns:
        str: The cleaned Python code
    """
    # First, check if the code is valid Python
    try:
        ast.parse(code)
    except SyntaxError:
        # If there's a syntax error, return the original code
        return code
    
    # Sort imports
    code = sort_imports(code)
    
    # Format code with black
    try:
        code = format_with_black(code)
    except Exception:
        # If black fails, try autopep8
        code = format_with_autopep8(code)
    
    # Remove unused imports
    code = remove_unused_imports(code)
    
    # Remove unused variables
    code = remove_unused_variables(code)
    
    return code

def sort_imports(code):
    """Sort imports using isort."""
    try:
        return isort.code(code)
    except Exception:
        return code

def format_with_black(code):
    """Format code using black."""
    try:
        return black.format_str(code, mode=black.FileMode())
    except Exception:
        return code

def format_with_autopep8(code):
    """Format code using autopep8."""
    try:
        return autopep8.fix_code(code, options={'aggressive': 1})
    except Exception:
        return code

def remove_unused_imports(code):
    """Remove unused imports from the code."""
    try:
        tree = ast.parse(code)
        
        # Get all imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append((name.name, name.asname, node))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for name in node.names:
                    if name.name == "*":
                        # Can't analyze wildcard imports safely
                        continue
                    imports.append((f"{module}.{name.name}", name.asname, node))
        
        # Get all used names
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
                if isinstance(node.value, ast.Name):
                    used_names.add(node.value.id)
        
        # Identify unused imports
        lines_to_remove = set()
        for import_name, alias, node in imports:
            name_to_check = alias if alias else import_name.split('.')[-1]
            if name_to_check not in used_names:
                lines_to_remove.add(node.lineno)
        
        # Remove unused import lines
        if lines_to_remove:
            code_lines = code.split('\n')
            cleaned_lines = [line for i, line in enumerate(code_lines, 1) if i not in lines_to_remove]
            return '\n'.join(cleaned_lines)
        
        return code
    except Exception:
        return code

def remove_unused_variables(code):
    """Remove unused variables from the code."""
    try:
        tree = ast.parse(code)
        
        # Get all variable assignments
        variables = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables[target.id] = node.lineno
        
        # Get all variable usages
        used_vars = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_vars.add(node.id)
        
        # Find unused variables
        unused_vars = set()
        for var, line in variables.items():
            if var not in used_vars and not var.startswith('_'):
                unused_vars.add(var)
        
        # Remove unused variable assignments
        if unused_vars:
            # This is a simplistic approach. A proper implementation would 
            # remove the specific assignments, but that requires manipulating the AST
            # or using a more sophisticated approach.
            # For now, we'll just identify the assignments that should be removed.
            lines_to_check = []
            for var in unused_vars:
                lines_to_check.append(variables[var])
            
            # This is a very basic implementation that might miss some cases or 
            # remove too much, but it's a starting point.
            code_lines = code.split('\n')
            cleaned_lines = []
            for i, line in enumerate(code_lines, 1):
                if i in lines_to_check and re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=', line):
                    # Skip lines that look like simple assignments of unused variables
                    continue
                cleaned_lines.append(line)
            
            return '\n'.join(cleaned_lines)
        
        return code
    except Exception:
        return code
