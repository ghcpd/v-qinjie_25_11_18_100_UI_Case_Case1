// Buggy JavaScript with intentional issues

document.addEventListener('DOMContentLoaded', function() {
    // BUG: Navigation buttons don't have event listeners
    // The buttons exist but don't do anything
    const homeBtn = document.getElementById('homeBtn');
    const aboutBtn = document.getElementById('aboutBtn');
    const contactBtn = document.getElementById('contactBtn');
    
    // Missing event listeners - buttons are non-functional
    
    // Markdown renderer - BUGGY implementation
    const markdownInput = document.getElementById('markdownInput');
    const renderBtn = document.getElementById('renderBtn');
    const markdownOutput = document.getElementById('markdownOutput');
    
    // BUG: Render button might not work due to z-index issues
    renderBtn.addEventListener('click', function() {
        const markdown = markdownInput.value;
        // BUG: Incorrect markdown parsing - just displays raw text
        markdownOutput.textContent = markdown;
        // Should parse markdown but doesn't
    });
    
    // Action buttons
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const deleteBtn = document.getElementById('deleteBtn');
    
    // BUG: Submit button is hidden, so this won't work
    if (submitBtn) {
        submitBtn.addEventListener('click', function() {
            alert('Submit clicked!');
        });
    }
    
    // Cancel button works
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            alert('Cancel clicked!');
        });
    }
    
    // BUG: Delete button is positioned off-screen, so this won't work
    if (deleteBtn) {
        deleteBtn.addEventListener('click', function() {
            alert('Delete clicked!');
        });
    }
    
    // BUG: Console error - trying to access non-existent element
    const nonExistentElement = document.getElementById('nonExistent');
    nonExistentElement.addEventListener('click', function() {
        console.log('This will cause an error');
    });
});

