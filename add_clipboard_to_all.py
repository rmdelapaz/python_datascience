#!/usr/bin/env python3
"""
Script to add clipboard.js functionality to all HTML files in the project.
This will add a script tag before the closing </body> tag in each HTML file.
"""

import os
from pathlib import Path
import sys

# Define the base directory
base_dir = Path(__file__).parent

# Script tag to add before closing body tag
CLIPBOARD_SCRIPT = '''    
    <!-- Copy to Clipboard functionality -->
    <script src="scripts/clipboard.js"></script>'''

def update_html_file(filepath):
    """Add clipboard.js script to HTML file if not already present."""
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if script is already added
        if 'clipboard.js' in content:
            return 'already_has'
        
        # Check if this is an HTML file with a body tag
        if '</body>' not in content:
            return 'no_body'
        
        # Add the script tag before closing body tag
        updated_content = content.replace('</body>', f'{CLIPBOARD_SCRIPT}\n</body>')
        
        # Write the updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return 'updated'
            
    except Exception as e:
        print(f"  Error processing {filepath.name}: {e}")
        return 'error'

def main():
    """Main function to process all HTML files."""
    print("🔧 Adding Clipboard Functionality to HTML Files")
    print("=" * 60)
    
    # Find all HTML files in the directory
    html_files = list(base_dir.glob("*.html"))
    
    if not html_files:
        print("❌ No HTML files found in the directory!")
        return 1
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    # Statistics
    stats = {
        'updated': 0,
        'already_has': 0,
        'no_body': 0,
        'error': 0
    }
    
    # Process each file
    for filepath in sorted(html_files):
        result = update_html_file(filepath)
        stats[result] += 1
        
        # Print status with appropriate emoji
        if result == 'updated':
            print(f"  ✅ {filepath.name} - Script added successfully")
        elif result == 'already_has':
            print(f"  ✓  {filepath.name} - Script already present")
        elif result == 'no_body':
            print(f"  ⚠️  {filepath.name} - No </body> tag found (skipped)")
        else:
            print(f"  ❌ {filepath.name} - Error occurred")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"  ✅ Updated:        {stats['updated']} files")
    print(f"  ✓  Already had:    {stats['already_has']} files")
    print(f"  ⚠️  No body tag:    {stats['no_body']} files")
    print(f"  ❌ Errors:         {stats['error']} files")
    
    # Final status
    if stats['updated'] > 0:
        print(f"\n🎉 Successfully added clipboard functionality to {stats['updated']} files!")
    elif stats['already_has'] == len(html_files):
        print("\n✅ All files already have clipboard functionality!")
    else:
        print("\n⚠️  No files were updated.")
    
    # Create a test file if it doesn't exist
    test_file = base_dir / "test_clipboard.html"
    if not test_file.exists():
        create_test_file(test_file)
        print(f"\n📝 Created test file: test_clipboard.html")
        print("   Open this file in a browser to test the clipboard functionality!")
    
    return 0

def create_test_file(filepath):
    """Create a test HTML file to verify clipboard functionality."""
    test_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clipboard Functionality Test</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #667eea;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            color: #666;
            margin-bottom: 2rem;
        }
        .code-example {
            background: #f5f7fa;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1.5rem 0;
            position: relative;
            border-left: 4px solid #667eea;
        }
        pre {
            margin: 0;
            overflow-x: auto;
        }
        code {
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
            line-height: 1.5;
        }
        .inline-code {
            background: #f5f7fa;
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
            font-family: 'Courier New', Courier, monospace;
            color: #e83e8c;
        }
        .test-section {
            margin: 2rem 0;
        }
        .test-section h2 {
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 0.5rem;
        }
        .feature-list {
            list-style: none;
            padding: 0;
        }
        .feature-list li {
            padding: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
        }
        .feature-list li:before {
            content: "✅";
            position: absolute;
            left: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 Clipboard Functionality Test</h1>
        <p class="subtitle">Test the copy-to-clipboard feature with the code blocks below</p>
        
        <div class="test-section">
            <h2>Python Examples</h2>
            
            <div class="code-example">
                <pre><code># NumPy Array Operations
import numpy as np

# Create arrays
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([10, 20, 30, 40, 50])

# Vectorized operations
result = arr1 * arr2 + 100
print(f"Result: {result}")
print(f"Mean: {result.mean():.2f}")
print(f"Standard deviation: {result.std():.2f}")</code></pre>
            </div>
            
            <div class="code-example">
                <pre><code># Pandas DataFrame Creation
import pandas as pd
import numpy as np

# Create sample data
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'Age': [25, 30, 35, 28],
    'Score': [92.5, 87.3, 94.1, 89.7],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}

# Create DataFrame
df = pd.DataFrame(data)

# Display statistics
print(df.describe())
print(f"\\nAverage age: {df['Age'].mean():.1f}")
print(f"Top scorer: {df.loc[df['Score'].idxmax(), 'Name']}")</code></pre>
            </div>
        </div>
        
        <div class="test-section">
            <h2>Data Visualization Example</h2>
            
            <div class="code-example">
                <pre><code># Matplotlib Visualization
import matplotlib.pyplot as plt
import numpy as np

# Generate data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * np.cos(x)

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Sine wave
axes[0, 0].plot(x, y1, 'b-', linewidth=2, label='sin(x)')
axes[0, 0].set_title('Sine Function')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].legend()

# Plot 2: Cosine wave
axes[0, 1].plot(x, y2, 'r-', linewidth=2, label='cos(x)')
axes[0, 1].set_title('Cosine Function')
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].legend()

# Plot 3: Combined
axes[1, 0].plot(x, y3, 'g-', linewidth=2, label='sin(x)·cos(x)')
axes[1, 0].set_title('Product Function')
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].legend()

# Plot 4: All together
axes[1, 1].plot(x, y1, 'b-', alpha=0.7, label='sin(x)')
axes[1, 1].plot(x, y2, 'r-', alpha=0.7, label='cos(x)')
axes[1, 1].plot(x, y3, 'g-', alpha=0.7, label='product')
axes[1, 1].set_title('All Functions')
axes[1, 1].grid(True, alpha=0.3)
axes[1, 1].legend()

plt.tight_layout()
plt.show()</code></pre>
            </div>
        </div>
        
        <div class="test-section">
            <h2>Inline Code Examples</h2>
            <p>
                You can also copy inline code snippets. Try clicking on these longer code examples:
            </p>
            <ul>
                <li>Array creation: <code class="inline-code">np.array([1, 2, 3, 4, 5])</code></li>
                <li>DataFrame filtering: <code class="inline-code">df[df['Score'] > 90].sort_values('Age')</code></li>
                <li>List comprehension: <code class="inline-code">[x**2 for x in range(10) if x % 2 == 0]</code></li>
            </ul>
        </div>
        
        <div class="test-section">
            <h2>✨ Features</h2>
            <ul class="feature-list">
                <li>Click the "Copy Code" button on any code block</li>
                <li>Button changes to "Copied!" with visual feedback</li>
                <li>Works with both modern clipboard API and fallback methods</li>
                <li>Inline code snippets are clickable (if > 20 characters)</li>
                <li>Automatic syntax preservation</li>
                <li>Mobile-friendly touch targets</li>
            </ul>
        </div>
    </div>
    
    <!-- Copy to Clipboard functionality -->
    <script src="scripts/clipboard.js"></script>
</body>
</html>'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(test_html)

if __name__ == "__main__":
    sys.exit(main())
