from playwright.sync_api import Page, expect

def test_browser_opens(page: Page):
    # Open example site
    page.goto("https://example.com")
    
    # Check title
    expect(page).to_have_title("Example Domain")
    
    print("✅ Browser opened successfully!")


def test_input_and_click(page: Page):
    # This site is made for automation practice
    page.goto("https://the-internet.herokuapp.com/login")
    
    # Fill username and password
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    
    # Click login button
    page.click("button[type='submit']")
    
    # Check login was successful
    expect(page.locator(".flash.success")).to_be_visible()
    
    print("✅ Login test passed!")


def test_checkbox(page: Page):
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    
    # Get first checkbox and click it
    checkbox = page.locator("input[type='checkbox']").first
    checkbox.check()
    
    # Verify it is checked
    expect(checkbox).to_be_checked()
    
    print("✅ Checkbox test passed!")