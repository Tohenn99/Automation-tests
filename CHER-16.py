import pytest
from playwright.sync_api import Page, expect


class TestCartPersistence:
    """Test suite for verifying cart persistence across navigation"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup method to navigate to the website before each test"""
        self.page = page
        self.base_url = "https://automationexercise.com"
        self.added_products = []

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
        print("📄 Navigating to Products page...")
        products_link = self.page.locator('a[href="/products"]').first
        products_link.click()
        self.page.wait_for_selector('.features_items')
        print("✅ On Products page")

    def add_product_to_cart(self, product_name, continue_shopping=True):
        """Add a specific product to cart by name"""
        print(f"🛒 Adding '{product_name}' to cart...")

        # Find the product container by name
        product_container = self.page.locator(f'.single-products:has(.productinfo p:text-is("{product_name}"))').first

        # Hover over the product to reveal Add to Cart button
        product_container.hover()
        self.page.wait_for_timeout(500)

        # Click the Add to Cart button in the overlay
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

        # Track added product
        self.added_products.append(product_name)

    def go_to_home_page(self):
        """Navigate to home page"""
        print("🏠 Navigating to Home page...")
        home_link = self.page.locator('a[href="/"]').first
        home_link.click()
        self.page.wait_for_load_state('networkidle')
        print("✅ On Home page")

    def navigate_directly_to_cart(self, url):
        """Navigate directly to cart by typing URL in address bar"""
        print(f"🔗 Typing URL directly: {url}")

        # Simulate typing URL directly in address bar
        self.page.goto(url)

        # Wait for page to load
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(1000)

        print("✅ Navigated directly to cart URL")

    def get_cart_products_with_details(self):
        """Get detailed information about products in cart including quantities and totals"""
        cart_rows = self.page.locator('#cart_info_table tbody tr').all()

        products = []
        for row in cart_rows:
            try:
                product_name = row.locator('.cart_description h4 a').inner_text()
                price = row.locator('.cart_price p').inner_text()
                quantity = row.locator('.cart_quantity button').inner_text()
                total = row.locator('.cart_total_price').inner_text()

                products.append({
                    'name': product_name,
                    'price': price,
                    'quantity': quantity,
                    'total': total
                })
            except:
                pass  # Skip if not a product row

        return products

    def test_cart_persistence_after_direct_url_navigation(self):
        """
        Test Case: Verify cart persistence when navigating directly to cart URL

        Steps:
        1. Open browser
        2. Go to Automation Exercise
        3. Click Products
        4. Add 2-3 products to cart
        5. Note down products added
        6. Navigate away from cart (go to Home page)
        7. Clear address bar
        8. Type "http://automationexercise.com/view_cart" directly
        9. Press Enter
        10. Wait for page to load
        11. Check if previously added products are still in cart
        12. Check quantities and totals
        """

        print("\n" + "=" * 70)
        print("TEST: Cart Persistence After Direct URL Navigation")
        print("=" * 70)

        # Step 1 & 2: Open browser and navigate to website
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Step 1-2: Opened Automation Exercise website")

        # Step 3: Click Products
        self.go_to_products_page()
        print("✅ Step 3: On Products page")

        # Step 4: Add 2-3 products to cart
        print("\n" + "-" * 70)
        print("ADDING PRODUCTS TO CART")
        print("-" * 70)

        self.add_product_to_cart("Blue Top", continue_shopping=True)
        self.add_product_to_cart("Men Tshirt", continue_shopping=True)
        self.add_product_to_cart("Sleeveless Dress", continue_shopping=False)

        print("✅ Step 4: Added 3 products to cart")

        # Step 5: Note down products added
        print("\n" + "-" * 70)
        print("PRODUCTS ADDED (NOTED)")
        print("-" * 70)

        for i, product in enumerate(self.added_products, 1):
            print(f"{i}. {product}")

        print(f"\nTotal products added: {len(self.added_products)}")
        print("✅ Step 5: Products noted down")

        # View cart to capture initial state
        view_cart_link = self.page.locator('a:has-text("View Cart")').first
        view_cart_link.click()
        self.page.wait_for_load_state('networkidle')

        # Capture initial cart state
        print("\n" + "-" * 70)
        print("INITIAL CART STATE (Before Navigation)")
        print("-" * 70)

        initial_cart_products = self.get_cart_products_with_details()

        for i, product in enumerate(initial_cart_products, 1):
            print(f"{i}. {product['name']}")
            print(f"   Price: {product['price']} | Quantity: {product['quantity']} | Total: {product['total']}")

        assert len(initial_cart_products) == len(self.added_products), \
            f"Cart should contain {len(self.added_products)} products"

        # Step 6: Navigate away from cart (go to Home page)
        self.go_to_home_page()
        print("✅ Step 6: Navigated to Home page (away from cart)")

        # Step 7-9: Type cart URL directly in address bar
        print("\n" + "-" * 70)
        print("DIRECT URL NAVIGATION")
        print("-" * 70)

        cart_url = f"{self.base_url}/view_cart"
        self.navigate_directly_to_cart(cart_url)
        print("✅ Step 7-9: Typed and navigated to cart URL directly")

        # Step 10: Wait for page to load (already done in navigate method)
        print("✅ Step 10: Page loaded")

        # Step 11: Check if previously added products are still in cart
        print("\n" + "-" * 70)
        print("FINAL CART STATE (After Direct URL Navigation)")
        print("-" * 70)

        final_cart_products = self.get_cart_products_with_details()

        for i, product in enumerate(final_cart_products, 1):
            print(f"{i}. {product['name']}")
            print(f"   Price: {product['price']} | Quantity: {product['quantity']} | Total: {product['total']}")

        # Verify all products are still in cart
        assert len(final_cart_products) == len(self.added_products), \
            f"Expected {len(self.added_products)} products, found {len(final_cart_products)}"

        final_product_names = [p['name'] for p in final_cart_products]

        for added_product in self.added_products:
            assert added_product in final_product_names, \
                f"Product '{added_product}' not found in cart after direct navigation"

        print("✅ Step 11: All previously added products are still in cart!")

        # Step 12: Check quantities and totals
        print("\n" + "-" * 70)
        print("VERIFICATION: Quantities and Totals")
        print("-" * 70)

        # Compare initial and final cart states
        for initial_product in initial_cart_products:
            final_product = next(
                (p for p in final_cart_products if p['name'] == initial_product['name']),
                None
            )

            if final_product:
                print(f"\n✓ {initial_product['name']}")
                print(f"  Quantity: {initial_product['quantity']} → {final_product['quantity']}")
                print(f"  Total: {initial_product['total']} → {final_product['total']}")

                assert initial_product['quantity'] == final_product['quantity'], \
                    f"Quantity mismatch for {initial_product['name']}"
                assert initial_product['total'] == final_product['total'], \
                    f"Total mismatch for {initial_product['name']}"

                print("  ✅ Quantity and total unchanged")

        print("\n✅ Step 12: All quantities and totals verified!")

        print("\n" + "=" * 70)
        print("✅ TEST PASSED: Cart persisted after direct URL navigation!")
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