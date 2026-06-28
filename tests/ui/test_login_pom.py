import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


# ================================
# TEST 1 - Successful Login
# ================================
def test_valid_login(page: Page):
    login = LoginPage(page)
    dashboard = DashboardPage(page)

    # Just one clean line to login!
    login.login("tomsmith", "SuperSecretPassword!")

    # Verify success
    login.verify_login_success()
    dashboard.verify_page_loaded()

    print("✅ Valid login passed!")


# ================================
# TEST 2 - Failed Login
# ================================
def test_invalid_login(page: Page):
    login = LoginPage(page)

    # Login with wrong password
    login.login("tomsmith", "wrongpassword")

    # Verify error shown
    login.verify_login_failed()

    print("✅ Invalid login correctly failed!")


# ================================
# TEST 3 - Login then Logout
# ================================
def test_login_then_logout(page: Page):
    login = LoginPage(page)
    dashboard = DashboardPage(page)

    # Login
    login.login("tomsmith", "SuperSecretPassword!")
    login.verify_login_success()

    # Verify dashboard
    dashboard.verify_page_loaded()
    dashboard.verify_url()

    # Logout
    dashboard.logout()

    # Verify back on login page
    expect_login = LoginPage(page)
    expect_login.goto()
    print("✅ Login and logout flow passed!")