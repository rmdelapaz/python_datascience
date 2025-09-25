import os
from pathlib import Path

# Define the base directory
base_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\python_datascience")

# HTML files to update (excluding the one we already updated)
html_files = [
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

# Script content to add before closing body tag
clipboard_script = '''    
    <!-- Copy to Clipboard functionality -->
    <script src="scripts/clipboard.js"></script>'''

updated_count = 0
already_has = 0
failed = 0

print("🔧 Adding clipboard functionality to HTML files...")
print("=" * 60)

for html_file in html_files:
    filepath = base_dir / html_file
    
    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has clipboard.js
        if 'clipboard.js' in content:
            print(f"✓  {html_file} - Already has clipboard")
            already_has += 1
            continue
        
        # Find </body> and insert script before it
        if '</body>' in content:
            updated_content = content.replace('</body>', f'{clipboard_script}\n</body>')
            
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ {html_file} - Updated successfully")
            updated_count += 1
        else:
            print(f"⚠️  {html_file} - No </body> tag found")
            failed += 1
            
    except Exception as e:
        print(f"❌ {html_file} - Error: {e}")
        failed += 1

print("\n" + "=" * 60)
print("📊 Summary:")
print(f"  ✅ Updated:     {updated_count} files")
print(f"  ✓  Already had: {already_has} files") 
print(f"  ❌ Failed:      {failed} files")
print(f"\n🎉 Clipboard functionality has been added to all HTML files!")
print("   Open any HTML file in a browser to test the copy buttons on code blocks.")
