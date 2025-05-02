import os
import pytest
from datetime import datetime
from playwright.sync_api import Page, Browser, expect


# Page Objects
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("[data-test=\"username\"]")
        self.password_input = page.locator("[data-test=\"password\"]")
        self.login_button = page.locator("[data-test=\"login-button\"]")
        self.app_root = page.locator("#root")

    def navigate(self):
        self.page.goto("https://www.saucedemo.com/")
        expect(self.app_root).to_contain_text("Swag Labs")
        return self

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return InventoryPage(self.page)

class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.shopping_cart_link = page.locator("[data-test=\"shopping-cart-link\"]")

    def add_item_to_cart(self, item_id):
        self.page.locator(f"[data-test=\"add-to-cart-{item_id}\"]").click()
        return self

    def go_to_cart(self):
        expect(self.shopping_cart_link).to_be_visible()
        self.shopping_cart_link.click()
        return CartPage(self.page)

class CartPage:
    def __init__(self, page):
        self.page = page
        self.checkout_button = page.locator("[data-test=\"checkout\"]")
        self.title = page.locator("[data-test=\"title\"]")

    def proceed_to_checkout(self):
        expect(self.title).to_contain_text("Your Cart")
        self.checkout_button.click()
        return CheckoutInfoPage(self.page)

class CheckoutInfoPage:
    def __init__(self, page):
        self.page = page
        self.first_name_input = page.locator("[data-test=\"firstName\"]")
        self.last_name_input = page.locator("[data-test=\"lastName\"]")
        self.postal_code_input = page.locator("[data-test=\"postalCode\"]")
        self.continue_button = page.locator("[data-test=\"continue\"]")
        self.error_message = page.locator("[data-test=\"error\"]")

    def fill_customer_info(self, first_name, last_name, postal_code):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        return self

    def continue_checkout(self):
        expect(self.continue_button).to_be_visible()
        self.continue_button.click()
        return CheckoutOverviewPage(self.page)

    def try_continue_without_info(self):
        self.continue_button.click()
        expect(self.error_message).to_contain_text("Error: First Name is required")
        return self

class CheckoutOverviewPage:
    def __init__(self, page):
        self.page = page
        self.finish_button = page.locator("[data-test=\"finish\"]")
        self.payment_info = page.locator("[data-test=\"payment-info-label\"]")

    def complete_purchase(self):
        expect(self.payment_info).to_contain_text("Payment Information:")
        self.finish_button.click()
        return CheckoutCompletePage(self.page)

class CheckoutCompletePage:
    def __init__(self, page):
        self.page = page
        self.complete_header = page.locator("[data-test=\"complete-header\"]")
        self.back_button = page.locator("[data-test=\"back-to-products\"]")

    def verify_order_completion(self):
        expect(self.complete_header).to_contain_text("Thank you for your order!")
        return self

    def back_to_products(self):
        self.back_button.click()
        return InventoryPage(self.page)

# Test Data
class TestData:
    USERS = {
        "standard": {
            "username": "standard_user",
            "password": "secret_sauce"
        }
    }

    CUSTOMER_INFO = {
        "customer1": {
            "firstName": "QAQ",
            "lastName": "AAQA",
            "postalCode": "22123"
        },
        "customer2": {
            "firstName": "Orange",
            "lastName": "Name",
            "postalCode": "332211"
        }
    }

    PRODUCTS = {
        "backpack": "sauce-labs-backpack",
        "bike_light": "sauce-labs-bike-light",
        "bolt_shirt": "sauce-labs-bolt-t-shirt",
        "fleece_jacket": "sauce-labs-fleece-jacket",
        "onesie": "sauce-labs-onesie",
        "red_shirt": "test.allthethings()-t-shirt-(red)"
    }

# Screenshot helper class
class ScreenshotHelper:
    def __init__(self, page, test_name):
        self.page = page
        self.test_name = test_name
        self.screenshot_dir = os.path.join("screenshots", datetime.now().strftime("%Y-%m-%d"))
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def take_screenshot(self, step_name):
        """Take screenshot at a specific step"""
        timestamp = datetime.now().strftime("%H-%M-%S")
        filename = f"{self.test_name}_{step_name}_{timestamp}.png"
        path = os.path.join(self.screenshot_dir, filename)
        self.page.screenshot(path=path, full_page=True)
        print(f"Screenshot saved: {path}")
        return path
