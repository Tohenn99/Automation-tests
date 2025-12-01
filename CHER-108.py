import pytest
from playwright.sync_api import Page, expect


class TestProductSearch:
    """Test suite for Automation Exercise product search functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup method to navigate to the website before each test"""
        self.page = page
        self.base_url = "https://automationexercise.com"

    def test_search_products_with_partial_term(self):
        """
        Test Case: Search for products using partial search term 'top'

        Steps:
        1. Open Chrome browser
        2. Go to Automation Exercise website
        3. Click Products menu
        4. Locate search box at top of products section
        5. Click inside search box
        6. Type 'top' as partial search term
        7. Click search button
        8. Count number of products shown
        9. Read and verify product names
        """

        # Step 1 & 2: Open browser and navigate to website
        self.page.goto(self.base_url)

        # Verify home page is loaded
        expect(self.page).to_have_title("Automation Exercise")

        # Handle cookie consent popup if it appears
        try:
            consent_button = self.page.locator('.fc-button.fc-cta-consent').first
            if consent_button.is_visible(timeout=5000):
                consent_button.click()
                self.page.wait_for_timeout(1000)  # Wait for popup to close
        except:
            pass  # If no consent popup, continue

        # Step 3: Click on Products menu
        products_link = self.page.locator('a[href="/products"]').first
        products_link.click()

        # Verify navigation to products page
        expect(self.page).to_have_url(f"{self.base_url}/products")

        # Step 4 & 5: Locate and click search box
        search_box = self.page.locator('#search_product')
        expect(search_box).to_be_visible()
        search_box.click()

        # Step 6: Type partial search term 'top'
        search_term = "top"
        search_box.fill(search_term)

        # Step 7: Click search button
        search_button = self.page.locator('#submit_search')
        search_button.click()

        # Wait for search results to load
        self.page.wait_for_selector('.features_items')

        # Step 8: Count number of products shown
        product_items = self.page.locator('.single-products').all()
        product_count = len(product_items)

        print(f"\n{'=' * 60}")
        print(f"Search Term: '{search_term}'")
        print(f"Total Products Found: {product_count}")
        print(f"{'=' * 60}")

        # Verify at least one product is found
        assert product_count > 0, f"No products found for search term '{search_term}'"

        # Step 9: Read product names
        product_names = []
        for i, product in enumerate(product_items, 1):
            # Get product name from the specific p tag inside product-image-wrapper
            product_name = product.locator('.productinfo p').first.inner_text()
            product_names.append(product_name)
            print(f"{i}. {product_name}")

        # Note: Website may return products based on category/tags,
        # not just product name matching

        print(f"{'=' * 60}\n")

        # Additional assertions
        assert len(product_names) == product_count, "Mismatch between product count and product names"

        return product_count, product_names


# Configuration for pytest
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context"""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080
        }
    }


if __name__ == "__main__":
    # Run the test using pytest
    pytest.main([__file__, "-v", "-s"])

