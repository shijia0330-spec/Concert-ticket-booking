"""Automation for EventHub_Login_testcases.md — core flows + session (F / P)."""

from playwright.sync_api import expect


def test_F01_valid_credentials_reach_home_and_show_logout(login_page, course_config):
    """F-01: Valid credentials → leave /login + Logout visible."""
    login_page.open(course_config["base_url"])
    login_page.login(course_config["email"], course_config["password"])

    assert "/login" not in login_page.page.url
    assert login_page.page.get_by_role("button", name="Logout").is_visible()


def test_F02_invalid_credentials_do_not_grant_access(login_page, login_url):
    """F-02: invalid@example.com / WrongPass1 → stay unauthenticated."""
    login_page.open(login_url)
    login_page.submit_credentials("invalid@example.com", "WrongPass1")

    login_page.expect_unauthenticated()
    assert login_page.page.get_by_role("button", name="Logout").count() == 0


def test_P01_logout_available_after_successful_login(login_page, course_config):
    """P-01: After F-01, Logout is visible and enabled."""
    login_page.open(course_config["base_url"])
    login_page.login(course_config["email"], course_config["password"])

    logout = login_page.page.get_by_role("button", name="Logout")
    assert logout.is_visible()
    assert logout.is_enabled()


def test_P02_fresh_session_shows_sign_in_not_logout(login_page, login_url):
    """P-02: Fresh /login shows Sign In, not Logout."""
    login_page.open(login_url)

    assert login_page.page.get_by_role("button", name="Sign In").is_visible()
    assert login_page.page.get_by_role("button", name="Logout").count() == 0


def test_P03_double_click_sign_in_reaches_authenticated_state(login_page, course_config):
    """P-03: Double-click Sign In ends in authenticated session (no crash)."""
    login_page.open(course_config["base_url"])
    login_page.fill_email(course_config["email"])
    login_page.fill_password(course_config["password"])
    login_page.dblclick_sign_in()

    expect(login_page.page.get_by_role("button", name="Logout")).to_be_visible()
    assert login_page.page.get_by_role("button", name="Logout").is_visible()
