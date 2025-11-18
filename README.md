# UI/UX Bug Detection and Fix Project

This project contains a web application with intentional UI/UX bugs, their fixes, and an automated test suite to verify the fixes.

## Project Structure

```
.
├── buggy/              # Web app with intentional UI/UX bugs
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── package.json
├── fixed/              # Corrected version with all bugs fixed
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── package.json
├── test_ui.py          # Pytest test suite
├── conftest.py         # Pytest configuration
├── requirements.txt    # Python dependencies
├── BUG_IDENTIFICATION.md  # Detailed bug analysis
├── EVALUATION_REPORT.md    # Test results and evaluation
└── README.md           # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js and npm (for running the web server)
- A modern web browser

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

3. **Install Node.js dependencies (optional, for running the server):**
   ```bash
   cd buggy
   npm install
   
   cd ../fixed
   npm install
   ```

## Running the Application

### Option 1: Using http-server (Node.js)

**Run the buggy version:**
```bash
cd buggy
npm start
# Or: npx http-server -p 8080
```

**Run the fixed version:**
```bash
cd fixed
npm start
# Or: npx http-server -p 8080
```

### Option 2: Using Python's HTTP Server

**Run the buggy version:**
```bash
cd buggy
python -m http.server 8080
```

**Run the fixed version:**
```bash
cd fixed
python -m http.server 8080
```

The application will be available at `http://localhost:8080`

## How to Run Tests

### Running Tests Against Buggy Version

1. Start the buggy application server:
   ```bash
   cd buggy
   python -m http.server 8080
   ```

2. In another terminal, run the tests:
   ```bash
   pytest test_ui.py -v
   ```

   Or with environment variable:
   ```bash
   TEST_VERSION=buggy PORT=8080 pytest test_ui.py -v
   ```

### Running Tests Against Fixed Version

1. Start the fixed application server:
   ```bash
   cd fixed
   python -m http.server 8080
   ```

2. In another terminal, run the tests:
   ```bash
   pytest test_ui.py -v
   ```

### Running Specific Tests

Run a specific test:
```bash
pytest test_ui.py::TestUIBugs::test_no_layout_overlaps -v
```

Run tests with detailed output:
```bash
pytest test_ui.py -v -s
```

Run tests with browser visible (non-headless):
Edit `conftest.py` and set `"headless": False`

### Test Coverage

The test suite includes:

1. **test_no_layout_overlaps** - Verifies no elements overlap
2. **test_navigation_buttons_exist_and_functional** - Checks navigation buttons work
3. **test_action_buttons_exist_and_visible** - Verifies all action buttons are visible
4. **test_action_buttons_functional** - Tests button functionality
5. **test_markdown_rendering** - Validates markdown parsing and rendering
6. **test_no_console_errors** - Checks for JavaScript errors
7. **test_markdown_output_styling** - Verifies markdown styling is correct

## Bugs Identified

See `BUG_IDENTIFICATION.md` for a detailed list of all bugs found and how they were fixed.

## Evaluation Report

See `EVALUATION_REPORT.md` for test results and evaluation of the bug detection and fixing process.

## Notes

- The tests use Playwright for browser automation
- Tests run in headless mode by default (can be changed in `conftest.py`)
- Make sure the web server is running before executing tests
- Tests assume the application runs on `http://localhost:8080` by default

