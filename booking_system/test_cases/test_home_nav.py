"""Automation for EventHub_Home_testcases.md — nav / featured list (L / D)."""

import re

from playwright.sync_api import expect


def test_L01_nav_home_stays_on_home(logged_in_home):
    """L-01: Click Home → still on / with Featured Events."""
    logged_in_home.click_nav("Home")
    expect(logged_in_home.page).to_have_url(re.compile(r"https://eventhub\.rahulshettyacademy\.com/?$"))
    expect(logged_in_home.page.get_by_role("heading", name="Featured Events")).to_be_visible()


def test_L02_nav_events_opens_events(logged_in_home):
    """L-02: Nav Events → /events."""
    logged_in_home.click_nav("Events")
    expect(logged_in_home.page).to_have_url(re.compile(r".*/events"))
    assert "/events" in logged_in_home.page.url


def test_L03_nav_my_bookings_opens_bookings(logged_in_home):
    """L-03: Nav My Bookings → /bookings."""
    logged_in_home.click_nav("My Bookings")
    expect(logged_in_home.page).to_have_url(re.compile(r".*/bookings"))
    assert "/bookings" in logged_in_home.page.url


def test_L04_api_docs_href_points_to_swagger(logged_in_home):
    """L-04: API Docs href is Swagger docs URL (avoid flaky external nav)."""
    link = logged_in_home.page.get_by_role("link", name="API Docs").first
    expect(link).to_be_visible()
    href = link.get_attribute("href") or ""
    assert href.rstrip("/") == "https://api.eventhub.rahulshettyacademy.com/api/docs"


def test_L05_featured_events_has_at_least_one_card(logged_in_home):
    """L-05: Featured Events has ≥1 Book Now (stable assert per T-05)."""
    expect(logged_in_home.page.get_by_role("heading", name="Featured Events")).to_be_visible()
    assert logged_in_home.book_now_links().count() >= 1


def test_L06_book_now_links_to_event_id(logged_in_home):
    """L-06: Book Now href matches /events/{id}."""
    first = logged_in_home.book_now_links().first
    expect(first).to_be_visible()
    href = first.get_attribute("href") or ""
    assert re.search(r"/events/\d+", href), f"unexpected Book Now href: {href}"


def test_L07_browse_or_explore_goes_to_events(logged_in_home):
    """L-07: Explore All Events (or Browse) → /events."""
    cta = logged_in_home.page.get_by_role("link", name=re.compile(r"Explore All Events|Browse Events", re.I)).first
    expect(cta).to_be_visible()
    cta.click()
    expect(logged_in_home.page).to_have_url(re.compile(r".*/events"))
    assert "/events" in logged_in_home.page.url


def test_L08_my_bookings_cta_goes_to_bookings(logged_in_home):
    """L-08: My Bookings control → /bookings."""
    # Prefer button CTA in hero if present; else first My Bookings link
    button = logged_in_home.page.get_by_role("button", name="My Bookings")
    if button.count():
        button.first.click()
    else:
        logged_in_home.page.get_by_role("link", name="My Bookings").first.click()
    expect(logged_in_home.page).to_have_url(re.compile(r".*/bookings"))
    assert "/bookings" in logged_in_home.page.url


def test_D01_featured_event_title_opens_detail(logged_in_home):
    """D-01: Click featured event title → /events/{id}."""
    # Title links wrap the event name (href /events/{id}), not "Book Now"
    title_link = logged_in_home.page.locator('a[href^="/events/"]').filter(
        has=logged_in_home.page.locator("h3")
    ).first
    expect(title_link).to_be_visible()
    title_link.click()
    expect(logged_in_home.page).to_have_url(re.compile(r".*/events/\d+"))
    assert re.search(r"/events/\d+", logged_in_home.page.url)
