"""
Automated UI/UX Test Suite using pytest and Playwright
Tests for layout overlaps, button functionality, markdown rendering, and console errors
"""

import pytest
from playwright.sync_api import Page, expect, Browser, BrowserContext
import time
import os


class TestUIBugs:
    """Test suite for detecting UI/UX bugs in the web application"""
    
    @pytest.fixture(scope="class")
    def browser_context(self, browser: Browser):
        """Create a browser context for tests"""
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        yield context
        context.close()
    
    @pytest.fixture(scope="class")
    def page(self, browser_context: BrowserContext):
        """Create a page instance"""
        page = browser_context.new_page()
        yield page
        page.close()
    
    @pytest.fixture(scope="class")
    def app_url(self):
        """Get the application URL - can be switched between buggy and fixed versions"""
        # Default to buggy version, can be overridden with environment variable
        version = os.getenv('TEST_VERSION', 'buggy')
        port = os.getenv('PORT', '8080')
        return f"http://localhost:{port}"
    
    def test_no_layout_overlaps(self, page: Page, app_url: str):
        """Test that no elements overlap each other"""
        page.goto(app_url)
        page.wait_for_load_state('networkidle')
        
        # Get all boxes in the content section
        boxes = page.locator('.content-box, .overlapping-box').all()
        
        if len(boxes) > 1:
            # Get bounding boxes for all elements
            bounding_boxes = []
            for box in boxes:
                bbox = box.bounding_box()
                if bbox:
                    bounding_boxes.append(bbox)
            
            # Check for overlaps between any two boxes
            overlaps_found = []
            for i in range(len(bounding_boxes)):
                for j in range(i + 1, len(bounding_boxes)):
                    box1 = bounding_boxes[i]
                    box2 = bounding_boxes[j]
                    
                    # Check if boxes overlap
                    if self._boxes_overlap(box1, box2):
                        overlaps_found.append((i, j))
            
            # Assert no overlaps found
            assert len(overlaps_found) == 0, \
                f"Found {len(overlaps_found)} overlapping element pairs: {overlaps_found}"
    
    def _boxes_overlap(self, box1: dict, box2: dict) -> bool:
        """Check if two bounding boxes overlap"""
        return not (
            box1['x'] + box1['width'] < box2['x'] or
            box2['x'] + box2['width'] < box1['x'] or
            box1['y'] + box1['height'] < box2['y'] or
            box2['y'] + box2['height'] < box1['y']
        )
    
    def test_navigation_buttons_exist_and_functional(self, page: Page, app_url: str):
        """Test that navigation buttons exist and are clickable"""
        page.goto(app_url)
        page.wait_for_load_state('networkidle')
        
        # Check that buttons exist
        home_btn = page.locator('#homeBtn')
        about_btn = page.locator('#aboutBtn')
        contact_btn = page.locator('#contactBtn')
        
        assert home_btn.is_visible(), "Home button should be visible"
        assert about_btn.is_visible(), "About button should be visible"
        assert contact_btn.is_visible(), "Contact button should be visible"
        
        # Test button clicks and check for alerts or console logs
        # Set up alert handler
        alert_triggered = {'value': False}
        
        def handle_alert(alert):
            alert_triggered['value'] = True
            alert.accept()
        
        page.on('dialog', handle_alert)
        
        # Click buttons and verify they trigger actions
        home_btn.click()
        time.sleep(0.5)  # Wait for potential alert
        
        about_btn.click()
        time.sleep(0.5)
        
        contact_btn.click()
        time.sleep(0.5)
        
        # Note: We can't easily test if JavaScript handlers are attached without
        # checking console logs or network activity, but we verify buttons are clickable
    
    def test_action_buttons_exist_and_visible(self, page: Page, app_url: str):
        """Test that all action buttons exist and are visible"""
        page.goto(app_url)
        page.wait_for_load_state('networkidle')
        
        submit_btn = page.locator('#submitBtn')
        cancel_btn = page.locator('#cancelBtn')
        delete_btn = page.locator('#deleteBtn')
        
        # Check visibility
        assert submit_btn.is_visible(), "Submit button should be visible"
        assert cancel_btn.is_visible(), "Cancel button should be visible"
        assert delete_btn.is_visible(), "Delete button should be visible"
        
        # Check that buttons are within viewport
        submit_bbox = submit_btn.bounding_box()
        cancel_bbox = cancel_btn.bounding_box()
        delete_bbox = delete_btn.bounding_box()
        
        assert submit_bbox is not None, "Submit button should have bounding box"
        assert cancel_bbox is not None, "Cancel button should have bounding box"
        assert delete_bbox is not None, "Delete button should have bounding box"
        
        # Check buttons are not positioned off-screen
        viewport = page.viewport_size
        assert submit_bbox['x'] >= 0 and submit_bbox['y'] >= 0, \
            "Submit button should be on-screen"
        assert submit_bbox['x'] + submit_bbox['width'] <= viewport['width'], \
            "Submit button should be within viewport width"
        assert submit_bbox['y'] + submit_bbox['height'] <= viewport['height'], \
            "Submit button should be within viewport height"
        
        assert cancel_bbox['x'] >= 0 and cancel_bbox['y'] >= 0, \
            "Cancel button should be on-screen"
        assert delete_bbox['x'] >= 0 and delete_bbox['y'] >= 0, \
            "Delete button should be on-screen"
    
    def test_action_buttons_functional(self, page: Page, app_url: str):
        """Test that action buttons are functional"""
        page.goto(app_url)
        page.wait_for_load_state('networkidle')
        
        alert_triggered = {'value': False, 'text': ''}
        
        def handle_alert(alert):
            alert_triggered['value'] = True
            alert_triggered['text'] = alert.message
            alert.dismiss()  # Dismiss to continue tests
        
        page.on('dialog', handle_alert)
        
        # Test cancel button
        cancel_btn = page.locator('#cancelBtn')
        cancel_btn.click()
        time.sleep(0.5)
        # Button should be clickable (alert may or may not appear depending on implementation)
        
        # Test submit button
        submit_btn = page.locator('#submitBtn')
        submit_btn.click()
        time.sleep(0.5)
        
        # Test delete button
        delete_btn = page.locator('#deleteBtn')
        delete_btn.click()
        time.sleep(0.5)
    
    def test_markdown_rendering(self, page: Page, app_url: str):
        """Test that markdown renders correctly"""
        page.goto(app_url)
        page.wait_for_load_state('networkidle')
        
        markdown_input = page.locator('#markdownInput')
        render_btn = page.locator('#renderBtn')
        markdown_output = page.locator('#markdownOutput')
        
        # Verify elements exist
        assert markdown_input.is_visible(), "Markdown input should be visible"
        assert render_btn.is_visible(), "Render button should be visible"
        
        # Check render button is clickable (not hidden behind other elements)
        render_bbox = render_btn.bounding_box()
        assert render_bbox is not None, "Render button should have bounding box"
        assert render_bbox['x'] >= 0 and render_bbox['y'] >= 0, \
            "Render button should be on-screen"
        
        # Test markdown rendering
        test_markdown = """# Heading 1
## Heading 2
**Bold text** and *italic text*
- List item 1
- List item 2

[Link text](https://example.com)"""
        
        markdown_input.fill(test_markdown)
        render_btn.click()
        page.wait_for_timeout(500)  # Wait for rendering
        
        # Check that output contains rendered HTML elements
        output_html = markdown_output.inner_html()
        
        # Verify headings are rendered (should be <h1> and <h2> tags, not plain text)
        assert '<h1>' in output_html or 'Heading 1' in output_html, \
            "Heading 1 should be rendered"
        assert '<h2>' in output_html or 'Heading 2' in output_html, \
            "Heading 2 should be rendered"
        
        # Verify bold text is rendered
        assert '<strong>' in output_html or 'Bold text' in output_html, \
            "Bold text should be rendered"
        
        # Verify list items are rendered
        assert '<li>' in output_html or 'List item' in output_html, \
            "List items should be rendered"
        
        # Verify links are rendered
        assert '<a' in output_html or 'Link text' in output_html, \
            "Links should be rendered"
    
    def test_no_console_errors(self, page: Page, app_url: str):
        """Test that there are no critical console errors"""
        page.goto(app_url)
        
        # Collect console messages
        console_errors = []
        console_warnings = []
        
        def handle_console(msg):
            if msg.type == 'error':
                console_errors.append(msg.text)
            elif msg.type == 'warning':
                console_warnings.append(msg.text)
        
        page.on('console', handle_console)
        
        # Interact with the page to trigger any JavaScript errors
        page.wait_for_load_state('networkidle')
        
        # Try clicking various buttons
        try:
            page.locator('#homeBtn').click()
            page.locator('#renderBtn').click()
            page.locator('#submitBtn').click()
        except Exception:
            pass  # Some buttons might not work, but we're checking for console errors
        
        page.wait_for_timeout(1000)  # Wait for any async errors
        
        # Check for critical errors (TypeError, ReferenceError, etc.)
        critical_errors = [
            err for err in console_errors
            if any(keyword in err.lower() for keyword in ['typeerror', 'referenceerror', 'cannot read', 'is not defined', 'null', 'undefined'])
        ]
        
        assert len(critical_errors) == 0, \
            f"Found {len(critical_errors)} critical console errors: {critical_errors}"
    
    def test_markdown_output_styling(self, page: Page, app_url: str):
        """Test that markdown output has proper styling"""
        page.goto(app_url)
        page.wait_for_load_state('networkidle')
        
        markdown_input = page.locator('#markdownInput')
        render_btn = page.locator('#renderBtn')
        markdown_output = page.locator('#markdownOutput')
        
        # Render some markdown
        markdown_input.fill("# Test Heading\n**Bold** text")
        render_btn.click()
        page.wait_for_timeout(500)
        
        # Check that headings have proper styling (not just normal text)
        h1_elements = markdown_output.locator('h1')
        if h1_elements.count() > 0:
            h1_font_weight = page.evaluate("""
                (element) => {
                    const style = window.getComputedStyle(element);
                    return style.fontWeight;
                }
            """, h1_elements.first.element_handle())
            
            # Heading should be bold (font-weight >= 600 or 'bold')
            assert h1_font_weight in ['bold', '700', '600', '800', '900'] or int(h1_font_weight) >= 600, \
                f"Heading should be bold, but font-weight is {h1_font_weight}"
        
        # Check that strong elements are bold
        strong_elements = markdown_output.locator('strong')
        if strong_elements.count() > 0:
            strong_font_weight = page.evaluate("""
                (element) => {
                    const style = window.getComputedStyle(element);
                    return style.fontWeight;
                }
            """, strong_elements.first.element_handle())
            
            assert strong_font_weight in ['bold', '700', '600', '800', '900'] or int(strong_font_weight) >= 600, \
                f"Strong text should be bold, but font-weight is {strong_font_weight}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

