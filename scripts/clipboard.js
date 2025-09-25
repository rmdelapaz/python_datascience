// clipboard.js - Add copy-to-clipboard functionality to all code blocks

document.addEventListener('DOMContentLoaded', function() {
    // Add CSS for copy button
    const style = document.createElement('style');
    style.textContent = `
        .code-example {
            position: relative;
        }
        
        .copy-button {
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 6px 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            opacity: 0.7;
            z-index: 10;
        }
        
        .copy-button:hover {
            opacity: 1;
            background: #5a67d8;
            transform: translateY(-2px);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        }
        
        .copy-button.copied {
            background: #10b981;
        }
        
        .copy-button.copied::after {
            content: ' ✓';
        }
        
        /* For inline code blocks */
        code {
            position: relative;
        }
        
        /* Ensure pre blocks have proper positioning context */
        pre {
            position: relative;
        }
        
        .code-example pre {
            padding-top: 40px; /* Make room for button */
        }
    `;
    document.head.appendChild(style);
    
    // Find all code blocks
    const codeBlocks = document.querySelectorAll('.code-example');
    
    codeBlocks.forEach((block, index) => {
        // Create copy button
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = 'Copy Code';
        button.setAttribute('data-index', index);
        
        // Add click handler
        button.addEventListener('click', function() {
            const codeElement = block.querySelector('code');
            if (codeElement) {
                const codeText = codeElement.textContent || codeElement.innerText;
                
                // Copy to clipboard
                if (navigator.clipboard && window.isSecureContext) {
                    // Modern way (requires HTTPS)
                    navigator.clipboard.writeText(codeText).then(() => {
                        // Show success
                        button.textContent = 'Copied';
                        button.classList.add('copied');
                        
                        // Reset after 2 seconds
                        setTimeout(() => {
                            button.textContent = 'Copy Code';
                            button.classList.remove('copied');
                        }, 2000);
                    }).catch(err => {
                        console.error('Failed to copy: ', err);
                        fallbackCopy(codeText, button);
                    });
                } else {
                    // Fallback for older browsers or non-HTTPS
                    fallbackCopy(codeText, button);
                }
            }
        });
        
        // Add button to code block
        block.style.position = 'relative';
        block.appendChild(button);
    });
    
    // Fallback copy method using textarea
    function fallbackCopy(text, button) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.top = '0';
        textArea.style.left = '-9999px';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        
        textArea.focus();
        textArea.select();
        
        try {
            const successful = document.execCommand('copy');
            if (successful) {
                button.textContent = 'Copied';
                button.classList.add('copied');
                
                setTimeout(() => {
                    button.textContent = 'Copy Code';
                    button.classList.remove('copied');
                }, 2000);
            } else {
                button.textContent = 'Copy failed';
                setTimeout(() => {
                    button.textContent = 'Copy Code';
                }, 2000);
            }
        } catch (err) {
            console.error('Fallback copy failed: ', err);
            button.textContent = 'Copy failed';
            setTimeout(() => {
                button.textContent = 'Copy Code';
            }, 2000);
        }
        
        document.body.removeChild(textArea);
    }
    
    // Also handle inline code elements (optional)
    const inlineCodeElements = document.querySelectorAll('code:not(.code-example code)');
    
    inlineCodeElements.forEach((codeEl) => {
        // Only add copy for substantial inline code (more than 20 characters)
        if (codeEl.textContent.length > 20 && !codeEl.closest('.code-example')) {
            codeEl.style.cursor = 'pointer';
            codeEl.title = 'Click to copy';
            
            codeEl.addEventListener('click', function(e) {
                e.stopPropagation();
                const codeText = codeEl.textContent || codeEl.innerText;
                
                if (navigator.clipboard && window.isSecureContext) {
                    navigator.clipboard.writeText(codeText).then(() => {
                        // Visual feedback
                        const originalBg = codeEl.style.backgroundColor;
                        codeEl.style.backgroundColor = '#10b981';
                        codeEl.style.color = 'white';
                        
                        setTimeout(() => {
                            codeEl.style.backgroundColor = originalBg;
                            codeEl.style.color = '';
                        }, 500);
                    });
                } else {
                    // Use fallback
                    const textArea = document.createElement('textarea');
                    textArea.value = codeText;
                    textArea.style.position = 'fixed';
                    textArea.style.top = '0';
                    textArea.style.left = '-9999px';
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    
                    // Visual feedback
                    const originalBg = codeEl.style.backgroundColor;
                    codeEl.style.backgroundColor = '#10b981';
                    codeEl.style.color = 'white';
                    
                    setTimeout(() => {
                        codeEl.style.backgroundColor = originalBg;
                        codeEl.style.color = '';
                    }, 500);
                }
            });
        }
    });
});
