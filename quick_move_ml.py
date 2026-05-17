#!/usr/bin/env python3
"""
Quick script to move remaining ML files to python_machine_learning
"""
import os
import shutil

source_dir = '\\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\python_datascience'
target_dir = '\\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\python_machine_learning'

# Files to move with their new names
files_to_move = {
    'ml_sklearn_basics.html': 'basics_sklearn.html',
    'ml_linear_logistic_regression.html': 'regression_linear_logistic.html',
    'ml_decision_trees.html': 'trees_decision.html',
    'ml_random_forests.html': 'trees_random_forest.html',
    'ml_gradient_boosting.html': 'trees_gradient_boosting.html',
    'ml_support_vector_machines.html': 'classification_svm.html',
    'ml_naive_bayes.html': 'classification_naive_bayes.html',
    'ml_evaluation_metrics.html': 'evaluation_metrics.html',
    'ml_cross_validation.html': 'evaluation_cross_validation.html',
    'ml_train_test_split.html': 'evaluation_train_test_split.html',
    'ml_model_selection.html': 'evaluation_model_selection.html',
    'ml_feature_engineering.html': 'preprocessing_feature_engineering.html',
    'mlops_intro.html': 'mlops_intro.html',
    'nlp_text_preprocessing.html': 'nlp_text_preprocessing.html',
    'deep_learning_basics.html': 'deep_learning_basics.html',
    'deep_learning_cnn.html': 'deep_learning_cnn.html',
    'deep_learning_rnn.html': 'deep_learning_rnn.html',
    'deep_learning_tensorflow_keras.html': 'deep_learning_tensorflow_keras.html',
    'deep_learning_transfer.html': 'deep_learning_transfer.html',
    'dimensionality_pca.html': 'dimensionality_pca.html',
    'dimensionality_tsne.html': 'dimensionality_tsne.html',
    'dimensionality_umap.html': 'dimensionality_umap.html',
    'dimensionality_lda.html': 'dimensionality_lda.html',
    'dimensionality_feature_selection.html': 'dimensionality_feature_selection.html'
}

moved_count = 0
for old_name, new_name in files_to_move.items():
    source = os.path.join(source_dir, old_name)
    target = os.path.join(target_dir, new_name)
    
    if os.path.exists(source):
        try:
            shutil.move(source, target)
            print(f"✓ Moved {old_name} → {new_name}")
            moved_count += 1
        except Exception as e:
            print(f"✗ Error moving {old_name}: {e}")
    else:
        print(f"⚠ File not found: {old_name}")

print(f"\nTotal files moved: {moved_count}")
