# Task Manager - Buggy Version

This is an intentionally buggy web application created for UI/UX testing and debugging evaluation.

## Known Bugs

This application contains the following intentional bugs:

1. **Layout Overlaps:**
   - Navigation menu overlaps with main content
   - Task cards overlap each other due to absolute positioning
   - Footer overlaps with main content

2. **Missing/Non-functional Buttons:**
   - Submit button is hidden (display: none)
   - Logout button is missing from header

3. **Markdown Rendering Issues:**
   - Headers are not properly formatted
   - Bold and italic text not rendered
   - Lists appear as plain text
   - Code blocks lose formatting
   - Links don't become clickable

## How to Run

### Using Python HTTP Server

```bash
python -m http.server 8080
```

Then open http://localhost:8080 in your browser.

### Using Docker

```bash
docker build -t task-manager-buggy .
docker run -p 8080:8080 task-manager-buggy
```

Then open http://localhost:8080 in your browser.

## Running Tests

```bash
pip install -r requirements.txt
playwright install chromium
pytest tests/test_ui.py -v
```
