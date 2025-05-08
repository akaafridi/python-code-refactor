import difflib
import html

def generate_diff(original_code, refactored_code):
    """
    Generate a diff between original and refactored code.
    
    Args:
        original_code (str): The original Python code
        refactored_code (str): The refactored Python code
        
    Returns:
        str: HTML representation of the diff with highlighted changes
    """
    # Create a diff
    diff = difflib.ndiff(original_code.splitlines(), refactored_code.splitlines())
    
    # Convert diff to HTML with highlighting
    html_diff = highlight_diff(diff)
    return html_diff

def highlight_diff(diff_lines):
    """
    Convert diff output to HTML with color highlighting.
    
    Args:
        diff_lines: Iterator of diff lines from difflib
        
    Returns:
        str: HTML representation with syntax highlighting
    """
    html_lines = ['<style>',
                  '.diff-container { font-family: monospace; white-space: pre; }',
                  '.diff-added { background-color: #e6ffed; color: #24292e; }',
                  '.diff-removed { background-color: #ffeef0; color: #24292e; }',
                  '.diff-unchanged { color: #24292e; }',
                  '</style>',
                  '<div class="diff-container">']
    
    for line in diff_lines:
        if line.startswith('+ '):
            html_lines.append(f'<div class="diff-added">{html.escape(line[2:])}</div>')
        elif line.startswith('- '):
            html_lines.append(f'<div class="diff-removed">{html.escape(line[2:])}</div>')
        elif line.startswith('? '):
            # Skip the indicator line as it's just for context
            continue
        else:
            # Lines starting with '  ' are unchanged
            html_lines.append(f'<div class="diff-unchanged">{html.escape(line[2:] if line.startswith("  ") else line)}</div>')
    
    html_lines.append('</div>')
    return '\n'.join(html_lines)
