import streamlit as st
import ast
import os
import tempfile
from pathlib import Path
import io

from utils.code_analyzer import analyze_code
from utils.code_cleaner import clean_code
from utils.code_refactor import refactor_code
from utils.diff_generator import generate_diff, highlight_diff

# Set page configuration
st.set_page_config(
    page_title="Python Code Refactor Tool",
    page_icon="🐍",
    layout="wide",
)

def process_code(code):
    """Process the input code by analyzing, cleaning, and refactoring it."""
    try:
        # Check if the code is valid Python
        ast.parse(code)
        
        # Analyze and clean the code
        analysis_result = analyze_code(code)
        cleaned_code = clean_code(code)
        
        # Refactor the code
        refactored_code, refactor_changes = refactor_code(cleaned_code)
        
        # Generate diff
        diff_html = generate_diff(code, refactored_code)
        
        return {
            "original_code": code,
            "refactored_code": refactored_code,
            "analysis_result": analysis_result,
            "refactor_changes": refactor_changes,
            "diff_html": diff_html,
            "success": True,
            "error_message": None
        }
    except SyntaxError as e:
        return {
            "original_code": code,
            "refactored_code": code,
            "analysis_result": {},
            "refactor_changes": [],
            "diff_html": "",
            "success": False,
            "error_message": f"Syntax Error: {str(e)}"
        }
    except Exception as e:
        return {
            "original_code": code,
            "refactored_code": code,
            "analysis_result": {},
            "refactor_changes": [],
            "diff_html": "",
            "success": False,
            "error_message": f"Error: {str(e)}"
        }

def process_file(uploaded_file):
    """Process an uploaded Python file."""
    content = uploaded_file.getvalue().decode("utf-8")
    result = process_code(content)
    result["filename"] = uploaded_file.name
    return result

def process_directory(uploaded_files):
    """Process multiple uploaded Python files."""
    results = []
    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith('.py'):
            results.append(process_file(uploaded_file))
    return results

def create_download_link(code, filename="refactored_code.py"):
    """Create a download link for the refactored code."""
    buffer = io.StringIO()
    buffer.write(code)
    buffer.seek(0)
    return buffer.getvalue()

# Main app
st.title("🐍 Python Code Refactor Tool")
st.write("""
This tool helps you refactor your Python code by:
- Formatting code according to PEP8 standards
- Removing unused imports and variables
- Simplifying complex expressions
- Renaming variables for better clarity
- Extracting functions for reusable code
- Ensuring DRY (Don't Repeat Yourself) principles
""")

# Create tabs for different input methods
tab1, tab2 = st.tabs(["Code Input", "File Upload"])

with tab1:
    st.header("Enter Your Python Code")
    
    # Sample code for demonstration
    sample_code = '''
import os, sys, math, datetime
from collections import defaultdict, Counter, OrderedDict

def complicated_function(x, y, z):
    result = 0
    for i in range(x):
        for j in range(y):
            for k in range(z):
                result = result + i*j*k
    return result

def another_function(a, b):
    temp = a + b
    temp = temp * 2
    return temp

a = 5
b = 10
c = a + b
d = a + b
unused_var = "This is not used"
    '''
    
    user_code = st.text_area("Python Code", sample_code, height=400, label_visibility="collapsed")
    
    if st.button("Refactor Code", key="refactor_text"):
        if user_code.strip():
            result = process_code(user_code)
            
            if result["success"]:
                st.session_state["result"] = result
            else:
                st.error(result["error_message"])
        else:
            st.warning("Please enter some Python code.")

with tab2:
    st.header("Upload Python File(s)")
    
    uploaded_files = st.file_uploader("Upload .py files", type=["py"], accept_multiple_files=True)
    
    if st.button("Refactor Files", key="refactor_files"):
        if uploaded_files:
            if len(uploaded_files) == 1:
                result = process_file(uploaded_files[0])
                if result["success"]:
                    st.session_state["result"] = result
                else:
                    st.error(f"Error processing {uploaded_files[0].name}: {result['error_message']}")
            else:
                results = process_directory(uploaded_files)
                if results:
                    st.session_state["batch_results"] = results
                    st.success(f"Processed {len(results)} files.")
                else:
                    st.warning("No Python files were found in the upload.")
        else:
            st.warning("Please upload at least one Python file.")

# Display results
if "result" in st.session_state:
    result = st.session_state["result"]
    
    st.header("Refactoring Results")
    
    # Create columns for before/after display
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Code")
        st.code(result["original_code"], language="python")
    
    with col2:
        st.subheader("Refactored Code")
        st.code(result["refactored_code"], language="python")
    
    # Analysis results
    st.subheader("Code Analysis")
    if result["analysis_result"]:
        for category, items in result["analysis_result"].items():
            if items:
                with st.expander(f"{category} ({len(items)})"):
                    for item in items:
                        st.write(f"- {item}")
    else:
        st.write("No issues found in the code.")
    
    # Refactoring changes
    st.subheader("Refactoring Changes")
    if result["refactor_changes"]:
        for change in result["refactor_changes"]:
            st.write(f"- {change}")
    else:
        st.write("No refactoring changes were made.")
    
    # Code metrics dashboard
    st.subheader("Code Metrics")
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    # Calculate metrics
    original_lines = len(result["original_code"].split('\n'))
    refactored_lines = len(result["refactored_code"].split('\n'))
    issues_count = sum(len(items) for items in result["analysis_result"].values())
    changes_count = len(result["refactor_changes"])
    
    # Display metrics
    with metrics_col1:
        st.metric("Original Lines", original_lines)
    with metrics_col2:
        st.metric("Refactored Lines", refactored_lines, delta=refactored_lines-original_lines)
    with metrics_col3:
        st.metric("Issues Found", issues_count)
    with metrics_col4:
        st.metric("Changes Made", changes_count)
    
    # Show diff with highlighted changes
    st.subheader("Code Diff (Changes Highlighted)")
    st.markdown(result["diff_html"], unsafe_allow_html=True)
    
    # Download button for refactored code with improved styling
    filename = result.get("filename", "refactored_code.py")
    download_buffer = create_download_link(result["refactored_code"], filename)
    
    download_col1, download_col2 = st.columns([1, 3])
    with download_col1:
        st.download_button(
            label="Download Refactored Code",
            data=download_buffer,
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )
    with download_col2:
        st.info(f"Download the refactored code as '{filename}'")
    

# Display batch results
if "batch_results" in st.session_state:
    results = st.session_state["batch_results"]
    
    st.header("Batch Processing Results")
    
    for i, result in enumerate(results):
        with st.expander(f"File: {result['filename']}"):
            if result["success"]:
                # Create columns for before/after display
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Original Code")
                    st.code(result["original_code"], language="python")
                
                with col2:
                    st.subheader("Refactored Code")
                    st.code(result["refactored_code"], language="python")
                
                # Refactoring changes
                st.subheader("Refactoring Changes")
                if result["refactor_changes"]:
                    for change in result["refactor_changes"]:
                        st.write(f"- {change}")
                else:
                    st.write("No refactoring changes were made.")
                
                # Download button for this file
                download_buffer = create_download_link(result["refactored_code"], result["filename"])
                st.download_button(
                    label=f"Download Refactored {result['filename']}",
                    data=download_buffer,
                    file_name=result["filename"],
                    mime="text/plain",
                    key=f"download_{i}"
                )
            else:
                st.error(result["error_message"])

# Footer
st.markdown("---")
st.write("Python Code Refactor Tool - Improves your code following best practices and PEP8 standards")
