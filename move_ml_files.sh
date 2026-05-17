#!/bin/bash

# Move ML files from python_datascience to python_machine_learning
# with appropriate renaming

SOURCE_DIR="/home/practicalace/projects/python_datascience"
TARGET_DIR="/home/practicalace/projects/python_machine_learning"

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Function to update content in files
update_file_content() {
    local file="$1"
    local new_name="$2"
    
    # Update CSS and JS references to point to python_intro site
    sed -i 's|href="styles/style.css"|href="https://rays-python-intro.netlify.app/styles/style.css"|g' "$file"
    sed -i 's|href="styles/main.css"|href="https://rays-python-intro.netlify.app/styles/main.css"|g' "$file"
    sed -i 's|src="scripts/clipboard.js"|src="https://rays-python-intro.netlify.app/scripts/clipboard.js"|g' "$file"
    sed -i 's|href="favicon.png"|href="https://rays-python-intro.netlify.app/favicon.png"|g' "$file"
    
    # Update navigation to python_intro
    sed -i 's|href="index.html"[^>]*>.*Python Data Science|href="https://rays-python-intro.netlify.app/">Python Courses|g' "$file"
    
    # Update internal ML file references
    sed -i 's|href="ml_dbscan.html"|href="clustering_dbscan.html"|g' "$file"
    sed -i 's|href="ml_optics.html"|href="clustering_optics.html"|g' "$file"
    sed -i 's|href="ml_gaussian_mixture.html"|href="clustering_gaussian_mixture.html"|g' "$file"
    sed -i 's|href="ml_hierarchical_clustering.html"|href="clustering_hierarchical.html"|g' "$file"
    sed -i 's|href="ml_kmeans_clustering.html"|href="clustering_kmeans.html"|g' "$file"
    sed -i 's|href="ml_kmeans_optimization.html"|href="clustering_kmeans_optimization.html"|g' "$file"
    sed -i 's|href="ml_kmeans_applications.html"|href="clustering_kmeans_applications.html"|g' "$file"
    sed -i 's|href="ml_anomaly_detection.html"|href="applications_anomaly_detection.html"|g' "$file"
    sed -i 's|href="ml_recommendation_systems.html"|href="applications_recommendation_systems.html"|g' "$file"
    sed -i 's|href="ml_sklearn_basics.html"|href="basics_sklearn.html"|g' "$file"
    sed -i 's|href="ml_linear_logistic_regression.html"|href="regression_linear_logistic.html"|g' "$file"
    sed -i 's|href="ml_decision_trees.html"|href="trees_decision.html"|g' "$file"
    sed -i 's|href="ml_random_forests.html"|href="trees_random_forest.html"|g' "$file"
    sed -i 's|href="ml_gradient_boosting.html"|href="trees_gradient_boosting.html"|g' "$file"
    sed -i 's|href="ml_support_vector_machines.html"|href="classification_svm.html"|g' "$file"
    sed -i 's|href="ml_naive_bayes.html"|href="classification_naive_bayes.html"|g' "$file"
    sed -i 's|href="ml_evaluation_metrics.html"|href="evaluation_metrics.html"|g' "$file"
    sed -i 's|href="ml_cross_validation.html"|href="evaluation_cross_validation.html"|g' "$file"
    sed -i 's|href="ml_train_test_split.html"|href="evaluation_train_test_split.html"|g' "$file"
    sed -i 's|href="ml_model_selection.html"|href="evaluation_model_selection.html"|g' "$file"
    sed -i 's|href="ml_feature_engineering.html"|href="preprocessing_feature_engineering.html"|g' "$file"
}

# Move and rename files
echo "Moving ML files to python_machine_learning..."
echo "============================================================"

# ML files to move with their new names
declare -A file_mappings=(
    ["ml_dbscan.html"]="clustering_dbscan.html"
    ["ml_optics.html"]="clustering_optics.html"
    ["ml_gaussian_mixture.html"]="clustering_gaussian_mixture.html"
    ["ml_hierarchical_clustering.html"]="clustering_hierarchical.html"
    ["ml_kmeans_clustering.html"]="clustering_kmeans.html"
    ["ml_kmeans_optimization.html"]="clustering_kmeans_optimization.html"
    ["ml_kmeans_applications.html"]="clustering_kmeans_applications.html"
    ["ml_anomaly_detection.html"]="applications_anomaly_detection.html"
    ["ml_recommendation_systems.html"]="applications_recommendation_systems.html"
    ["ml_sklearn_basics.html"]="basics_sklearn.html"
    ["ml_linear_logistic_regression.html"]="regression_linear_logistic.html"
    ["ml_decision_trees.html"]="trees_decision.html"
    ["ml_random_forests.html"]="trees_random_forest.html"
    ["ml_gradient_boosting.html"]="trees_gradient_boosting.html"
    ["ml_support_vector_machines.html"]="classification_svm.html"
    ["ml_naive_bayes.html"]="classification_naive_bayes.html"
    ["ml_evaluation_metrics.html"]="evaluation_metrics.html"
    ["ml_cross_validation.html"]="evaluation_cross_validation.html"
    ["ml_train_test_split.html"]="evaluation_train_test_split.html"
    ["ml_model_selection.html"]="evaluation_model_selection.html"
    ["ml_feature_engineering.html"]="preprocessing_feature_engineering.html"
    ["mlops_intro.html"]="mlops_intro.html"
    ["nlp_text_preprocessing.html"]="nlp_text_preprocessing.html"
)

# Deep learning files (keep names)
deep_learning_files=(
    "deep_learning_basics.html"
    "deep_learning_cnn.html"
    "deep_learning_rnn.html"
    "deep_learning_tensorflow_keras.html"
    "deep_learning_transfer.html"
)

# Dimensionality reduction files (keep names)
dimensionality_files=(
    "dimensionality_pca.html"
    "dimensionality_tsne.html"
    "dimensionality_umap.html"
    "dimensionality_lda.html"
    "dimensionality_feature_selection.html"
)

# Move ML files with renaming
for old_name in "${!file_mappings[@]}"; do
    new_name="${file_mappings[$old_name]}"
    source_file="$SOURCE_DIR/$old_name"
    target_file="$TARGET_DIR/$new_name"
    
    if [ -f "$source_file" ]; then
        cp "$source_file" "$target_file"
        update_file_content "$target_file" "$new_name"
        rm "$source_file"
        echo "✓ Moved $old_name → $new_name"
    else
        echo "⚠ File not found: $old_name"
    fi
done

# Move deep learning files (no renaming)
for file in "${deep_learning_files[@]}"; do
    source_file="$SOURCE_DIR/$file"
    target_file="$TARGET_DIR/$file"
    
    if [ -f "$source_file" ]; then
        cp "$source_file" "$target_file"
        update_file_content "$target_file" "$file"
        rm "$source_file"
        echo "✓ Moved $file"
    else
        echo "⚠ File not found: $file"
    fi
done

# Move dimensionality files (no renaming)
for file in "${dimensionality_files[@]}"; do
    source_file="$SOURCE_DIR/$file"
    target_file="$TARGET_DIR/$file"
    
    if [ -f "$source_file" ]; then
        cp "$source_file" "$target_file"
        update_file_content "$target_file" "$file"
        rm "$source_file"
        echo "✓ Moved $file"
    else
        echo "⚠ File not found: $file"
    fi
done

echo "============================================================"
echo "Move complete! Files have been moved to $TARGET_DIR"
echo ""
echo "Next step: Add copy-to-clipboard functionality to python_intro"
