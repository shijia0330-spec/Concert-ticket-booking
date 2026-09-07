"""Automation for EventHub_Home_testcases.md — access / session (F / P)."""

import re

from playwright.sync_api import expect


def test_F01_anonymous_root_redirects_to_login(home_page, home_url):
    """F-01: Open / without session → /login + Sign In."""
    home_page.page.context.clear_cookies()
    home_page.open(home_url)
    expect(home_page.page).to_have_url(re.compile(r".*/login"), timeout=15000)
    assert "/login" in home_page.page.url
    assert home_page.page.get_by_role("button", name="Sign In").is_visible()


def test_P01_anonymous_cannot_see_auth_home_chrome(home_page, home_url):
    """P-01: Anon on / → no Logout, on login."""
    home_page.page.context.clear_cookies()
    home_page.open(home_url)
    expect(home_page.page).to_have_url(re.compile(r".*/login"), timeout=15000)
    assert "/login" in home_page.page.url
    assert home_page.page.get_by_role("button", name="Logout").count() == 0


def test_F02_auth_home_shows_hero_featured_and_logout(logged_in_home):
    """F-02: After login → home URL, hero, Featured Events, Logout."""
    page = logged_in_home.page
    assert "/login" not in page.url
    logged_in_home.expect_hero()
    expect(page.get_by_role("heading", name="Featured Events")).to_be_visible()
    assert page.get_by_role("button", name="Logout").is_visible()


def test_P02_auth_home_shows_email_and_logout(logged_in_home, course_config):
    """P-02: Authenticated home shows email + Logout."""
    page = logged_in_home.page
    assert page.get_by_text(course_config["email"]).first.is_visible()
    assert page.get_by_role("button", name="Logout").is_visible()
