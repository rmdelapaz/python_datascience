#!/usr/bin/env python3
"""
Update python_datascience to add clipboard functionality and match other courses.
This script:
1. Copies clipboard.js from python_intro
2. Updates all HTML files to include clipboard.js and course-enhancements.js
3. Adds enhanced.css references (file already exists)
4. Adds accessibility features
"""

import os
import re
import sys
import shutil
import platform
from pathlib import Path

def detect_path_format():
    """Detect if we're running on Windows or WSL/Linux"""
    system = platform.system()
    if system == "Windows":
        return "windows"
    else:
        return "wsl"

def get_project_paths():
    """Get the correct paths for both source and destination projects"""
    system_type = detect_path_format()
    
    if system_type == "windows":
        # Windows path format for WSL files
        paths = {
            'datascience': [
                r"\\wsl$\Ubuntu\home\practicalace\projects\python_datascience",
                r"\\wsl.localhost\Ubuntu\home\practicalace\projects\python_datascience",
            ],
            'intro': [
                r"\\wsl$\Ubuntu\home\practicalace\projects\python_intro",
                r"\\wsl.localhost\Ubuntu\home\practicalace\projects\python_intro",
            ]
        }
    else:
        # WSL/Linux path format
        paths = {
            'datascience': [
                "/home/practicalace/projects/python_datascience",
                os.path.expanduser("~/projects/python_datascience"),
            ],
            'intro': [
                "/home/practicalace/projects/python_intro", 
                os.path.expanduser("~/projects/python_intro"),
            ]
        }
    
    # Find which paths exist
    found_paths = {}
    for project, path_list in paths.items():
        for path in path_list:
            if os.path.exists(path):
                found_paths[project] = path
                break
    
    if 'datascience' not in found_paths:
        print("❌ Could not find python_datascience folder!")
        print("Please enter the full path to python_datascience:")
        user_path = input().strip()
        if os.path.exists(user_path):
            found_paths['datascience'] = user_path
        else:
            print(f"Error: Path '{user_path}' does not exist!")
            sys.exit(1)
    
    return found_paths

def copy_clipboard_js(paths):
    """Copy clipboard.js from python_intro to python_datascience"""
    print("\n📂 Setting up clipboard.js...")
    
    # Ensure js directory exists
    js_dir = os.path.join(paths['datascience'], 'js')
    if not os.path.exists(js_dir):
        os.makedirs(js_dir)
        print(f"  ✅ Created js directory")
    
    # Check if clipboard.js already exists
    dest_clipboard = os.path.join(js_dir, 'clipboard.js')
    if os.path.exists(dest_clipboard):
        print(f"  ✓ clipboard.js already exists")
        return True
    
    # Try to copy from python_intro
    if 'intro' in paths:
        source_clipboard = os.path.join(paths['intro'], 'js', 'clipboard.js')
        if os.path.exists(source_clipboard):
            try:
                shutil.copy2(source_clipboard, dest_clipboard)
                print(f"  ✅ Copied clipboard.js from python_intro")
                return True
            except Exception as e:
                print(f"  ❌ Failed to copy clipboard.js: {e}")
        else:
            print(f"  ⚠️  clipboard.js not found in python_intro")
    
    # If we couldn't copy, create it
    print("  📝 Creating clipboard.js...")
    clipboard_content = '''/**
 * Copy to Clipboard functionality for code blocks
 * Adds a copy button to all code blocks and handles the copy action
 */

(function() {
    'use strict';
    
    // Wait for DOM to be fully loaded
    document.addEventListener('DOMContentLoaded', function() {
        
        // Find all code blocks
        const codeBlocks = document.querySelectorAll('pre code');
        
        codeBlocks.forEach(function(codeBlock) {
            // Create wrapper div for positioning
            const wrapper = document.createElement('div');
            wrapper.className = 'code-block-wrapper';
            wrapper.style.position = 'relative';
            
            // Wrap the pre element
            const preElement = codeBlock.parentElement;
            preElement.parentNode.insertBefore(wrapper, preElement);
            wrapper.appendChild(preElement);
            
            // Create copy button
            const copyButton = document.createElement('button');
            copyButton.className = 'copy-button';
            copyButton.textContent = 'Copy';
            copyButton.setAttribute('aria-label', 'Copy code to clipboard');
            
            // Style the button
            copyButton.style.cssText = `
                position: absolute;
                top: 8px;
                right: 8px;
                padding: 6px 12px;
                background-color: #4a5568;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 12px;
                cursor: pointer;
                opacity: 0.8;
                transition: opacity 0.2s, background-color 0.2s;
                z-index: 10;
            `;
            
            // Add hover effect
            copyButton.addEventListener('mouseenter', function() {
                this.style.opacity = '1';
                this.style.backgroundColor = '#2d3748';
            });
            
            copyButton.addEventListener('mouseleave', function() {
                this.style.opacity = '0.8';
                this.style.backgroundColor = '#4a5568';
            });
            
            // Add copy functionality
            copyButton.addEventListener('click', function() {
                const textToCopy = codeBlock.textContent || codeBlock.innerText;
                
                // Modern clipboard API
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(textToCopy).then(function() {
                        // Success feedback
                        showCopyFeedback(copyButton, true);
                    }).catch(function(err) {
                        // Fallback to older method
                        fallbackCopyTextToClipboard(textToCopy, copyButton);
                    });
                } else {
                    // Fallback for older browsers
                    fallbackCopyTextToClipboard(textToCopy, copyButton);
                }
            });
            
            // Add button to wrapper
            wrapper.appendChild(copyButton);
        });
    });
    
    // Fallback copy method for older browsers
    function fallbackCopyTextToClipboard(text, button) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        
        // Avoid scrolling to bottom
        textArea.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 2em;
            height: 2em;
            padding: 0;
            border: none;
            outline: none;
            box-shadow: none;
            background: transparent;
        `;
        
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            const successful = document.execCommand('copy');
            showCopyFeedback(button, successful);
        } catch (err) {
            showCopyFeedback(button, false);
        }
        
        document.body.removeChild(textArea);
    }
    
    // Show feedback when copy is complete
    function showCopyFeedback(button, success) {
        const originalText = button.textContent;
        
        if (success) {
            button.textContent = '✓ Copied!';
            button.style.backgroundColor = '#48bb78';
        } else {
            button.textContent = '✗ Failed';
            button.style.backgroundColor = '#f56565';
        }
        
        // Reset button after 2 seconds
        setTimeout(function() {
            button.textContent = originalText;
            button.style.backgroundColor = '#4a5568';
        }, 2000);
    }
    
    // Add CSS for code blocks if not already present
    const style = document.createElement('style');
    style.textContent = `
        .code-block-wrapper {
            position: relative;
            margin: 1em 0;
        }
        
        .code-block-wrapper pre {
            padding-right: 60px; /* Make room for copy button */
            margin: 0;
        }
        
        /* Ensure code blocks have appropriate styling */
        pre code {
            display: block;
            overflow-x: auto;
            padding: 1em;
            background-color: #f6f8fa;
            border-radius: 6px;
        }
        
        /* Hide button on print */
        @media print {
            .copy-button {
                display: none;
            }
        }
        
        /* Accessibility improvements */
        .copy-button:focus {
            outline: 2px solid #4299e1;
            outline-offset: 2px;
        }
        
        /* Dark mode support if page has dark class */
        .dark pre code {
            background-color: #1a202c;
            color: #e2e8f0;
        }
        
        .dark .copy-button {
            background-color: #2d3748;
        }
        
        .dark .copy-button:hover {
            background-color: #4a5568;
        }
    `;
    document.head.appendChild(style);
    
})();'''
    
    try:
        with open(dest_clipboard, 'w', encoding='utf-8') as f:
            f.write(clipboard_content)
        print(f"  ✅ Created clipboard.js")
        return True
    except Exception as e:
        print(f"  ❌ Failed to create clipboard.js: {e}")
        return False

def update_html_file(filepath):
    """Update a single HTML file to include scripts and enhanced CSS"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Error reading file: {e}"
    
    original_content = content
    changes_made = []
    
    # 1. Add enhanced.css after main.css (if not already present)
    if 'enhanced.css' not in content and 'main.css' in content:
        # Look for the main.css line and add enhanced.css after it
        pattern = r'(<link href="styles/main.css" rel="stylesheet"/>)'
        replacement = r'\1\n    <link href="/styles/enhanced.css" rel="stylesheet"/>'
        new_content = re.sub(pattern, replacement, content, count=1)
        
        if new_content != content:
            content = new_content
            changes_made.append("added enhanced.css")
    
    # 2. Add course-enhancements.js before </head> (if not already present)
    if 'course-enhancements.js' not in content:
        if '</head>' in content:
            pattern = r'(</head>)'
            replacement = r'    <script src="/js/course-enhancements.js" defer></script>\n\1'
            new_content = re.sub(pattern, replacement, content, count=1)
            
            if new_content != content:
                content = new_content
                changes_made.append("added course-enhancements.js")
    
    # 3. Add clipboard.js after course-enhancements or before </head>
    if 'clipboard.js' not in content:
        if 'course-enhancements.js' in content:
            # Add after course-enhancements.js
            pattern = r'(    <script src="/js/course-enhancements.js" defer></script>)'
            replacement = r'\1\n    <script src="/js/clipboard.js" defer></script>'
            new_content = re.sub(pattern, replacement, content, count=1)
        else:
            # Add before </head>
            pattern = r'(</head>)'
            replacement = r'    <script src="/js/clipboard.js" defer></script>\n\1'
            new_content = re.sub(pattern, replacement, content, count=1)
        
        if new_content != content:
            content = new_content
            changes_made.append("added clipboard.js")
    
    # 4. Add skip-to-main link if not present
    if 'skip-to-main' not in content and '<body>' in content:
        pattern = r'(<body>)'
        replacement = r'\1\n    <!-- Skip to main content for accessibility -->\n    <a href="#main-content" class="skip-to-main">Skip to main content</a>'
        new_content = re.sub(pattern, replacement, content, count=1)
        
        if new_content != content:
            content = new_content
            changes_made.append("added skip-to-main link")
    
    # 5. Add progress indicator if not present
    if 'progress-indicator' not in content and 'skip-to-main' in content:
        pattern = r'(    <a href="#main-content" class="skip-to-main">Skip to main content</a>)'
        replacement = r'\1\n    \n    <!-- Progress indicator -->\n    <div class="progress-indicator" role="progressbar" aria-label="Page scroll progress">\n        <div class="progress-bar"></div>\n    </div>'
        new_content = re.sub(pattern, replacement, content, count=1)
        
        if new_content != content:
            content = new_content
            changes_made.append("added progress indicator")
    
    # 6. Add main wrapper if not present
    # Note: Many datascience files already have content structure, so we'll be careful here
    if '<main' not in content and 'breadcrumb' in content:
        # Find where to insert main opening tag (after breadcrumb)
        pattern = r'(</nav>\s*\n)(\s*<h1)'
        replacement = r'\1\n    <main id="main-content">\n\2'
        new_content = re.sub(pattern, replacement, content, count=1)
        
        if new_content != content:
            # Add closing main tag before footer or body close
            if '<footer>' in new_content:
                pattern = r'(\s*<footer>)'
                replacement = r'    </main>\n\1'
            else:
                pattern = r'(</body>)'
                replacement = r'    </main>\n\1'
            
            content = re.sub(pattern, replacement, new_content, count=1)
            changes_made.append("added main wrapper")
    
    # Write the updated content if changes were made
    if changes_made:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made
        except Exception as e:
            return False, f"Error writing file: {e}"
    else:
        return False, "no changes needed"

def process_all_html_files(datascience_path):
    """Process all HTML files in python_datascience"""
    print("\n📝 Updating HTML files...")
    
    # Get all HTML files
    html_files = []
    for filename in os.listdir(datascience_path):
        if filename.endswith('.html'):
            html_files.append(filename)
    
    html_files.sort()
    total_files = len(html_files)
    
    print(f"Found {total_files} HTML files to process")
    print("-" * 60)
    
    # Statistics
    updated_count = 0
    skipped_count = 0
    failed_files = []
    
    # Process each file
    for i, filename in enumerate(html_files, 1):
        filepath = os.path.join(datascience_path, filename)
        progress = f"[{i}/{total_files}]"
        
        success, result = update_html_file(filepath)
        
        if success:
            changes = ", ".join(result)
            print(f"{progress} ✅ {filename}: {changes}")
            updated_count += 1
        elif "no changes needed" in str(result):
            print(f"{progress} ✓  {filename}: already updated")
            skipped_count += 1
        else:
            print(f"{progress} ⚠  {filename}: {result}")
            failed_files.append((filename, result))
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files processed: {total_files}")
    print(f"Files updated: {updated_count}")
    print(f"Files skipped (already updated): {skipped_count}")
    print(f"Files failed: {len(failed_files)}")
    
    if failed_files:
        print("\n⚠ Failed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
    
    return updated_count > 0

def verify_setup(datascience_path):
    """Verify that all required files are in place"""
    print("\n🔍 Verifying setup...")
    
    checks = {
        'index.html': False,
        'js/course-enhancements.js': False,
        'js/clipboard.js': False,
        'styles/main.css': False,
        'styles/enhanced.css': False
    }
    
    for file_path in checks.keys():
        full_path = os.path.join(datascience_path, file_path)
        if os.path.exists(full_path):
            checks[file_path] = True
            print(f"  ✅ {file_path} exists")
        else:
            print(f"  ❌ {file_path} missing")
    
    all_good = all(checks.values())
    
    if all_good:
        print("\n✅ All required files are in place!")
    else:
        print("\n⚠️  Some files are missing. The setup may not be complete.")
    
    # Check sample file for proper structure
    sample_file = os.path.join(datascience_path, 'numpy_arrays_vs_lists.html')
    if os.path.exists(sample_file):
        with open(sample_file, 'r', encoding='utf-8') as f:
            sample_content = f.read()
        
        print("\n📋 Sample file check (numpy_arrays_vs_lists.html):")
        checks = {
            'clipboard.js': 'clipboard.js' in sample_content,
            'course-enhancements.js': 'course-enhancements.js' in sample_content,
            'enhanced.css': 'enhanced.css' in sample_content,
            'skip-to-main': 'skip-to-main' in sample_content,
            'progress-indicator': 'progress-indicator' in sample_content
        }
        
        for feature, present in checks.items():
            if present:
                print(f"  ✅ Has {feature}")
            else:
                print(f"  ❌ Missing {feature}")
    
    return all_good

def main():
    """Main function"""
    
    print("=" * 60)
    print("PYTHON DATA SCIENCE UPDATER")
    print("=" * 60)
    print("\nThis script will update python_datascience to:")
    print("  • Add clipboard functionality to all code blocks")
    print("  • Include course enhancement features")
    print("  • Add accessibility improvements")
    print("  • Match the structure of other courses\n")
    
    # Get project paths
    print("🔍 Detecting project paths...")
    paths = get_project_paths()
    
    print(f"✅ Found python_datascience at: {paths['datascience']}")
    if 'intro' in paths:
        print(f"✅ Found python_intro at: {paths['intro']}")
    
    # Step 1: Copy clipboard.js
    if not copy_clipboard_js(paths):
        print("\n⚠️  Warning: clipboard.js setup had issues")
    
    # Step 2: Update HTML files
    if process_all_html_files(paths['datascience']):
        print("\n✅ HTML files successfully updated!")
    else:
        print("\n✓ No HTML files needed updating.")
    
    # Step 3: Verify setup
    verify_setup(paths['datascience'])
    
    print("\n" + "=" * 60)
    print("✅ PROCESS COMPLETE!")
    print("=" * 60)
    print("\nYour python_datascience project now has:")
    print("  • An organized index.html with all lessons")
    print("  • Copy-to-clipboard functionality on all code blocks")
    print("  • Course enhancement features")
    print("  • Improved accessibility")
    print("  • Consistent structure with other courses")
    print("\n📊 Ready to learn data science with enhanced features! 🚀")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
