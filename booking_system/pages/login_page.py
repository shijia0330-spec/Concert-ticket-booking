from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    def open(self, base_url: str) -> None:
        self.goto(base_url)
        expect(self.page.get_by_role("button", name="Sign In")).to_be_visible()

    def fill_email(self, email: str) -> None:
        self.page.get_by_label("Email").fill(email)

    def fill_password(self, password: str) -> None:
        self.page.get_by_label("Password").fill(password)

    def clear_credentials(self) -> None:
        self.page.get_by_label("Email").fill("")
        self.page.get_by_label("Password").fill("")

    def click_sign_in(self) -> None:
        self.page.get_by_role("button", name="Sign In").click()

    def dblclick_sign_in(self) -> None:
        self.page.get_by_role("button", name="Sign In").dblclick()

    def submit_credentials(self, email: str, password: str) -> None:
        """Fill and click Sign In — does not assume success or failure."""
        self.fill_email(email)
        self.fill_password(password)
        self.click_sign_in()

    def login(self, email: str, password: str) -> None:
        """Valid login — waits until home shows Logout."""
        self.submit_credentials(email, password)
        expect(self.page.get_by_role("button", name="Logout")).to_be_visible()

    def expect_authenticated(self) -> None:
        expect(self.page.get_by_role("button", name="Logout")).to_be_visible()

    def expect_unauthenticated(self) -> None:
        """Stay on login / no Logout (asserts from F-02 / validation cases)."""
        expect(self.page.get_by_role("button", name="Sign In")).to_be_visible()
        expect(self.page.get_by_role("button", name="Logout")).to_have_count(0)
        assert "/login" in self.page.url
