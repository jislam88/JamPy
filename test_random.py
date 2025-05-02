import re
from playwright.sync_api import Page, expect
from pytest import mark, fixture



class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("[data-test=\"username\"]")
        self.password_input = page.locator("[data-test=\"password\"]")
        self.login_button = page.locator("[data-test=\"login-button\"]")

    def navigate(self) -> 'LoginPage':
        """Navigate to login page"""
        self.page.goto("https://www.saucedemo.com/")
        return self

    def login(self, username: str, password: str) -> None:
        """Perform login with given credentials"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()


def test_login(page: Page) -> None:
    """Test login functionality"""
    login_page = LoginPage(page).navigate()
    login_page.login("standard_user", "secret_sauce")   
    expect(page.locator(".title")).to_have_text("Products")
def test_login_invalid(page: Page) -> None:
    """Test login with invalid credentials"""
    login_page = LoginPage(page).navigate()
    login_page.login("invalid_user", "invalid_password")
    expect(page.locator("[data-test=\"error\"]")).to_have_text("Epic sadface: Username and password do not match any user in this service")
    expect(page).to_have_url("https://www.saucedemo.com/")
