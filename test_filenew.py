import pytest
from playwright.sync_api import sync_playwright

def test_get_cat_fact_with_max_length():
    with sync_playwright() as p:
        request_context = p.request.new_context()
        response = request_context.get("https://catfact.ninja/fact?max_length=55")

        # Assert status code is 200 OK
        assert response.status == 200, f"Expected 200 but got {response.status}"

        # Parse and validate response
        json_response = response.json()
        assert "fact" in json_response, f"'fact' key not in response: {json_response}"

        # Assert fact length is less than or equal to 55
        fact = json_response["fact"]
        assert len(fact) <= 55, f"Expected fact length <= 55, got {len(fact)}: '{fact}'"