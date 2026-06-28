from playwright.sync_api import Page, expect


class LoginPage:

    # ================================
    # SELECTORS - all in one place
    # ================================
    def __init__(self, page: Page):
        self.page = page

        # Define all elements here
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button   = page.locator("button[type='submit']")
        self.success_message = page.locator(".flash.success")
        self.error_message   = page.locator(".flash.error")

    # ================================
    # ACTIONS - what user can do
    # ================================
    def goto(self):
        self.page.goto("https://the-internet.herokuapp.com/login")

    def enter_username(self, username: str):
        self.username_input.fill(username)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    def login(self, username: str, password: str):
        # One method to do everything
        self.goto()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ================================
    # ASSERTIONS - what to verify
    # ================================
    def verify_login_success(self):
        expect(self.success_message).to_be_visible()

    def verify_login_failed(self):
        expect(self.error_message).to_be_visible()