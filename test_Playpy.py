##Jam iA##
import re
import os
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page, expect

def test_TableSortSearch(page: Page) -> None:
    """Test table sorting and searching functionality"""
    page.goto("https://www.lambdatest.com/selenium-playground/")
    page.get_by_role("link", name="Table Sort & Search").click()
    page.get_by_role("searchbox", name="Search:").click()
    page.get_by_role("searchbox", name="Search:").fill("Tokyo")
    expect(page.get_by_role("gridcell", name="Tokyo").first).to_be_visible()
    page.get_by_role("searchbox", name="Search:").click()
    page.get_by_role("searchbox", name="Search:").dblclick()
    page.get_by_role("searchbox", name="Search:").fill("")
    page.get_by_role("gridcell", name="Position: activate to sort").click()
    page.get_by_role("gridcell", name="Office: activate to sort").click()
    page.get_by_role("gridcell", name="Age: activate to sort column").click()
    page.get_by_text("2", exact=True).click()
    page.get_by_text("3", exact=True).click()
    expect(page.get_by_text("Showing 21 to 24 of 24 entries")).to_be_visible()

def test_DownloadCSVFile(page: Page) -> None:
    """Test CSV file download functionality"""
    try:
        # Create downloads directory if it doesn't exist
        download_dir = Path("downloads")
        download_dir.mkdir(exist_ok=True)

        # Navigate to the page
        page.goto("https://www.lambdatest.com/selenium-playground/")
        page.get_by_role("link", name="Table Data Download").click()
        
        # Handle download with proper timestamp and path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"TESTCSV_{timestamp}.csv"
        download_path = download_dir / filename

        # Wait for and handle download
        with page.expect_download() as download_info:
            page.get_by_role("link", name="CSV").click()
        
        download = download_info.value
        download.save_as(str(download_path))
        
        # Verify download
        assert download_path.exists(), f"Download failed: {filename}"
        print(f"File downloaded successfully to: {download_path}")
        print(f"File size: {os.path.getsize(download_path)} bytes")

    except Exception as e:
        print(f"Error during download: {str(e)}")
        raise
    finally:
        # Ensure page is cleaned up
        if page and not page.is_closed():
            page.close()


def test_MultiSelect(page: Page) -> None:
    page.goto("https://www.lambdatest.com/selenium-playground/")
    page.get_by_role("link", name="Select Dropdown List").click()
    expect(page.get_by_role("heading", name="Dropdown Demo")).to_be_visible()
    page.locator("#multi-select").select_option("Washington")
    page.locator("#multi-select").select_option(["Pennsylvania", "Washington"])
    page.locator("#multi-select").select_option(["Texas", "Pennsylvania", "Washington"])
    page.get_by_role("button", name="First Selected").click()
    page.get_by_role("button", name="Get Last Selected").click()
    expect(page.locator("[id=\"__next\"]")).to_contain_text("Washington")
    expect(page.locator("[id=\"__next\"]")).to_contain_text("Washington,Pennsylvania,Texas")
    page.close()


def test_iFrame(page: Page) -> None:
    page.goto("https://www.lambdatest.com/selenium-playground/")
    page.get_by_role("link", name="iFrame Demo").click()
    expect(page.get_by_text("Simple iFrame containing Editor")).to_be_visible()
    expect(page.get_by_text("Simple iFrame containing webpage")).to_be_visible()
    expect(page.locator("div").filter(has_text=re.compile(r"^Simple iFrame containing Editor$")).locator("iframe").content_frame.get_by_text("Your content.")).to_be_visible()
    expect(page.locator("div").filter(has_text=re.compile(r"^Simple iFrame containing webpage$")).locator("iframe").content_frame.get_by_text("LambdaTest Documentation and Knowledge Hub")).to_be_visible()
