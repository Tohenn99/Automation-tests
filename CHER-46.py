import pytest
from playwright.sync_api import Page, expect


class TestMultiBrandShoppingCart:
    """Test suite for adding products from multiple brands to cart"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup method to navigate to the website before each test"""
        self.page = page
        self.base_url = "https://automationexercise.com"

    def handle_cookie_consent(self):
        """Handle cookie consent popup if it appears"""
        try:
            consent_button = self.page.locator('.fc-button.fc-cta-consent').first
            if consent_button.is_visible(timeout=5000):
                consent_button.click()
                self.page.wait_for_timeout(1000)
        except:
            pass

    def go_to_products_page(self):
        """Navigate to products page"""
        products_link = self.page.locator('a[href="/products"]').first
        products_link.click()
        self.page.wait_for_selector('.features_items')
        # URL might be /products or /brand_products/... so just wait for page load

    def filter_by_brand(self, brand_name):
        """Filter products by brand name"""
        print(f"\n🔍 Filtering by brand: {brand_name}")

        # Click on the brand in the sidebar
        brand_link = self.page.locator(f'.brands-name a:has-text("{brand_name}")')
        brand_link.click()

        # Wait for filtered results to load
        self.page.wait_for_selector('.features_items')
        self.page.wait_for_timeout(1000)

        print(f"✅ Filtered by {brand_name}")

    def add_product_to_cart(self, product_name, continue_shopping=True):
        """Add a specific product to cart by name"""
        print(f"🛒 Adding '{product_name}' to cart...")

        # Find the product container by name
        product_container = self.page.locator(f'.single-products:has(.productinfo p:text-is("{product_name}"))').first

        # Hover over the product to reveal Add to Cart button
        product_container.hover()
        self.page.wait_for_timeout(500)  # Wait for overlay to appear

        # Click the Add to Cart button in the overlay (more reliable)
        add_to_cart_btn = product_container.locator('.overlay-content .add-to-cart').first
        add_to_cart_btn.click()

        # Wait for modal to appear
        self.page.wait_for_selector('#cartModal', state='visible')

        if continue_shopping:
            # Click Continue Shopping button
            continue_btn = self.page.locator('button:has-text("Continue Shopping")')
            continue_btn.click()

            # Wait for modal to disappear
            self.page.wait_for_selector('#cartModal', state='hidden')
            print(f"✅ Added '{product_name}' - Continued shopping")
        else:
            print(f"✅ Added '{product_name}'")

    def view_cart(self):
        """Navigate to cart page"""
        print("\n🛒 Viewing cart...")

        # Click View Cart from the modal or navigate directly
        view_cart_link = self.page.locator('a:has-text("View Cart")').first
        view_cart_link.click()

        # Verify we're on cart page
        expect(self.page).to_have_url(f"{self.base_url}/view_cart")
        print("✅ On cart page")

    def get_cart_products(self):
        """Get all products currently in the cart"""
        cart_items = self.page.locator('#cart_info_table tbody tr').all()

        products = []
        for item in cart_items:
            try:
                product_name = item.locator('.cart_description h4 a').inner_text()
                products.append(product_name)
            except:
                pass  # Skip if not a product row

        return products

    def test_add_products_from_multiple_brands(self):
        """
        Test Case: Add products from different brands to cart

        Steps:
        1. Open browser and go to automationexercise.com
        2. Click Products
        3. Filter by MAST & HARBOUR brand
        4. Add Winter Top to cart, click Continue Shopping
        5. Go back to all products
        6. Filter by MADAME brand
        7. Add Sleeveless Dress to cart, click Continue Shopping
        8. Go back to all products
        9. Filter by BIBA brand
        10. Add Blue Cotton Indie Mickey Dress to cart
        11. Click View Cart
        12. Check all 3 products from different brands are in cart
        """

        print("\n" + "=" * 70)
        print("TEST: Add Products from Multiple Brands to Cart")
        print("=" * 70)

        # Step 1: Open browser and navigate to website
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Step 1: Opened automationexercise.com")

        # Step 2: Click Products
        self.go_to_products_page()
        print("✅ Step 2: Navigated to Products page")

        # Step 3: Filter by MAST & HARBOUR brand
        self.filter_by_brand("Mast & Harbour")
        print("✅ Step 3: Filtered by MAST & HARBOUR")

        # Step 4: Add Winter Top to cart, Continue Shopping
        self.add_product_to_cart("Winter Top", continue_shopping=True)
        print("✅ Step 4: Added Winter Top and continued shopping")

        # Step 5: Go back to all products
        self.go_to_products_page()
        print("✅ Step 5: Returned to all products")

        # Step 6: Filter by MADAME brand
        self.filter_by_brand("Madame")
        print("✅ Step 6: Filtered by MADAME")

        # Step 7: Add Sleeveless Dress to cart, Continue Shopping
        self.add_product_to_cart("Sleeveless Dress", continue_shopping=True)
        print("✅ Step 7: Added Sleeveless Dress and continued shopping")

        # Step 8: Go back to all products
        self.go_to_products_page()
        print("✅ Step 8: Returned to all products")

        # Step 9: Filter by BIBA brand
        self.filter_by_brand("Biba")
        print("✅ Step 9: Filtered by BIBA")

        # Step 10: Add Blue Cotton Indie Mickey Dress to cart
        self.add_product_to_cart("Blue Cotton Indie Mickey Dress", continue_shopping=False)
        print("✅ Step 10: Added Blue Cotton Indie Mickey Dress")

        # Step 11: Click View Cart
        self.view_cart()
        print("✅ Step 11: Navigated to cart")

        # Step 12: Verify all 3 products are in cart
        expected_products = [
            "Winter Top",
            "Sleeveless Dress",
            "Blue Cotton Indie Mickey Dress"
        ]

        cart_products = self.get_cart_products()

        print("\n" + "=" * 70)
        print("CART VERIFICATION")
        print("=" * 70)
        print(f"Expected products: {len(expected_products)}")
        print(f"Actual products in cart: {len(cart_products)}")
        print("\nProducts in cart:")

        for i, product in enumerate(cart_products, 1):
            status = "✅" if product in expected_products else "❌"
            print(f"{status} {i}. {product}")

        # Assertions
        assert len(cart_products) >= 3, f"Expected at least 3 products, found {len(cart_products)}"

        for expected_product in expected_products:
            assert expected_product in cart_products, \
                f"Product '{expected_product}' not found in cart. Cart contains: {cart_products}"

        print("\n" + "=" * 70)
        print("✅ TEST PASSED: All 3 products from different brands are in cart!")
        print("=" * 70 + "\n")


# Configuration for pytest
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context - full HD size"""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080
        },
        "no_viewport": False
    }


if __name__ == "__main__":
    # Run the test using pytest
    pytest.main([__file__, "-v", "-s", "--headed"])