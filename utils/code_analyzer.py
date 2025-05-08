import ast
import builtins
import re
from collections import Counter

def analyze_code(code):
    """
    Analyze the given Python code to identify potential issues and improvements.
    
    Args:
        code (str): The Python code to analyze
        
    Returns:
        dict: Analysis results containing various categories of issues
    """
    analysis_result = {
        "Unused Imports": [],
        "Unused Variables": [],
        "Complex Expressions": [],
        "Nested Loops": [],
        "Long Functions": [],
        "Code Duplication": [],
        "Poorly Named Variables": [],
        "Magic Numbers": [],
        "Missing Docstrings": [],
        "Excessive Line Length": [],
        "Too Many Arguments": [],
        "Global Variables": []
    }
    
    try:
        tree = ast.parse(code)
        
        # Track imports and their usage
        imports = _get_imports(tree)
        used_names = _get_used_names(tree)
        unused_imports = _find_unused_imports(imports, used_names)
        analysis_result["Unused Imports"] = unused_imports
        
        # Find unused variables
        variables = _get_variables(tree)
        unused_vars = _find_unused_variables(variables, used_names)
        analysis_result["Unused Variables"] = unused_vars
        
        # Find complex expressions and nested loops
        complex_expr, nested_loops = _find_complex_code(tree)
        analysis_result["Complex Expressions"] = complex_expr
        analysis_result["Nested Loops"] = nested_loops
        
        # Find long functions
        long_funcs = _find_long_functions(tree, code)
        analysis_result["Long Functions"] = long_funcs
        
        # Find poorly named variables
        poor_names = _find_poor_variable_names(variables)
        analysis_result["Poorly Named Variables"] = poor_names
        
        # Find magic numbers
        magic_numbers = _find_magic_numbers(tree)
        analysis_result["Magic Numbers"] = magic_numbers
        
        # Find duplicated code
        duplications = _find_duplicated_code(tree, code)
        analysis_result["Code Duplication"] = duplications
        
        # Find missing docstrings
        missing_docs = _find_missing_docstrings(tree)
        analysis_result["Missing Docstrings"] = missing_docs
        
        # Find excessive line lengths
        long_lines = _find_excessive_line_length(code)
        analysis_result["Excessive Line Length"] = long_lines
        
        # Find functions with too many arguments
        too_many_args = _find_too_many_arguments(tree)
        analysis_result["Too Many Arguments"] = too_many_args
        
        # Find global variables
        globals_found = _find_global_variables(tree)
        analysis_result["Global Variables"] = globals_found
        
    except SyntaxError as e:
        # Return syntax error if code cannot be parsed
        return {"Syntax Errors": [f"Line {e.lineno}: {e.msg}"]}
    except Exception as e:
        # Return general error for other exceptions
        return {"Errors": [str(e)]}
    
    return analysis_result

def _get_imports(tree):
    """Extract all imports from the AST."""
    imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.append(name.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for name in node.names:
                if name.name == "*":
                    imports.append(f"{module}.*")
                else:
                    imports.append(f"{module}.{name.name}")
    
    return imports

def _get_used_names(tree):
    """Get all names that are used in the code."""
    used_names = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used_names.add(node.id)
        elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
            # Handle attributes like module.function
            if isinstance(node.value, ast.Name):
                used_names.add(f"{node.value.id}.{node.attr}")
                used_names.add(node.value.id)  # Also add the module name
    
    return used_names

def _find_unused_imports(imports, used_names):
    """Find imports that are not used in the code."""
    unused = []
    
    for imp in imports:
        parts = imp.split('.')
        if not any(imp == used or imp.startswith(used + '.') or 
                  any(used.startswith(p + '.') for p in parts) for used in used_names):
            unused.append(f"Import '{imp}' is not used")
    
    return unused

def _get_variables(tree):
    """Get all variable declarations in the code."""
    variables = {}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variables[target.id] = getattr(node, 'lineno', 0)
    
    return variables

def _find_unused_variables(variables, used_names):
    """Find variables that are declared but not used."""
    unused = []
    builtin_names = dir(builtins)
    
    for var, line in variables.items():
        if var not in used_names and var not in builtin_names and not var.startswith('_'):
            unused.append(f"Variable '{var}' declared on line {line} is never used")
    
    return unused

def _find_complex_code(tree):
    """Find complex expressions and nested loops."""
    complex_expr = []
    nested_loops = []
    
    for node in ast.walk(tree):
        # Check for complex boolean expressions
        if isinstance(node, ast.BoolOp) and len(node.values) > 3:
            complex_expr.append(f"Complex boolean expression with {len(node.values)} conditions at line {node.lineno}")
        
        # Check for nested loops
        if isinstance(node, (ast.For, ast.While)):
            nested = _check_nested_loops(node)
            if nested > 1:  # More than 1 level of nesting
                nested_loops.append(f"Nested loop with {nested} levels at line {node.lineno}")
    
    return complex_expr, nested_loops

def _check_nested_loops(node, level=1):
    """Recursively check for nested loops and return the nesting level."""
    max_level = level
    
    for child_node in ast.iter_child_nodes(node):
        if isinstance(child_node, (ast.For, ast.While)):
            nested_level = _check_nested_loops(child_node, level + 1)
            max_level = max(max_level, nested_level)
    
    return max_level

def _find_long_functions(tree, code):
    """Find functions that are too long (more than 30 lines)."""
    long_funcs = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Calculate lines of code in the function
            source_segment = ast.get_source_segment(code, node)
            if source_segment:
                func_lines = len(source_segment.split('\n'))
                if func_lines > 30:
                    long_funcs.append(f"Function '{node.name}' has {func_lines} lines (over 30) at line {node.lineno}")
    
    return long_funcs

def _find_poor_variable_names(variables):
    """Find variables with poor names (too short or not descriptive)."""
    poor_names = []
    
    for var, line in variables.items():
        # Skip special variables
        if var.startswith('_') or var in ('i', 'j', 'k', 'x', 'y', 'z'):
            continue
        
        # Check for single character names that aren't common loop variables
        if len(var) == 1 and var not in ('i', 'j', 'k', 'x', 'y', 'z'):
            poor_names.append(f"Variable '{var}' at line {line} has a single-character name")
        
        # Check for non-descriptive names
        if var in ('temp', 'tmp', 'var', 'foo', 'bar'):
            poor_names.append(f"Variable '{var}' at line {line} has a non-descriptive name")
    
    return poor_names

def _find_magic_numbers(tree):
    """Find magic numbers (hardcoded numeric literals)."""
    magic_numbers = []
    allowed = (0, 1, -1, 2, 10, 100)  # Common numbers that are often not considered "magic"
    
    for node in ast.walk(tree):
        # Check for ast.Constant with numeric values (Python 3.8+)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            if node.value not in allowed:
                magic_numbers.append(f"Magic number {node.value} at line {getattr(node, 'lineno', 0)}")
        # Backwards compatibility for older Python versions using ast.Num
        elif hasattr(ast, 'Num') and isinstance(node, ast.Num):
            if node.n not in allowed:
                magic_numbers.append(f"Magic number {node.n} at line {getattr(node, 'lineno', 0)}")
    
    return magic_numbers

def _find_duplicated_code(tree, code):
    """Find potentially duplicated code fragments."""
    duplications = []
    statements = []
    
    # Extract statement strings
    for node in ast.walk(tree):
        if isinstance(node, (ast.Expr, ast.Assign, ast.AugAssign)) and hasattr(node, 'lineno'):
            source_segment = ast.get_source_segment(code, node)
            if source_segment:
                stmt = source_segment.strip()
                if len(stmt) > 20:  # Only consider substantive statements
                    statements.append((stmt, node.lineno))
    
    # Find duplicates
    seen = {}
    for stmt, line in statements:
        # Normalize whitespace
        normalized = re.sub(r'\s+', ' ', stmt).strip()
        if normalized in seen and seen[normalized] != line:
            duplications.append(f"Similar code at lines {seen[normalized]} and {line}")
        else:
            seen[normalized] = line
    
    return duplications
    
def _find_missing_docstrings(tree):
    """Find functions and classes missing docstrings."""
    missing_docs = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # Check if function/class has a docstring
            docstring = ast.get_docstring(node)
            if not docstring and not node.name.startswith('_'):
                item_type = "class" if isinstance(node, ast.ClassDef) else "function"
                missing_docs.append(f"{item_type.capitalize()} '{node.name}' at line {node.lineno} is missing a docstring")
    
    return missing_docs

def _find_excessive_line_length(code):
    """Find lines that exceed the recommended limit (79 characters for Python)."""
    long_lines = []
    
    for i, line in enumerate(code.split('\n')):
        if len(line) > 100:  # Using 100 as a more permissive limit than PEP8's 79
            long_lines.append(f"Line {i+1} is {len(line)} characters long (exceeds 100 characters)")
    
    return long_lines

def _find_too_many_arguments(tree):
    """Find functions with too many arguments (more than 5)."""
    too_many_args = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args_count = len(node.args.args)
            if args_count > 5:  # Common recommendation is to have no more than 5 parameters
                too_many_args.append(f"Function '{node.name}' at line {node.lineno} has {args_count} parameters (exceeds 5)")
    
    return too_many_args

def _find_global_variables(tree):
    """Find global variables in the code."""
    globals_found = []
    module_level_vars = {}
    
    # First pass: collect module-level variables
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            # Only consider if the assignment is at module level (no parent function/class)
            is_module_level = True
            
            # Check if it's within a function/class
            for parent in ast.walk(tree):
                if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    for child in ast.walk(parent):
                        if child is node:
                            is_module_level = False
                            break
            
            if is_module_level and not var_name.startswith('_') and var_name.upper() != var_name:
                module_level_vars[var_name] = node.lineno
    
    # Second pass: find global statements inside functions
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Global):
                    for name in subnode.names:
                        globals_found.append(f"Global variable '{name}' used in function '{node.name}' at line {subnode.lineno}")
    
    # Add module-level variables (except constants)
    for name, line in module_level_vars.items():
        globals_found.append(f"Module-level variable '{name}' declared at line {line}")
    
    return globals_found
