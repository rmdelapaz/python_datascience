#!/usr/bin/env python3
"""
Move ML files from python_datascience to python_machine_learning
with appropriate renaming and content updates
"""

import os
import shutil
import re

# File mappings
file_mappings = {
    'deep_learning_basics.html': 'deep_learning_basics.html',
    'deep_learning_cnn.html': 'deep_learning_cnn.html',
    'deep_learning_rnn.html': 'deep_learning_rnn.html',
    'deep_learning_tensorflow_keras.html': 'deep_learning_tensorflow_keras.html',
    'deep_learning_transfer.html': 'deep_learning_transfer.html',
    'dimensionality_feature_selection.html': 'dimensionality_feature_selection.html',
    'dimensionality_lda.html': 'dimensionality_lda.html',
    'dimensionality_pca.html': 'dimensionality_pca.html',
    'dimensionality_tsne.html': 'dimensionality_tsne.html',
    'dimensionality_umap.html': 'dimensionality_umap.html',
    'ml_anomaly_detection.html': 'applications_anomaly_detection.html',
    'ml_cross_validation.html': 'evaluation_cross_validation.html',
    'ml_dbscan.html': 'clustering_dbscan.html',
    'ml_decision_trees.html': 'trees_decision.html',
    'ml_evaluation_metrics.html': 'evaluation_metrics.html',
    'ml_feature_engineering.html': 'preprocessing_feature_engineering.html',
    'ml_gaussian_mixture.html': 'clustering_gaussian_mixture.html',
    'ml_gradient_boosting.html': 'trees_gradient_boosting.html',
    'ml_hierarchical_clustering.html': 'clustering_hierarchical.html',
    'ml_kmeans_applications.html': 'clustering_kmeans_applications.html',
    'ml_kmeans_clustering.html': 'clustering_kmeans.html',
    'ml_kmeans_optimization.html': 'clustering_kmeans_optimization.html',
    'ml_linear_logistic_regression.html': 'regression_linear_logistic.html',
    'ml_model_selection.html': 'evaluation_model_selection.html',
    'ml_naive_bayes.html': 'classification_naive_bayes.html',
    'ml_optics.html': 'clustering_optics.html',
    'ml_random_forests.html': 'trees_random_forest.html',
    'ml_recommendation_systems.html': 'applications_recommendation_systems.html',
    'ml_sklearn_basics.html': 'basics_sklearn.html',
    'ml_support_vector_machines.html': 'classification_svm.html',
    'ml_train_test_split.html': 'evaluation_train_test_split.html',
    'mlops_intro.html': 'mlops_intro.html',
    'nlp_text_preprocessing.html': 'nlp_text_preprocessing.html'
}

source_dir = '/home/practicalace/projects/python_datascience'
target_dir = '/home/practicalace/projects/python_machine_learning'

def update_content(content, old_filename, new_filename):
    """Update content with new references"""
    
    # Update resource references to point to python_intro site
    content = re.sub(
        r'href="styles/style\.css"',
        'href="https://rays-python-intro.netlify.app/styles/style.css"',
        content
    )
    content = re.sub(
        r'href="styles/main\.css"',
        'href="https://rays-python-intro.netlify.app/styles/main.css"',
        content
    )
    content = re.sub(
        r'src="scripts/clipboard\.js"',
        'src="https://rays-python-intro.netlify.app/scripts/clipboard.js"',
        content
    )
    content = re.sub(
        r'href="favicon\.png"',
        'href="https://rays-python-intro.netlify.app/favicon.png"',
        content
    )
    
    # Update navigation to python_intro
    content = re.sub(
        r'href="index\.html"[^>]*>.*?Python Data Science',
        'href="https://rays-python-intro.netlify.app/">Python Courses',
        content
    )
    
    # Update internal ML file references
    for old, new in file_mappings.items():
        if old != new:
            content = content.replace(f'href="{old}"', f'href="{new}"')
            content = content.replace(f'"{old}"', f'"{new}"')
    
    # Add link back to main Python site in navigation
    if '<nav class="nav-container">' in content:
        # Update existing nav
        content = re.sub(
            r'<a href="[^"]*" class="nav-logo">.*?</a>',
            '<a href="https://rays-python-intro.netlify.app/" class="nav-logo">Python Courses</a>',
            content
        )
    
    return content

def move_files():
    """Move and update all ML files"""
    
    moved_count = 0
    errors = []
    
    for old_name, new_name in file_mappings.items():
        source_path = os.path.join(source_dir, old_name)
        target_path = os.path.join(target_dir, new_name)
        
        try:
            if os.path.exists(source_path):
                # Read content
                with open(source_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update content
                updated_content = update_content(content, old_name, new_name)
                
                # Write to new location
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"✓ Moved {old_name} → {new_name}")
                moved_count += 1
                
                # Delete original file
                os.remove(source_path)
                
            else:
                print(f"⚠ File not found: {old_name}")
                
        except Exception as e:
            errors.append(f"Error moving {old_name}: {e}")
            print(f"✗ Error moving {old_name}: {e}")
    
    print(f"\n{'='*60}")
    print(f"Summary: Moved {moved_count} files")
    
    if errors:
        print(f"\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")
    
    return moved_count, errors

if __name__ == "__main__":
    print("Moving ML files to python_machine_learning...")
    print("="*60)
    
    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    moved, errors = move_files()
    
    if not errors:
        print("\n✅ All files moved successfully!")
    else:
        print(f"\n⚠ Completed with {len(errors)} errors")
