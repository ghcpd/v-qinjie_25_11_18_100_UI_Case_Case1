# Test Suite for Task Manager UI/UX

This directory contains automated tests for validating the Task Manager application's UI/UX.

## Test Coverage

### Layout Tests (`TestUILayout`)
- ✅ No navigation/content overlap
- ✅ No task card overlapping
- ✅ No footer/content overlap
- ✅ Proper grid distribution

### Button Tests (`TestButtons`)
- ✅ Submit button exists and is visible
- ✅ Submit button is functional
- ✅ Logout button exists and is visible
- ✅ Cancel button clears form
- ✅ Edit/Delete buttons present on cards

### Markdown Rendering Tests (`TestMarkdownRendering`)
- ✅ Headers rendered as HTML tags
- ✅ Bold text rendered with `<strong>`
- ✅ Italic text rendered with `<em>`
- ✅ Lists rendered with bullets
- ✅ Links are clickable
- ✅ Code blocks formatted
- ✅ Inline code formatted
- ✅ No raw markdown syntax in output

### Console Error Tests (`TestConsoleErrors`)
- ✅ No critical JavaScript errors
- ✅ All resources load successfully

### Accessibility Tests (`TestAccessibility`)
- ✅ Form inputs have labels/placeholders
- ✅ Buttons have descriptive text

### Responsiveness Tests (`TestResponsiveness`)
- ✅ Mobile layout works
- ✅ Desktop layout works

## Running Tests

### Prerequisites

```bash
pip install -r requirements.txt
playwright install chromium
```

### Start the Application

In one terminal:
```bash
cd buggy-app  # or fixed-app
python -m http.server 8080
```

### Run All Tests

In another terminal:
```bash
pytest tests/test_ui.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_ui.py::TestMarkdownRendering -v
```

### Run Specific Test

```bash
pytest tests/test_ui.py::TestButtons::test_submit_button_visible -v
```

### Test Against Custom URL

```bash
pytest tests/test_ui.py --app-url=http://localhost:3000 -v
```

### Generate HTML Report

```bash
pip install pytest-html
pytest tests/test_ui.py --html=report.html --self-contained-html
```

## Expected Results

### Buggy App
When running tests against `buggy-app`, expect **multiple failures**:
- Layout overlap tests will fail
- Submit button visibility test will fail
- Logout button existence test will fail
- Markdown rendering tests will fail

### Fixed App
When running tests against `fixed-app`, expect **all tests to pass** ✅

## Test Output Example

```
tests/test_ui.py::TestUILayout::test_no_navigation_content_overlap PASSED
tests/test_ui.py::TestUILayout::test_no_task_cards_overlap PASSED
tests/test_ui.py::TestUILayout::test_no_footer_content_overlap PASSED
tests/test_ui.py::TestButtons::test_submit_button_visible PASSED
tests/test_ui.py::TestButtons::test_logout_button_exists PASSED
tests/test_ui.py::TestMarkdownRendering::test_headers_rendered_as_html PASSED
tests/test_ui.py::TestMarkdownRendering::test_bold_text_rendered PASSED
tests/test_ui.py::TestMarkdownRendering::test_links_are_clickable PASSED
...

===================== 25 passed in 15.2s =====================
```
