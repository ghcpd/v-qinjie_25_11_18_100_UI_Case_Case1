// FIXED: Proper Markdown Renderer
class MarkdownRenderer {
    static render(markdown) {
        if (!markdown) return '';
        
        let html = markdown;
        
        // Escape HTML to prevent XSS (basic implementation)
        html = html.replace(/</g, '&lt;').replace(/>/g, '&gt;');
        
        // FIXED: Code blocks (must be done before inline code)
        html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
        
        // FIXED: Inline code
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // FIXED: Headers
        html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
        
        // FIXED: Bold (must be done before italic)
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        
        // FIXED: Italic
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
        
        // FIXED: Links
        html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
        
        // FIXED: Lists - basic implementation
        // Convert unordered lists
        html = html.replace(/^[*-] (.+)$/gm, '<li>$1</li>');
        
        // Wrap consecutive <li> tags in <ul>
        html = html.replace(/(<li>.*<\/li>\n?)+/g, function(match) {
            return '<ul>' + match + '</ul>';
        });
        
        // FIXED: Line breaks
        html = html.replace(/\n\n/g, '<br><br>');
        
        return html;
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeTasks();
    setupEventListeners();
});

function initializeTasks() {
    // Sample markdown content for tasks
    const taskContents = [
        `# Documentation Tasks
        
**Priority: High**

- Write API documentation
- Update README.md
- Create user guide

Visit [our docs](https://example.com) for more info.`,
        
        `## Code Review Checklist

Review the following:
* Check for *security issues*
* Verify **test coverage**
* Validate \`code style\`

\`\`\`javascript
function example() {
    return true;
}
\`\`\``,
        
        `### Dependency Updates

Update these packages:
- **React** to v18.2.0
- *Redux* to latest
- Testing libraries

Use \`npm update\` to proceed.`
    ];

    // FIXED: Render markdown as HTML
    const contents = document.querySelectorAll('.markdown-content');
    contents.forEach((content, index) => {
        if (taskContents[index]) {
            // FIXED: Use innerHTML instead of textContent
            content.innerHTML = MarkdownRenderer.render(taskContents[index]);
        }
    });
}

function setupEventListeners() {
    const taskForm = document.getElementById('taskForm');
    const cancelBtn = document.getElementById('cancelBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    
    // FIXED: Submit button now works
    if (taskForm) {
        taskForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addNewTask();
        });
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            clearForm();
        });
    }
    
    // FIXED: Added logout functionality
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to logout?')) {
                alert('Logout functionality would redirect to login page');
                // In a real app: window.location.href = '/logout';
            }
        });
    }
    
    // Setup edit and delete buttons
    setupTaskButtons();
}

function setupTaskButtons() {
    const editBtns = document.querySelectorAll('.edit-btn');
    const deleteBtns = document.querySelectorAll('.delete-btn');
    
    editBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const card = this.closest('.task-card');
            editTask(card);
        });
    });
    
    deleteBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const card = this.closest('.task-card');
            deleteTask(card);
        });
    });
}

function addNewTask() {
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;
    
    if (!title) {
        alert('Please enter a task title');
        return;
    }
    
    // Create new task card
    const taskGrid = document.querySelector('.task-grid');
    const newCard = document.createElement('div');
    newCard.className = 'task-card';
    newCard.innerHTML = `
        <h3>${escapeHtml(title)}</h3>
        <div class="task-content">
            <div class="markdown-content">${MarkdownRenderer.render(description)}</div>
        </div>
        <div class="task-actions">
            <button class="edit-btn">Edit</button>
            <button class="delete-btn">Delete</button>
        </div>
    `;
    
    taskGrid.appendChild(newCard);
    clearForm();
    setupTaskButtons();
}

function clearForm() {
    document.getElementById('taskTitle').value = '';
    document.getElementById('taskDescription').value = '';
}

function editTask(card) {
    const title = card.querySelector('h3').textContent;
    const content = card.querySelector('.markdown-content').textContent;
    
    document.getElementById('taskTitle').value = title;
    document.getElementById('taskDescription').value = content;
    
    // Remove the card (will be re-added on submit)
    card.remove();
}

function deleteTask(card) {
    if (confirm('Are you sure you want to delete this task?')) {
        card.remove();
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// FIXED: Removed intentional console error
console.log('App initialized successfully');
