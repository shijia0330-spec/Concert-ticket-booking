from playwright.sync_api import expect

from pages.base_page import BasePage


class EventPage(BasePage):
    def open(self, event_url: str) -> None:
        self.goto(event_url)
        expect(self.page.get_by_role("button", name="Confirm Booking")).to_be_visible()

    def open_dilli_diwali_mela(self, origin: str) -> None:
        self.open(origin.rstrip("/") + "/events/3")
        expect(self.page.get_by_role("heading", name="Dilli Diwali Mela").first).to_be_visible()

    def set_quantity(self, qty: int) -> None:
        """Increase from default 1 using + until qty reached (max 8)."""
        if qty < 1:
            raise ValueError("qty must be >= 1")
        plus = self.page.get_by_role("button", name="+")
        for _ in range(qty - 1):
            plus.click()

    def fill_booking_form(self, full_name: str, email: str, phone: str) -> None:
        self.page.locator("#customerName").fill(full_name)
        self.page.locator("#customer-email").fill(email)
        self.page.locator("#phone").fill(phone)

    def clear_booking_form(self) -> None:
        self.page.locator("#customerName").fill("")
        self.page.locator("#customer-email").fill("")
        self.page.locator("#phone").fill("")

    def confirm_booking(self) -> None:
        self.page.get_by_role("button", name="Confirm Booking").click()

    def expect_booking_confirmed(self, tickets: int = 2) -> None:
        expect(self.page.get_by_text("Booking Confirmed!")).to_be_visible()
        expect(self.page.get_by_text("Your tickets are reserved.")).to_be_visible()
        expect(self.page.get_by_text("Booking Ref")).to_be_visible()
        # Confirmation summary lists ticket count under Tickets
        expect(self.page.get_by_text("Tickets").first).to_be_visible()
        expect(self.page.locator("text=Tickets").locator("..").get_by_text(str(tickets), exact=True)).to_be_visible()

    def expect_total(self, amount_text: str = "$600") -> None:
        """Assert Total amount visible on book form or confirmation (e.g. $600)."""
        expect(self.page.get_by_text("Total").first).to_be_visible()
        expect(self.page.get_by_text(amount_text, exact=True).first).to_be_visible()
