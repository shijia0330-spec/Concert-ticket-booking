"""Automation for EventHub_Login_testcases.md — validation (V-01 … V-07)."""

from playwright.sync_api import expect


def test_V01_empty_email_and_password(login_page, login_url):
    """V-01: Empty email + password → no login success."""
    login_page.open(login_url)
    login_page.clear_credentials()
    login_page.click_sign_in()

    login_page.expect_unauthenticated()


def test_V02_email_filled_password_empty(login_page, login_url):
    """V-02: Email filled, password empty → no login success."""
    login_page.open(login_url)
    login_page.fill_email("someone@example.com")
    login_page.fill_password("")
    login_page.click_sign_in()

    login_page.expect_unauthenticated()


def test_V03_password_shorter_than_six_rejected(login_page, login_url):
    """V-03: Password 12345 (5 chars) → login does not succeed."""
    login_page.open(login_url)
    login_page.submit_credentials("someone@example.com", "12345")

    login_page.expect_unauthenticated()


def test_V04_password_exactly_six_wrong_account_fails(login_page, login_url):
    """V-04: invalid@example.com / abcdef → still unauthenticated."""
    login_page.open(login_url)
    login_page.submit_credentials("invalid@example.com", "abcdef")

    login_page.expect_unauthenticated()


def test_V05_malformed_email_rejected(login_page, login_url):
    """V-05: Email not-an-email → login does not succeed."""
    login_page.open(login_url)
    login_page.submit_credentials("not-an-email", "abcdef")

    login_page.expect_unauthenticated()


def test_V06_wrong_credentials_do_not_authenticate(login_page, login_url):
    """V-06: Valid-format email, wrong password → no Logout."""
    login_page.open(login_url)
    login_page.submit_credentials("not-a-user@example.com", "WrongPass123!")

    login_page.expect_unauthenticated()


def test_V07_normal_printable_input_no_crash(login_page, login_url):
    """V-07: letters+digits+symbol input → controlled failure, no crash."""
    login_page.open(login_url)
    login_page.submit_credentials("probe@example.com", "Test1!")

    # Controlled failure (wrong account): page still usable, not a blank crash
    expect(login_page.page.locator("body")).not_to_be_empty()
    login_page.expect_unauthenticated()
