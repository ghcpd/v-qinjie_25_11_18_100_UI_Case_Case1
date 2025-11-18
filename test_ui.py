import pathlib
import threading
import http.server
import socketserver
import pytest
from playwright.sync_api import Page

ROOT = pathlib.Path(__file__).resolve().parent


@pytest.fixture(scope='session')
def http_server():
    handler = http.server.SimpleHTTPRequestHandler
    handler.directory = str(ROOT)
    server = socketserver.TCPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f'http://127.0.0.1:{server.server_address[1]}'
    server.shutdown()


@pytest.fixture(autouse=True)
def guard_console_errors(page: Page):
    errors = []

    def _on_console(msg):
        if msg.type == 'error':
            errors.append(msg.text)

    page.on('console', _on_console)
    yield
    assert not errors, f'Console errors appeared: {errors}'


def test_layout_has_no_overlap(page: Page, http_server):
    page.goto(f"{http_server}/fixed_app/index.html")
    left = page.locator('.left-panel')
    right = page.locator('.right-panel')
    left_box = left.bounding_box()
    right_box = right.bounding_box()
    assert left_box and right_box
    assert right_box['x'] >= left_box['x'] + left_box['width'] - 1


def test_buttons_render_and_actions(page: Page, http_server):
    page.goto(f"{http_server}/fixed_app/index.html")
    hero_button = page.get_by_role('button', name='Open Guidance')
    messages = []

    def _capture(msg):
        if 'Guidance modal' in msg.text or 'Save action' in msg.text:
            messages.append(msg.text)

    page.on('console', _capture)
    hero_button.click()
    save_button = page.get_by_role('button', name='Save')
    assert save_button.is_enabled()
    save_button.click()
    assert any('Guidance modal' in text for text in messages)
    assert any('Save action' in text for text in messages)


def test_markdown_renders_formatting(page: Page, http_server):
    page.goto(f"{http_server}/fixed_app/index.html")
    input_box = page.locator('#markdown-input')
    render_button = page.get_by_role('button', name='Render Markdown')
    input_box.fill('# Heading\n\nThis is **bold** text for review.')
    render_button.click()
    output_html = page.locator('#markdown-output').inner_html()
    assert '<h1>Heading</h1>' in output_html
    assert '<strong>bold</strong>' in output_html
