import os
from pathlib import Path

# Define the base directory
base_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\python_datascience")

# Script tag to add before closing body tag
script_tag = '''    <!-- Copy to Clipboard functionality -->
    <script src="scripts/clipboard.js"></script>
</body>'''

# List of HTML files to update
html_files = [
    "numpy_arrays_vs_lists.html",
    "numpy_vectorized_operations.html",
    "numpy_broadcasting.html",
    "numpy_random_generation.html",
    "numpy_linear_algebra.html",
    "pandas_dataframes_series.html",
    "pandas_data_loading.html",
    "pandas_data_cleaning.html",
    "pandas_merging_joining.html",
    "pandas_groupby_operations.html",
    "matplotlib_line_scatter_bar.html",
    "matplotlib_subplots_composition.html",
    "matplotlib_customizing_plots.html",
    "matplotlib_saving_figures.html"
]

def update_html_file(filepath):
    """Add clipboard.js script to HTML file"""
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if script is already added
        if 'clipboard.js' in content:
            print(f"✓ {filepath.name} - Script already added")
            return False
        
        # Add the script tag before closing body tag
        if '</body>' in content:
            content = content.replace('</body>', script_tag)
            
            # Write the updated content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {filepath.name} - Script added successfully")
            return True
        else:
            print(f"⚠️ {filepath.name} - No </body> tag found")
            return False
            
    except Exception as e:
        print(f"❌ {filepath.name} - Error: {e}")
        return False

# Update all HTML files
print("Updating HTML files with clipboard functionality...")
print("-" * 50)

updated_count = 0
for html_file in html_files:
    filepath = base_dir / html_file
    if filepath.exists():
        if update_html_file(filepath):
            updated_count += 1
    else:
        print(f"❌ {html_file} - File not found")

print("-" * 50)
print(f"Summary: {updated_count} files updated successfully")

# Create a test HTML file to verify the functionality
test_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clipboard Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .code-example {
            background: #f5f5f5;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
            position: relative;
        }
        pre {
            margin: 0;
            overflow-x: auto;
        }
        code {
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <h1>Clipboard Functionality Test</h1>
    <p>Test the copy-to-clipboard functionality with the code blocks below:</p>
    
    <div class="code-example">
        <pre><code># Python Example
import numpy as np

# Create an array
arr = np.array([1, 2, 3, 4, 5])
print(f"Array: {arr}")
print(f"Sum: {arr.sum()}")
print(f"Mean: {arr.mean()}")</code></pre>
    </div>
    
    <div class="code-example">
        <pre><code># Another Example
import pandas as pd

# Create a DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

print(df)</code></pre>
    </div>
    
    <p>Inline code example: <code>np.array([1, 2, 3, 4, 5])</code> (click to copy)</p>
    
    <!-- Copy to Clipboard functionality -->
    <script src="scripts/clipboard.js"></script>
</body>
</html>'''

# Save the test file
test_file_path = base_dir / "test_clipboard.html"
with open(test_file_path, 'w', encoding='utf-8') as f:
    f.write(test_html)

print(f"\n✅ Test file created: test_clipboard.html")
print("Open this file in a browser to test the clipboard functionality!")
