import csv
import pytest
from pages.login_page import LoginPage

def load_credentials():
    with open("data/credentials.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return [(row["username"], row["password"]) for row in reader]

@pytest.mark.parametrize("username,password", load_credentials())
def test_login_with_csv(page, username, password):
    login_page = LoginPage(page)
    page.goto("https://www.saucedemo.com/")
    login_page.login(username, password)

    if username == "standard_user" and password == "secret_sauce":
        assert page.url == "https://www.saucedemo.com/inventory.html"
    else:
        assert login_page.get_error_message() != ""