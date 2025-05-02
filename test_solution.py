from objects.playwright_page import PlaywrightPage
from playwright.sync_api import Page, expect

def test_doc_link(page: Page):
    """Test documentation link navigation"""
    homepage = PlaywrightPage(page)
    homepage.visit_docs()
    expect(page).to_have_url("https://playwright.dev/python/docs/intro")

def test_docs_search(page: Page):
    """Test search functionality"""
    query = "assertions"
    homepage = PlaywrightPage(page)
    page.goto("https://playwright.dev/python")  # Ensure we start at homepage
    homepage.search(query)
    expect(homepage.search_dropdown).to_be_visible()
    expect(homepage.search_dropdown).to_contain_text("List of assertions")

if __name__ == "__main__":
    print("Test file loaded successfully.")