"""
Pytest configuration and fixtures for Playwright tests
"""

import pytest
from playwright.sync_api import Browser, BrowserType


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch arguments"""
    return {
        **browser_type_launch_args,
        "headless": True,  # Set to False to see browser during tests
    }


@pytest.fixture(scope="session")
def browser(browser_type: BrowserType):
    """Launch browser instance"""
    browser = browser_type.launch()
    yield browser
    browser.close()

