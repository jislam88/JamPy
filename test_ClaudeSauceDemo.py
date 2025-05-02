import os
import pytest
from datetime import datetime
from playwright.sync_api import Page, Browser, Expect
from objects.Stuff import LoginPage, InventoryPage, CartPage, CheckoutInfoPage, CheckoutOverviewPage, CheckoutCompletePage
from objects.Stuff import TestData, ScreenshotHelper


## fixtures
@pytest.fixture
def login_page(page: Page):
    return LoginPage(page).navigate()

@pytest.fixture
def logged_in_page(login_page):
    user = TestData.USERS["standard"]
    return login_page.login(user["username"], user["password"])

# Pytest hook for automatic screenshot on test failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Only take screenshot on failure during the "call" phase of a test
    if report.when == "call" and report.failed:
        page = None
        for fixture_name in item.fixturenames:
            if fixture_name == "page":
                page = item.funcargs[fixture_name]
                break

        if page:
            # Create screenshots directory if it doesn't exist
            screenshots_dir = os.path.join("screenshots", "failures", datetime.now().strftime("%Y-%m-%d"))
            os.makedirs(screenshots_dir, exist_ok=True)
            
            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%H-%M-%S")
            filename = f"{item.name}_failure_{timestamp}.png"
            path = os.path.join(screenshots_dir, filename)

            # Take screenshot
            try:
                page.screenshot(path=path, full_page=True)
                print(f"Screenshot on failure: {path}")
            except Exception as e:
                print(f"Failed to take screenshot: {e}")

# Tests

def test_complete_purchase_with_multiple_items(login_page):
    # Setup screenshot helper
    page = login_page.page
    screenshot = ScreenshotHelper(page, "complete_purchase")
    
    try:
        # Arrange
        user = TestData.USERS["standard"]
        customer = TestData.CUSTOMER_INFO["customer1"]

        # Act & Assert
        inventory_page = login_page.login(user["username"], user["password"])
        screenshot.take_screenshot("after_login")

        # Add multiple items to cart
        inventory_page.add_item_to_cart(TestData.PRODUCTS["backpack"])
        inventory_page.add_item_to_cart(TestData.PRODUCTS["bike_light"])
        inventory_page.add_item_to_cart(TestData.PRODUCTS["bolt_shirt"])
        inventory_page.add_item_to_cart(TestData.PRODUCTS["fleece_jacket"])
        screenshot.take_screenshot("items_added_to_cart")
        print("Items added to cart")
        
        # Complete checkout process
        cart_page = inventory_page.go_to_cart()
        screenshot.take_screenshot("cart_page")

        checkout_info_page = cart_page.proceed_to_checkout()
        screenshot.take_screenshot("checkout_info_page")

        checkout_overview_page = checkout_info_page.fill_customer_info(
            customer["firstName"], 
            customer["lastName"], 
            customer["postalCode"]
        ).continue_checkout()
        screenshot.take_screenshot("checkout_overview_page")

        # Finish order and verify
        checkout_complete_page = checkout_overview_page.complete_purchase()
        screenshot.take_screenshot("order_complete")
        
        checkout_complete_page.verify_order_completion()
        checkout_complete_page.back_to_products()
        screenshot.take_screenshot("back_to_products")
    except Exception as e:
        # Take screenshot on exception
        screenshot.take_screenshot("exception")
        raise e


def test_purchase_with_form_validation(logged_in_page):
    # Setup screenshot helper
    page = logged_in_page.page
    screenshot = ScreenshotHelper(page, "form_validation")

    try:
        # Add items to cart and get cart page instance
        inventory_page = logged_in_page
        screenshot.take_screenshot("start_inventory_page")

        cart_page = (inventory_page
            .add_item_to_cart(TestData.PRODUCTS["onesie"])
            .add_item_to_cart(TestData.PRODUCTS["red_shirt"])
            .go_to_cart())
        screenshot.take_screenshot("cart_page")

        # Test form validation
        checkout_info_page = cart_page.proceed_to_checkout()
        screenshot.take_screenshot("checkout_info_page")

        checkout_info_page.try_continue_without_info()
        screenshot.take_screenshot("validation_error")

        # Complete the purchase after validation
        customer = TestData.CUSTOMER_INFO["customer2"]
        checkout_info_page.fill_customer_info(
            customer["firstName"], 
            customer["lastName"], 
            customer["postalCode"]
        )
        screenshot.take_screenshot("checkout_info_filled")

        checkout_overview_page = checkout_info_page.continue_checkout()
        screenshot.take_screenshot("checkout_overview_page")

        # Finish order and verify
        checkout_complete_page = checkout_overview_page.complete_purchase()
        screenshot.take_screenshot("order_complete")

        checkout_complete_page.verify_order_completion()
        checkout_complete_page.back_to_products()
        screenshot.take_screenshot("back_to_products")
    except Exception as e:
        # Take screenshot on exception
        screenshot.take_screenshot("exception")
        raise e
    

