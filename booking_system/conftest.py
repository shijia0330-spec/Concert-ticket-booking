import os
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import pytest
from dotenv import load_dotenv

from pages.bookings_page import BookingsPage
from pages.event_page import EventPage
from pages.home_page import HomePage
from pages.login_page import LoginPage

# .env stays at the project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _origin_from_login(login_url: str) -> str:
    parsed = urlparse(login_url)
    return urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture
def login_url():
    """EventHub login URL (named to avoid clash with pytest-base-url)."""
    return os.getenv("BASE_URL", "https://eventhub.rahulshettyacademy.com/login")


@pytest.fixture
def home_url(login_url):
    return os.getenv("HOME_URL") or (_origin_from_login(login_url) + "/")


@pytest.fixture
def course_config(login_url):
    email = os.getenv("COURSE_EMAIL", "")
    password = os.getenv("COURSE_PASSWORD", "")
    if "example.com" in email or not email or not password:
        pytest.skip("Copy .env.example to .env and put your EventHub email/password there.")
    return {
        "base_url": login_url,
        "email": email,
        "password": password,
    }


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def home_page(page):
    return HomePage(page)


@pytest.fixture
def event_page(page):
    return EventPage(page)


@pytest.fixture
def bookings_page(page):
    return BookingsPage(page)


@pytest.fixture
def site_origin(home_url):
    return home_url.rstrip("/")


@pytest.fixture
def logged_in_home(login_page, home_page, course_config, home_url):
    """Login then ensure authenticated home is ready."""
    login_page.open(course_config["base_url"])
    login_page.login(course_config["email"], course_config["password"])
    if "/login" in home_page.page.url:
        home_page.open(home_url)
    home_page.expect_home()
    return home_page


@pytest.fixture
def cleared_bookings(logged_in_home, bookings_page, site_origin):
    """Login + clear My Bookings so event seats are available again."""
    bookings_page.open(site_origin)
    bookings_page.clear_all_bookings()
    return logged_in_home
