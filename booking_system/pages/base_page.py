from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str) -> None:
        self.page.goto(url)

    def expect_visible(self, locator) -> None:
        expect(locator).to_be_visible()
