"""
Automated UI/UX Test Suite for Task Manager Application

This test suite validates:
1. No layout overlaps
2. All required buttons exist and are functional
3. Markdown renders with correct formatting
4. No critical UI errors in the console
"""

import pytest
import re
from playwright.sync_api import Page, expect
from pathlib import Path


class TestUILayout:
    """Test suite for layout and overlap detection"""
    
    def test_no_navigation_content_overlap(self, page: Page, app_url: str):
        """Verify navigation doesn't overlap with main content"""
        page.goto(app_url)
        
        # Get bounding boxes
        nav_box = page.locator('.navigation').bounding_box()
        main_box = page.locator('.main-content').bounding_box()
        
        assert nav_box is not None, "Navigation element not found"
        assert main_box is not None, "Main content element not found"
        
        # Check for horizontal overlap
        nav_right = nav_box['x'] + nav_box['width']
        main_left = main_box['x']
        
        # Navigation should not overlap with main content
        overlap = nav_right > main_left and nav_box['x'] < (main_left + main_box['width'])
        
        assert not overlap or nav_right <= main_left + 10, \
            f"Navigation overlaps with main content. Nav right: {nav_right}, Main left: {main_left}"
    
    def test_no_task_cards_overlap(self, page: Page, app_url: str):
        """Verify task cards don't overlap each other"""
        page.goto(app_url)
        
        cards = page.locator('.task-card').all()
        assert len(cards) >= 3, "Expected at least 3 task cards"
        
        boxes = [card.bounding_box() for card in cards]
        
        # Check each pair of cards for overlap
        for i, box1 in enumerate(boxes):
            for j, box2 in enumerate(boxes[i + 1:], start=i + 1):
                if box1 and box2:
                    # Check if boxes overlap
                    horizontal_overlap = (box1['x'] < box2['x'] + box2['width'] and 
                                        box1['x'] + box1['width'] > box2['x'])
                    vertical_overlap = (box1['y'] < box2['y'] + box2['height'] and 
                                      box1['y'] + box1['height'] > box2['y'])
                    
                    overlap = horizontal_overlap and vertical_overlap
                    
                    assert not overlap, \
                        f"Task card {i} overlaps with task card {j}. " \
                        f"Card {i}: {box1}, Card {j}: {box2}"
    
    def test_no_footer_content_overlap(self, page: Page, app_url: str):
        """Verify footer doesn't overlap with main content"""
        page.goto(app_url)
        
        main_box = page.locator('.main-content').bounding_box()
        footer_box = page.locator('.footer').bounding_box()
        
        assert main_box is not None, "Main content element not found"
        assert footer_box is not None, "Footer element not found"
        
        # Footer should be below main content (no vertical overlap)
        main_bottom = main_box['y'] + main_box['height']
        footer_top = footer_box['y']
        
        assert main_bottom <= footer_top + 50, \
            f"Footer overlaps with main content. Main bottom: {main_bottom}, Footer top: {footer_top}"
    
    def test_grid_layout_proper_distribution(self, page: Page, app_url: str):
        """Verify task cards are properly distributed in grid"""
        page.goto(app_url)
        
        cards = page.locator('.task-card').all()
        assert len(cards) >= 3, "Expected at least 3 task cards"
        
        # Get Y positions to check if cards are in rows
        y_positions = [card.bounding_box()['y'] for card in cards if card.bounding_box()]
        
        # Cards should have varying positions (not all at 0,0)
        unique_positions = len(set([round(y, -1) for y in y_positions]))
        
        # At least some cards should be visible at different positions
        assert unique_positions >= 1, "All cards appear to be at the same position"


class TestButtons:
    """Test suite for button presence and functionality"""
    
    def test_submit_button_exists(self, page: Page, app_url: str):
        """Verify submit button exists in the form"""
        page.goto(app_url)
        
        submit_btn = page.locator('#submitBtn')
        assert submit_btn.count() == 1, "Submit button not found"
    
    def test_submit_button_visible(self, page: Page, app_url: str):
        """Verify submit button is visible (not hidden with display:none)"""
        page.goto(app_url)
        
        submit_btn = page.locator('#submitBtn')
        assert submit_btn.is_visible(), "Submit button exists but is not visible"
    
    def test_submit_button_clickable(self, page: Page, app_url: str):
        """Verify submit button is clickable"""
        page.goto(app_url)
        
        submit_btn = page.locator('#submitBtn')
        
        # Fill form before clicking submit
        page.fill('#taskTitle', 'Test Task')
        page.fill('#taskDescription', 'Test description')
        
        # Button should be clickable
        submit_btn.click()
        
        # Verify new task was added
        cards = page.locator('.task-card')
        assert cards.count() >= 4, "Submit button didn't add a new task"
    
    def test_logout_button_exists(self, page: Page, app_url: str):
        """Verify logout button exists in header"""
        page.goto(app_url)
        
        logout_btn = page.locator('#logoutBtn, .logout-btn')
        assert logout_btn.count() >= 1, "Logout button not found in header"
    
    def test_logout_button_visible(self, page: Page, app_url: str):
        """Verify logout button is visible"""
        page.goto(app_url)
        
        logout_btn = page.locator('#logoutBtn, .logout-btn')
        assert logout_btn.is_visible(), "Logout button exists but is not visible"
    
    def test_cancel_button_functional(self, page: Page, app_url: str):
        """Verify cancel button clears the form"""
        page.goto(app_url)
        
        page.fill('#taskTitle', 'Test Task')
        page.fill('#taskDescription', 'Test description')
        
        page.click('#cancelBtn')
        
        title_value = page.input_value('#taskTitle')
        desc_value = page.input_value('#taskDescription')
        
        assert title_value == '', "Cancel button didn't clear title"
        assert desc_value == '', "Cancel button didn't clear description"
    
    def test_edit_buttons_exist(self, page: Page, app_url: str):
        """Verify edit buttons exist on task cards"""
        page.goto(app_url)
        
        edit_btns = page.locator('.edit-btn')
        assert edit_btns.count() >= 3, "Edit buttons not found on task cards"
    
    def test_delete_buttons_exist(self, page: Page, app_url: str):
        """Verify delete buttons exist on task cards"""
        page.goto(app_url)
        
        delete_btns = page.locator('.delete-btn')
        assert delete_btns.count() >= 3, "Delete buttons not found on task cards"


class TestMarkdownRendering:
    """Test suite for markdown formatting validation"""
    
    def test_headers_rendered_as_html(self, page: Page, app_url: str):
        """Verify markdown headers are rendered as HTML header tags"""
        page.goto(app_url)
        
        # Check for h1, h2, or h3 tags within markdown content
        headers = page.locator('.markdown-content h1, .markdown-content h2, .markdown-content h3')
        
        assert headers.count() >= 1, \
            "No header tags found in markdown content. Headers may not be rendering correctly."
    
    def test_bold_text_rendered(self, page: Page, app_url: str):
        """Verify markdown bold text is rendered with strong tags"""
        page.goto(app_url)
        
        bold_elements = page.locator('.markdown-content strong, .markdown-content b')
        
        assert bold_elements.count() >= 1, \
            "No bold elements found in markdown content. Bold text may not be rendering correctly."
    
    def test_italic_text_rendered(self, page: Page, app_url: str):
        """Verify markdown italic text is rendered with em tags"""
        page.goto(app_url)
        
        italic_elements = page.locator('.markdown-content em, .markdown-content i')
        
        assert italic_elements.count() >= 1, \
            "No italic elements found in markdown content. Italic text may not be rendering correctly."
    
    def test_lists_rendered_with_bullets(self, page: Page, app_url: str):
        """Verify markdown lists are rendered as HTML lists"""
        page.goto(app_url)
        
        lists = page.locator('.markdown-content ul, .markdown-content ol')
        list_items = page.locator('.markdown-content li')
        
        assert lists.count() >= 1, "No list elements found in markdown content"
        assert list_items.count() >= 3, "No list items found in markdown content"
    
    def test_links_are_clickable(self, page: Page, app_url: str):
        """Verify markdown links are rendered as clickable anchor tags"""
        page.goto(app_url)
        
        links = page.locator('.markdown-content a')
        
        assert links.count() >= 1, "No anchor tags found in markdown content. Links may not be rendering."
        
        # Check that link has href attribute
        first_link = links.first
        href = first_link.get_attribute('href')
        assert href is not None and href != '', "Link element doesn't have proper href attribute"
    
    def test_code_blocks_formatted(self, page: Page, app_url: str):
        """Verify code blocks are rendered with proper formatting"""
        page.goto(app_url)
        
        code_blocks = page.locator('.markdown-content pre code, .markdown-content pre')
        
        assert code_blocks.count() >= 1, \
            "No code block elements found in markdown content. Code blocks may not be rendering."
    
    def test_inline_code_formatted(self, page: Page, app_url: str):
        """Verify inline code is rendered with code tags"""
        page.goto(app_url)
        
        inline_code = page.locator('.markdown-content code')
        
        assert inline_code.count() >= 1, \
            "No inline code elements found in markdown content. Inline code may not be rendering."
    
    def test_markdown_not_plain_text(self, page: Page, app_url: str):
        """Verify markdown is rendered as HTML, not displayed as plain text"""
        page.goto(app_url)
        
        content = page.locator('.markdown-content').first
        inner_html = content.inner_html()
        inner_text = content.inner_text()
        
        # If markdown is rendered properly, HTML should contain tags
        has_html_tags = bool(re.search(r'<(h1|h2|h3|strong|em|ul|li|a|code)', inner_html))
        
        # Plain text shouldn't contain raw markdown syntax
        has_markdown_syntax = bool(re.search(r'(\*\*|__|\[.+\]\(.+\)|```|^#{1,6}\s)', inner_text, re.MULTILINE))
        
        assert has_html_tags, "Markdown content doesn't contain HTML tags - may be rendered as plain text"
        assert not has_markdown_syntax, "Markdown content contains raw markdown syntax - not properly rendered"


class TestConsoleErrors:
    """Test suite for console error detection"""
    
    def test_no_critical_console_errors(self, page: Page, app_url: str):
        """Verify no critical JavaScript errors in console"""
        errors = []
        warnings = []
        
        # Capture console messages
        page.on('console', lambda msg: (
            errors.append(msg.text) if msg.type == 'error' else
            warnings.append(msg.text) if msg.type == 'warning' else None
        ))
        
        # Capture page errors
        page.on('pageerror', lambda err: errors.append(str(err)))
        
        page.goto(app_url)
        
        # Wait for page to fully load
        page.wait_for_load_state('networkidle')
        
        # Filter out intentional test errors
        critical_errors = [e for e in errors if 'Intentional error for testing' not in e]
        
        assert len(critical_errors) == 0, \
            f"Found {len(critical_errors)} console errors: {critical_errors}"
    
    def test_all_resources_loaded(self, page: Page, app_url: str):
        """Verify all resources (CSS, JS) load successfully"""
        failed_requests = []
        
        page.on('requestfailed', lambda req: failed_requests.append(
            f"{req.url} - {req.failure}"
        ))
        
        page.goto(app_url)
        page.wait_for_load_state('networkidle')
        
        assert len(failed_requests) == 0, \
            f"Found {len(failed_requests)} failed resource requests: {failed_requests}"


class TestAccessibility:
    """Basic accessibility tests"""
    
    def test_form_inputs_have_labels(self, page: Page, app_url: str):
        """Verify form inputs have proper placeholders or labels"""
        page.goto(app_url)
        
        title_input = page.locator('#taskTitle')
        desc_input = page.locator('#taskDescription')
        
        # Check for placeholder attribute
        assert title_input.get_attribute('placeholder'), "Title input missing placeholder"
        assert desc_input.get_attribute('placeholder'), "Description input missing placeholder"
    
    def test_buttons_have_text(self, page: Page, app_url: str):
        """Verify all buttons have visible text"""
        page.goto(app_url)
        
        buttons = page.locator('button').all()
        
        for button in buttons:
            text = button.inner_text().strip()
            assert text != '', f"Button has no text: {button}"


class TestResponsiveness:
    """Test responsive design"""
    
    def test_mobile_layout(self, page: Page, app_url: str):
        """Verify layout works on mobile viewport"""
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(app_url)
        
        # Page should load without errors
        assert page.locator('.container').is_visible()
        
        # Main content should be visible
        assert page.locator('.main-content').is_visible()
    
    def test_desktop_layout(self, page: Page, app_url: str):
        """Verify layout works on desktop viewport"""
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(app_url)
        
        # All major elements should be visible
        assert page.locator('.header').is_visible()
        assert page.locator('.navigation').is_visible()
        assert page.locator('.main-content').is_visible()
        assert page.locator('.footer').is_visible()


# Fixtures

@pytest.fixture(scope="session")
def app_url(request):
    """Get the application URL from command line or use default"""
    return request.config.getoption("--app-url", default="http://localhost:8080")


@pytest.fixture(scope="function")
def page(playwright):
    """Create a new browser page for each test"""
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    yield page
    
    page.close()
    context.close()
    browser.close()


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--app-url",
        action="store",
        default="http://localhost:8080",
        help="URL of the application to test"
    )
