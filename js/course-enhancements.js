/* Course Enhancements for Python Data Science Path */

// Copy to Clipboard Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add copy buttons to all code blocks
    const codeBlocks = document.querySelectorAll('pre');
    
    codeBlocks.forEach((block) => {
        // Create copy button
        const button = document.createElement('button');
        button.className = 'copy-btn';
        button.textContent = 'Copy';
        button.style.cssText = `
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
            opacity: 0;
            z-index: 10;
        `;
        
        // Make pre element relative for absolute positioning
        block.style.position = 'relative';
        
        // Show button on hover
        block.addEventListener('mouseenter', () => {
            button.style.opacity = '1';
        });
        
        block.addEventListener('mouseleave', () => {
            if (!button.classList.contains('copied')) {
                button.style.opacity = '0';
            }
        });
        
        // Copy functionality
        button.addEventListener('click', async () => {
            const codeElement = block.querySelector('code');
            const text = codeElement ? codeElement.textContent : block.textContent;
            
            try {
                await navigator.clipboard.writeText(text);
                button.textContent = 'Copied!';
                button.classList.add('copied');
                button.style.background = '#10b981';
                
                setTimeout(() => {
                    button.textContent = 'Copy';
                    button.classList.remove('copied');
                    button.style.background = '#667eea';
                    button.style.opacity = '0';
                }, 2000);
            } catch (err) {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = text;
                textArea.style.position = 'fixed';
                textArea.style.opacity = '0';
                document.body.appendChild(textArea);
                textArea.select();
                
                try {
                    document.execCommand('copy');
                    button.textContent = 'Copied!';
                    button.style.background = '#10b981';
                    
                    setTimeout(() => {
                        button.textContent = 'Copy';
                        button.style.background = '#667eea';
                    }, 2000);
                } catch (err) {
                    button.textContent = 'Failed';
                    setTimeout(() => {
                        button.textContent = 'Copy';
                    }, 2000);
                }
                
                document.body.removeChild(textArea);
            }
        });
        
        block.appendChild(button);
    });
    
    // Calculate reading time
    const content = document.querySelector('main') || document.querySelector('body');
    if (content) {
        const text = content.innerText || content.textContent;
        const wordsPerMinute = 200;
        const words = text.trim().split(/\s+/).length;
        const readingTime = Math.ceil(words / wordsPerMinute);
        
        const readingTimeElement = document.querySelector('.reading-time');
        if (readingTimeElement) {
            readingTimeElement.textContent = `${readingTime} min read`;
        }
    }
    
    // Progress indicator
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            progressBar.style.width = scrolled + '%';
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        // Alt + Left Arrow for previous lesson
        if (e.altKey && e.key === 'ArrowLeft') {
            const prevLink = document.querySelector('.prev-lesson');
            if (prevLink) prevLink.click();
        }
        // Alt + Right Arrow for next lesson
        if (e.altKey && e.key === 'ArrowRight') {
            const nextLink = document.querySelector('.next-lesson');
            if (nextLink) nextLink.click();
        }
        // Alt + Home for course home
        if (e.altKey && e.key === 'Home') {
            const homeLink = document.querySelector('.home-link');
            if (homeLink) homeLink.click();
        }
    });
    
    // Add ARIA labels to interactive elements
    document.querySelectorAll('button').forEach(button => {
        if (!button.getAttribute('aria-label') && button.textContent) {
            button.setAttribute('aria-label', button.textContent.trim());
        }
    });
    
    // Mobile menu toggle (if needed)
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
            const isExpanded = mobileMenu.classList.contains('active');
            mobileMenuToggle.setAttribute('aria-expanded', isExpanded);
        });
    }
    
    // Interactive code examples - syntax highlighting with basic tokenization
    const pythonKeywords = [
        'import', 'from', 'as', 'def', 'class', 'if', 'elif', 'else', 'for', 'while',
        'return', 'yield', 'lambda', 'with', 'try', 'except', 'finally', 'raise',
        'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is', 'pass', 'break',
        'continue', 'global', 'nonlocal', 'del', 'await', 'async', 'assert'
    ];
    
    const pythonBuiltins = [
        'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set',
        'tuple', 'type', 'isinstance', 'enumerate', 'zip', 'map', 'filter',
        'sum', 'min', 'max', 'abs', 'round', 'sorted', 'reversed', 'open'
    ];
    
    // Add line numbers to code blocks
    document.querySelectorAll('pre code').forEach(block => {
        const lines = block.textContent.split('\n');
        if (lines.length > 5) {
            block.parentElement.classList.add('line-numbers');
            
            const lineNumbersDiv = document.createElement('div');
            lineNumbersDiv.className = 'line-numbers-rows';
            lineNumbersDiv.style.cssText = `
                position: absolute;
                pointer-events: none;
                top: 1em;
                font-size: 100%;
                left: 0;
                width: 3em;
                letter-spacing: -1px;
                border-right: 1px solid #e1e4e8;
                user-select: none;
            `;
            
            for (let i = 0; i < lines.length; i++) {
                const lineNumber = document.createElement('span');
                lineNumbersDiv.appendChild(lineNumber);
            }
            
            block.parentElement.style.paddingLeft = '3.8em';
            block.parentElement.appendChild(lineNumbersDiv);
        }
    });
    
    // Add interactive tooltips for complex terms
    const addTooltip = (element, text) => {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = text;
        tooltip.style.cssText = `
            position: absolute;
            background: #333;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
        `;
        
        element.addEventListener('mouseenter', (e) => {
            document.body.appendChild(tooltip);
            const rect = element.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.bottom + 5) + 'px';
            tooltip.style.opacity = '1';
        });
        
        element.addEventListener('mouseleave', () => {
            tooltip.style.opacity = '0';
            setTimeout(() => {
                if (tooltip.parentNode) {
                    tooltip.parentNode.removeChild(tooltip);
                }
            }, 300);
        });
    };
    
    // Track lesson completion
    const lessonPath = window.location.pathname;
    const completedLessons = JSON.parse(localStorage.getItem('completedLessons') || '[]');
    
    if (!completedLessons.includes(lessonPath)) {
        // Mark as completed when user scrolls to bottom
        let hasCompleted = false;
        window.addEventListener('scroll', () => {
            if (!hasCompleted) {
                const scrollPercent = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight;
                if (scrollPercent > 0.9) {
                    hasCompleted = true;
                    completedLessons.push(lessonPath);
                    localStorage.setItem('completedLessons', JSON.stringify(completedLessons));
                    console.log('Lesson marked as completed!');
                }
            }
        });
    }
    
    // Add print-friendly button
    const printButton = document.createElement('button');
    printButton.textContent = '🖨️ Print';
    printButton.className = 'print-button';
    printButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 10px 20px;
        background: white;
        border: 2px solid #667eea;
        color: #667eea;
        border-radius: 25px;
        cursor: pointer;
        font-weight: bold;
        z-index: 999;
        transition: all 0.3s ease;
    `;
    
    printButton.addEventListener('click', () => {
        window.print();
    });
    
    printButton.addEventListener('mouseenter', () => {
        printButton.style.background = '#667eea';
        printButton.style.color = 'white';
    });
    
    printButton.addEventListener('mouseleave', () => {
        printButton.style.background = 'white';
        printButton.style.color = '#667eea';
    });
    
    document.body.appendChild(printButton);
});

// Utility function for formatting numbers with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Utility function for creating interactive plots (placeholder for actual implementation)
function createInteractivePlot(canvasId, plotType, data) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    // Basic plot rendering would go here
    // This is a placeholder for demonstration
    ctx.fillStyle = '#667eea';
    ctx.fillRect(10, 10, 100, 100);
    ctx.fillStyle = '#000';
    ctx.font = '14px Arial';
    ctx.fillText(`${plotType} Plot`, 10, 130);
}