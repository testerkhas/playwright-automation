from playwright.sync_api import Page, expect


class DashboardPage:

    def __init__(self, page: Page):
        self.page = page

        # Selectors
        self.heading      = page.locator("h2")
        self.logout_button = page.locator("a[href='/logout']")

    # Actions
    def logout(self):
        self.logout_button.click()

    # Assertions
    def verify_page_loaded(self):
        expect(self.heading).to_be_visible()
        expect(self.heading).to_have_text("Secure Area")

    def verify_url(self):
        expect(self.page).to_have_url(
            "https://the-internet.herokuapp.com/secure"
        )