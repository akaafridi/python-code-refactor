import ast
import re
from collections import Counter

def refactor_code(code):
    """
    Refactor the given Python code to improve its quality.
    
    Args:
        code (str): The Python code to refactor
        
    Returns:
        tuple: (refactored_code, list_of_changes)
    """
    try:
        tree = ast.parse(code)
        
        # Track refactoring changes
        changes = []
        
        # Rename poorly named variables
        new_code, var_changes = rename_variables(code, tree)
        if var_changes:
            changes.extend(var_changes)
            code = new_code
            # Re-parse the tree after changes
            tree = ast.parse(code)
        
        # Extract repetitive code into functions
        new_code, extract_changes = extract_functions(code, tree)
        if extract_changes:
            changes.extend(extract_changes)
            code = new_code
            tree = ast.parse(code)
        
        # Simplify complex expressions
        new_code, simplify_changes = simplify_expressions(code, tree)
        if simplify_changes:
            changes.extend(simplify_changes)
            code = new_code
            tree = ast.parse(code)
        
        # Apply DRY principles to remove duplication
        new_code, dry_changes = apply_dry_principles(code, tree)
        if dry_changes:
            changes.extend(dry_changes)
            code = new_code
        
        return code, changes
    except SyntaxError:
        # If there's a syntax error, return the original code
        return code, ["Could not refactor due to syntax errors"]
    except Exception as e:
        # Handle other exceptions
        return code, [f"Refactoring error: {str(e)}"]

def rename_variables(code, tree):
    """Rename poorly named variables to improve clarity."""
    changes = []
    
    # Find variables with poor names
    poor_names = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    # Check for poor names
                    if _is_poor_name(var_name):
                        better_name = _suggest_better_name(var_name, node)
                        poor_names[var_name] = better_name
                        changes.append(f"Renamed variable '{var_name}' to '{better_name}'")
    
    # Perform the renaming
    if poor_names:
        lines = code.split('\n')
        for i, line in enumerate(lines):
            for old_name, new_name in poor_names.items():
                # Use regex to match variable names while avoiding partial matches
                pattern = r'\b' + re.escape(old_name) + r'\b'
                lines[i] = re.sub(pattern, new_name, lines[i])
        
        return '\n'.join(lines), changes
    
    return code, changes

def _is_poor_name(name):
    """Check if a variable name is considered poor."""
    # Skip common loop variables and special variables
    if name in ('i', 'j', 'k', 'x', 'y', 'z') or name.startswith('_'):
        return False
    
    # Single letter variables that aren't common loop variables
    if len(name) == 1 and name not in ('i', 'j', 'k', 'x', 'y', 'z'):
        return True
    
    # Non-descriptive names
    if name in ('temp', 'tmp', 'var', 'foo', 'bar', 'data'):
        return True
    
    # Very short names
    if len(name) <= 2 and not name.startswith('_'):
        return True
    
    return False

def _suggest_better_name(name, node):
    """Suggest a better name for a poorly named variable."""
    # For temp variables
    if name in ('temp', 'tmp'):
        return 'temporary_value'
    
    # For single letter variables
    if len(name) == 1:
        if isinstance(node.value, ast.Num):
            return 'number_value'
        elif isinstance(node.value, ast.Str):
            return 'string_value'
        elif isinstance(node.value, ast.List):
            return 'items_list'
        elif isinstance(node.value, ast.Dict):
            return 'data_map'
        else:
            return 'value'
    
    # For other poor names, just make them more descriptive
    if name == 'var':
        return 'variable'
    if name == 'val':
        return 'value'
    if name == 'arr':
        return 'array'
    if name == 'obj':
        return 'object'
    if name == 'num':
        return 'number'
    if name == 'str':
        return 'string'
    if name == 'dict':
        return 'dictionary'
    if name == 'lst':
        return 'list'
    
    # If we can't suggest a specific better name, add a suffix
    return f"{name}_value"

def extract_functions(code, tree):
    """Extract repetitive code into functions."""
    changes = []
    
    # Find code blocks that could be extracted into functions
    # This is a simplified implementation that focuses on duplicate expressions
    expressions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and not isinstance(node.value, (ast.Str, ast.Constant)):
            expr_code = ast.get_source_segment(code, node)
            if expr_code and len(expr_code.strip()) > 20:  # Only consider substantive expressions
                expressions.append(expr_code.strip())
    
    # Count occurrences of each expression
    expr_counts = Counter(expressions)
    
    # Extract expressions that occur multiple times
    extracted_funcs = []
    for expr, count in expr_counts.items():
        if count > 1 and len(expr.split('\n')) < 5:  # Don't extract very complex expressions
            func_name = f"extracted_function_{len(extracted_funcs) + 1}"
            # Create function definition with proper indentation
            function_lines = ["def " + func_name + "():"]
            for line in expr.split("\n"):
                function_lines.append("    " + line)
            function_lines.append("")
            func_def = "\n".join(function_lines)
            extracted_funcs.append((expr, func_name, func_def))
            changes.append(f"Extracted repeated code into function '{func_name}'")
    
    # Apply the extractions
    if extracted_funcs:
        # Find the insertion point for new functions
        lines = code.split('\n')
        import_end = 0
        
        # Skip past imports
        for i, line in enumerate(lines):
            if re.match(r'^(import|from)\s+', line):
                import_end = i + 1
        
        # Insert the extracted functions after imports
        for _, _, func_def in extracted_funcs:
            lines.insert(import_end, func_def)
            import_end += func_def.count('\n') + 1
        
        # Replace occurrences of the extracted code
        for expr, func_name, _ in extracted_funcs:
            code_str = '\n'.join(lines)
            # Replace exact matches of the expression with function calls
            lines = code_str.replace(expr, f"{func_name}()")
        
        return lines, changes
    
    return code, changes

def simplify_expressions(code, tree):
    """Simplify complex expressions in the code."""
    changes = []
    
    # Find and simplify complex boolean expressions
    for node in ast.walk(tree):
        if isinstance(node, ast.BoolOp) and len(node.values) > 3:
            # Complex boolean expression found, but simplification requires
            # advanced AST manipulation which is beyond the scope of this implementation
            changes.append("Identified complex boolean expression that could be simplified")
    
    # Find and simplify nested loops with simple bodies
    for node in ast.walk(tree):
        if isinstance(node, ast.For) and hasattr(node, 'body'):
            if len(node.body) == 1 and isinstance(node.body[0], ast.For):
                # Nested loop with simple body found
                changes.append("Identified nested loop that could be simplified or refactored")
    
    # This is a simplified implementation that only identifies potential simplifications
    # A full implementation would actually transform the AST and generate new code
    
    return code, changes

def apply_dry_principles(code, tree):
    """Apply DRY (Don't Repeat Yourself) principles to the code."""
    changes = []
    
    # Find duplicate code blocks
    blocks = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Skip function definitions for this analysis
            continue
        
        if isinstance(node, ast.Assign):
            # Look for duplicate assignments
            for target in node.targets:
                if isinstance(target, ast.Name):
                    # Get the right side of the assignment
                    right_side = ast.get_source_segment(code, node.value)
                    if right_side:
                        if right_side in blocks:
                            blocks[right_side].append(target.id)
                        else:
                            blocks[right_side] = [target.id]
    
    # Find duplicate assignments
    duplicate_assigns = {expr: vars for expr, vars in blocks.items() if len(vars) > 1}
    
    # Apply DRY principles where possible
    if duplicate_assigns:
        for expr, vars in duplicate_assigns.items():
            if len(expr.strip()) > 5:  # Only consider substantive expressions
                # This is a simplified implementation that identifies but doesn't transform
                changes.append(f"Identified repeated assignment of '{expr}' to variables: {', '.join(vars)}")
    
    # This is a limited implementation. A full implementation would actually
    # refactor the code to eliminate duplication through variables, functions, etc.
    
    return code, changes
