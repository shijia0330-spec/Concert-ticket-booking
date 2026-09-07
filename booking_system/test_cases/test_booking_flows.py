"""Automation for EventHub_Booking_testcases.md — F-01 / V-01 / V-02 / V-03 / L-01."""

from playwright.sync_api import expect


EVENT_NAME = "Dilli Diwali Mela"
TICKETS = 2
TOTAL = "$600"


def test_F01_book_dilli_diwali_mela_qty2_and_see_in_bookings(
    cleared_bookings,
    event_page,
    bookings_page,
    course_config,
    site_origin,
):
    """F-01 (+ L-01): Book ×2 with required fields → Confirmed → My Bookings."""
    event_page.open_dilli_diwali_mela(site_origin)
    event_page.set_quantity(TICKETS)
    event_page.fill_booking_form(
        full_name="Shi Jia Test",
        email=course_config["email"],
        phone="+91 98765 43210",
    )
    event_page.confirm_booking()
    event_page.expect_booking_confirmed(tickets=TICKETS)
    event_page.expect_total(TOTAL)

    # User assert: transaction under My Bookings
    bookings_page.open(site_origin)
    bookings_page.expect_booking(EVENT_NAME, tickets=TICKETS)
    bookings_page.expect_booking_total(TOTAL)


def test_V01_empty_compulsory_fields_block_confirm(cleared_bookings, event_page, site_origin):
    """V-01: Empty required fields → Booking Confirmed! does not appear."""
    event_page.open_dilli_diwali_mela(site_origin)
    event_page.clear_booking_form()
    event_page.confirm_booking()

    expect(event_page.page.get_by_text("Booking Confirmed!")).to_have_count(0)


def test_V02_qty2_updates_price_line(cleared_bookings, event_page, site_origin):
    """V-02: Qty 2 shows × 2 tickets in price line before confirm."""
    event_page.open_dilli_diwali_mela(site_origin)
    event_page.set_quantity(TICKETS)

    expect(event_page.page.get_by_text("× 2 tickets")).to_be_visible()


def test_V03_qty2_total_equals_600(cleared_bookings, event_page, site_origin):
    """V-03: Qty 2 → Total $600 (automated)."""
    event_page.open_dilli_diwali_mela(site_origin)
    event_page.set_quantity(TICKETS)

    event_page.expect_total(TOTAL)
    assert event_page.page.get_by_text(TOTAL, exact=True).first.is_visible()
