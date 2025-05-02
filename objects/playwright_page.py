from playwright.sync_api import Page, expect

class PlaywrightPage:
    def __init__(self, page: Page):
        self.page = page
        self.page.goto("https://playwright.dev/python")
        self.docs_link = page.get_by_role("link", name="Docs", exact=True)
        self.search_input = page.get_by_placeholder("Search docs")
        self.search_dropdown = page.locator(".DocSearch-Dropdown")

    def visit_docs(self) -> None:
        """Click the docs link and navigate to documentation"""
        self.docs_link.click()
        expect(self.page).to_have_title("Installation | Playwright Python")
    
    def search(self, query: str) -> None:
        """Perform search using keyboard shortcut"""
        self.page.keyboard.press("Control+K")
        self.search_input.fill(query)
        expect(self.search_input).to_have_value(query)

    def search_results(self) -> None:
        """Get search results dropdown"""
        expect(self.search_dropdown).to_be_visible()
        return self.search_dropdown.is_visible()
    
print ("PlaywrightPage class loaded successfully.")

