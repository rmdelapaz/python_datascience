#!/usr/bin/env python3
"""
Update HTML files to match the proper structure from numpy_arrays_vs_lists.html
"""

import os
import re
from datetime import datetime

# Files that need to be updated (created recently with wrong structure)
files_to_update = [
    'ml_dbscan.html',
    'ml_optics.html',
    'ml_gaussian_mixture.html',
    'ml_hierarchical_clustering.html',
    'ml_anomaly_detection.html',
    'ml_recommendation_systems.html',
    'dimensionality_pca.html',
    'dimensionality_tsne.html',
    'dimensionality_umap.html',
    'dimensionality_lda.html',
    'dimensionality_feature_selection.html'
]

def update_html_structure(filepath):
    """Update HTML file to match proper structure"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title from current file
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else 'Python Data Science'
    
    # Extract main content from current file
    # Look for content within <h1> to </body>
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    h1_content = h1_match.group(1) if h1_match else ''
    
    # Extract all content after h1 and before </body>
    body_match = re.search(r'</h1>(.*?)</body>', content, re.DOTALL)
    main_content = body_match.group(1) if body_match else ''
    
    # Determine navigation based on filename
    nav_prev = ''
    nav_next = ''
    
    if 'ml_dbscan' in filepath:
        nav_prev = 'ml_kmeans_applications.html'
        nav_next = 'ml_optics.html'
    elif 'ml_optics' in filepath:
        nav_prev = 'ml_dbscan.html'
        nav_next = 'ml_gaussian_mixture.html'
    elif 'ml_gaussian_mixture' in filepath:
        nav_prev = 'ml_optics.html'
        nav_next = 'ml_hierarchical_clustering.html'
    elif 'ml_hierarchical_clustering' in filepath:
        nav_prev = 'ml_gaussian_mixture.html'
        nav_next = 'ml_anomaly_detection.html'
    elif 'ml_anomaly_detection' in filepath:
        nav_prev = 'ml_hierarchical_clustering.html'
        nav_next = 'ml_recommendation_systems.html'
    elif 'ml_recommendation_systems' in filepath:
        nav_prev = 'ml_anomaly_detection.html'
        nav_next = 'dimensionality_pca.html'
    elif 'dimensionality_pca' in filepath:
        nav_prev = 'ml_recommendation_systems.html'
        nav_next = 'dimensionality_tsne.html'
    elif 'dimensionality_tsne' in filepath:
        nav_prev = 'dimensionality_pca.html'
        nav_next = 'dimensionality_umap.html'
    elif 'dimensionality_umap' in filepath:
        nav_prev = 'dimensionality_tsne.html'
        nav_next = 'dimensionality_lda.html'
    elif 'dimensionality_lda' in filepath:
        nav_prev = 'dimensionality_umap.html'
        nav_next = 'dimensionality_feature_selection.html'
    elif 'dimensionality_feature_selection' in filepath:
        nav_prev = 'dimensionality_lda.html'
        nav_next = 'deep_learning_basics.html'
    
    # New HTML structure based on reference
    new_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>{title}</title>
    <link href="styles/main.css" rel="stylesheet"/>
    <link href="/favicon.png" rel="icon" type="image/png"/>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    <style>
        .breadcrumb {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 2rem;
            font-size: 0.9rem;
        }}
        
        .breadcrumb a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .breadcrumb a:hover {{
            text-decoration: underline;
        }}
        
        .navigation-links {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 2rem 0;
            margin-top: 3rem;
            border-top: 2px solid #e0e0e0;
        }}
        
        .navigation-links a {{
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            transition: all 0.3s ease;
        }}
        
        .navigation-links a:hover {{
            background: #f0f0f0;
        }}
        
        .nav-prev, .nav-next {{
            flex: 1;
        }}
        
        .nav-next {{
            text-align: right;
        }}
        
        .nav-home {{
            text-align: center;
        }}
        
        .comment-block {{
            background: #f0f4f8;
            border-left: 4px solid #667eea;
            padding: 1.5rem;
            margin: 2rem 0;
            border-radius: 0 5px 5px 0;
        }}
        
        .summary-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin: 2rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .summary-box h3 {{
            margin-top: 0;
            font-size: 1.5rem;
        }}
        
        .summary-box ul {{
            margin-bottom: 0;
        }}
        
        .summary-box li {{
            margin: 0.5rem 0;
        }}
    </style>
</head>
<body>
    <nav class="breadcrumb">
        <a href="index.html">Home</a> &gt; 
        <a href="index.html#machine-learning">Machine Learning</a> &gt;
        <span>{title.replace(' - Python Data Science', '')}</span>
    </nav>

    <h1>{h1_content}</h1>
    
    {main_content}
    
    <footer>
        <div class="navigation-links">
            <a class="nav-prev" href="{nav_prev}">← Previous</a>
            <a class="nav-home" href="index.html">🏠 Course Home</a>
            <a class="nav-next" href="{nav_next}">Next →</a>
        </div>
    </footer>
    
    <!-- Copy to Clipboard functionality -->
    <script src="scripts/clipboard.js"></script>
</body>
</html>'''
    
    return new_html

def main():
    base_path = '/home/practicalace/projects/python_datascience/'
    
    for filename in files_to_update:
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            print(f"Updating {filename}...")
            try:
                new_content = update_html_structure(filepath)
                
                # Backup original
                backup_path = filepath + '.backup'
                with open(filepath, 'r', encoding='utf-8') as f:
                    original = f.read()
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original)
                
                # Write updated content
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"  ✓ Updated {filename}")
            except Exception as e:
                print(f"  ✗ Error updating {filename}: {e}")
        else:
            print(f"  ⚠ File not found: {filename}")
    
    print("\nUpdate complete!")

if __name__ == "__main__":
    main()
