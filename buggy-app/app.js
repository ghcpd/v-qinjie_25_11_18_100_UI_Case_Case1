// Buggy Markdown Renderer
class MarkdownRenderer {
    // BUG: Incorrect markdown parsing - doesn't handle headers, lists, or formatting properly
    static render(markdown) {
        if (!markdown) return '';
        
        // BUG: Wrong regex patterns and incomplete implementation
        let html = markdown;
        
        // Headers - BUG: Wrong replacement pattern
        html = html.replace(/^# (.+)$/gm, '$1');  // Should wrap in <h1> tags
        html = html.replace(/^## (.+)$/gm, '$1'); // Should wrap in <h2> tags
        
        // Bold - BUG: Doesn't wrap in <strong> tags
        html = html.replace(/\*\*(.+?)\*\*/g, '$1');
        
        // Italic - BUG: Doesn't wrap in <em> tags
        html = html.replace(/\*(.+?)\*/g, '$1');
        
        // Lists - BUG: Completely broken, just removes the markers
        html = html.replace(/^- (.+)$/gm, '$1');
        html = html.replace(/^\* (.+)$/gm, '$1');
        
        // Links - BUG: Wrong pattern, doesn't create anchor tags
        html = html.replace(/\[(.+?)\]\((.+?)\)/g, '$1');
        
        // Code blocks - BUG: Doesn't preserve formatting
        html = html.replace(/```(.+?)```/gs, '$1');
        
        // Inline code - BUG: Just removes backticks
        html = html.replace(/`(.+?)`/g, '$1');
        
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

    // BUG: Render markdown incorrectly
    const contents = document.querySelectorAll('.markdown-content');
    contents.forEach((content, index) => {
        if (taskContents[index]) {
            // BUG: Sets as plain text instead of HTML
            content.textContent = MarkdownRenderer.render(taskContents[index]);
        }
    });
}

function setupEventListeners() {
    const taskForm = document.getElementById('taskForm');
    const cancelBtn = document.getElementById('cancelBtn');
    
    // BUG: Submit button is hidden, so this won't work as expected
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
        <h3>${title}</h3>
        <div class="task-content">
            <p class="markdown-content">${MarkdownRenderer.render(description)}</p>
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

// BUG: Console error intentionally left in
console.log('App initialized');
// This will cause an error because undefinedVariable doesn't exist
try {
    undefinedVariable.someMethod();
} catch (e) {
    console.error('Intentional error for testing:', e);
}
