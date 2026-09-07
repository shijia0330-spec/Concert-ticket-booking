from playwright.sync_api import expect

from pages.base_page import BasePage


class BookingsPage(BasePage):
    def open(self, origin: str) -> None:
        self.goto(origin.rstrip("/") + "/bookings")
        expect(self.page.get_by_role("heading", name="My Bookings")).to_be_visible()

    def clear_all_bookings(self) -> None:
        """Reset sandbox inventory — frees seats for booking tests."""
        if self.page.get_by_text("No bookings yet").count():
            return

        clear_btn = self.page.get_by_role("button", name="Clear all bookings")
        if clear_btn.count() == 0:
            return

        # Accept native confirm *during* click (avoid deadlock with expect_dialog after click)
        self.page.once("dialog", lambda dialog: dialog.accept())
        clear_btn.click(timeout=15000)
        expect(self.page.get_by_text("No bookings yet")).to_be_visible(timeout=20000)

    def expect_booking(self, event_name: str, tickets: int) -> None:
        expect(self.page.get_by_text(event_name).first).to_be_visible()
        expect(self.page.get_by_text(f"{tickets} tickets").first).to_be_visible()
        expect(self.page.get_by_text("confirmed").first).to_be_visible()

    def expect_booking_total(self, amount_text: str = "$600") -> None:
        expect(self.page.get_by_text(amount_text, exact=True).first).to_be_visible()
