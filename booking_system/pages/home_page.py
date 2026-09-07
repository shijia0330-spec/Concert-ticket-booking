from playwright.sync_api import expect

from pages.base_page import BasePage


class HomePage(BasePage):
    def open(self, home_url: str) -> None:
        self.goto(home_url)

    def expect_home(self) -> None:
        expect(self.page.get_by_role("button", name="Logout")).to_be_visible()
        expect(self.page.get_by_role("heading", name="Featured Events")).to_be_visible()

    def expect_hero(self) -> None:
        expect(self.page.get_by_role("heading", name="Discover & Book Amazing Events")).to_be_visible()

    def nav_link(self, name: str):
        return self.page.get_by_role("link", name=name).first

    def click_nav(self, name: str) -> None:
        self.nav_link(name).click()

    def book_now_links(self):
        return self.page.get_by_role("link", name="Book Now")

    def featured_event_title_links(self):
        # Event titles under Featured Events are links to /events/{id}
        return self.page.locator('a[href^="/events/"]').filter(has_not_text="Book Now")
