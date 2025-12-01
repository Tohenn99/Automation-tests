import pytest
from playwright.sync_api import Page, expect


class TestRemoveProductFromCart:
    """Test suite for removing products from shopping cart"""

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

    def view_cart(self):
        """Navigate to cart page"""
        print("🛒 Navigating to View Cart...")

        # Click View Cart
        view_cart_link = self.page.locator('a:has-text("View Cart")').first
        view_cart_link.click()

        # Verify we're on cart page
        expect(self.page).to_have_url(f"{self.base_url}/view_cart")
        print("✅ On cart page")

    def get_cart_products_details(self):
        """Get detailed information about products in cart"""
        cart_rows = self.page.locator('#cart_info_table tbody tr').all()

        products = []
        for row in cart_rows:
            try:
                product_name = row.locator('.cart_description h4 a').inner_text()
                quantity = row.locator('.cart_quantity button').inner_text()
                products.append({
                    'name': product_name,
                    'quantity': quantity,
                    'row': row
                })
            except:
                pass  # Skip if not a product row

        return products

    def remove_product_from_cart(self, product_name):
        """Remove a specific product from cart by clicking X button"""
        print(f"🗑️ Removing '{product_name}' from cart...")

        # Find the row containing the product
        product_row = self.page.locator(
            f'#cart_info_table tbody tr:has(.cart_description h4 a:text-is("{product_name}"))').first

        # Locate and click the orange X button in the delete column
        delete_btn = product_row.locator('.cart_delete a.cart_quantity_delete').first
        delete_btn.click()

        # Wait for page to reload/refresh
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(1000)

        print(f"✅ Removed '{product_name}' from cart")

    def test_remove_product_from_cart(self):
        """
        Test Case: Add 3 products to cart and remove the middle one

        Steps:
        1. Open browser and navigate to automationexercise.com
        2. Go to Products page
        3. Add Blue Top to cart, continue shopping
        4. Add Men Tshirt to cart, continue shopping
        5. Add Sleeveless Dress to cart
        6. Click View Cart
        7. Locate all three products in cart table
        8. Find Men Tshirt row (middle product)
        9. Locate orange X button in Total column for Men Tshirt
        10. Click X button for Men Tshirt
        11. Wait for page to refresh/reload
        12. Check cart contents
        13. Count remaining products
        14. Check if Blue Top and Sleeveless Dress are still present
        15. Check their quantities haven't changed
        """

        print("\n" + "=" * 70)
        print("TEST: Remove Product from Cart")
        print("=" * 70)

        # Step 1: Open browser and navigate to website
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Step 1: Opened automationexercise.com")

        # Step 2: Go to Products page
        self.go_to_products_page()
        print("✅ Step 2: On Products page")

        # Step 3: Add Blue Top to cart, continue shopping
        self.add_product_to_cart("Blue Top", continue_shopping=True)
        print("✅ Step 3: Added Blue Top")

        # Step 4: Add Men Tshirt to cart, continue shopping
        self.add_product_to_cart("Men Tshirt", continue_shopping=True)
        print("✅ Step 4: Added Men Tshirt")

        # Step 5: Add Sleeveless Dress to cart
        self.add_product_to_cart("Sleeveless Dress", continue_shopping=False)
        print("✅ Step 5: Added Sleeveless Dress")

        # Step 6: Click View Cart
        self.view_cart()
        print("✅ Step 6: Viewing cart")

        # Step 7: Locate all three products in cart table
        print("\n" + "-" * 70)
        print("INITIAL CART STATE")
        print("-" * 70)

        initial_products = self.get_cart_products_details()
        print(f"Total products in cart: {len(initial_products)}")

        for i, product in enumerate(initial_products, 1):
            print(f"{i}. {product['name']} - Quantity: {product['quantity']}")

        # Verify all 3 products are present
        assert len(initial_products) == 3, f"Expected 3 products, found {len(initial_products)}"

        product_names = [p['name'] for p in initial_products]
        assert "Blue Top" in product_names, "Blue Top not found in cart"
        assert "Men Tshirt" in product_names, "Men Tshirt not found in cart"
        assert "Sleeveless Dress" in product_names, "Sleeveless Dress not found in cart"

        print("✅ Step 7: All 3 products located in cart")

        # Save initial quantities
        blue_top_initial = next(p for p in initial_products if p['name'] == "Blue Top")
        sleeveless_dress_initial = next(p for p in initial_products if p['name'] == "Sleeveless Dress")

        # Steps 8-10: Find Men Tshirt and click X button
        print("\n" + "-" * 70)
        print("REMOVING MEN TSHIRT")
        print("-" * 70)
        self.remove_product_from_cart("Men Tshirt")
        print("✅ Steps 8-10: Found and removed Men Tshirt")

        # Step 11: Wait for page to refresh (already done in remove method)
        print("✅ Step 11: Page refreshed")

        # Steps 12-15: Check cart contents after removal
        print("\n" + "-" * 70)
        print("FINAL CART STATE")
        print("-" * 70)

        final_products = self.get_cart_products_details()
        print(f"Total products in cart: {len(final_products)}")

        for i, product in enumerate(final_products, 1):
            print(f"{i}. {product['name']} - Quantity: {product['quantity']}")

        # Step 13: Count remaining products
        assert len(final_products) == 2, f"Expected 2 products after removal, found {len(final_products)}"
        print("✅ Step 13: Correct number of products remaining (2)")

        # Step 14: Check if Blue Top and Sleeveless Dress are still present
        final_product_names = [p['name'] for p in final_products]

        assert "Blue Top" in final_product_names, "Blue Top should still be in cart"
        assert "Sleeveless Dress" in final_product_names, "Sleeveless Dress should still be in cart"
        assert "Men Tshirt" not in final_product_names, "Men Tshirt should be removed from cart"
        print("✅ Step 14: Blue Top and Sleeveless Dress still present")

        # Step 15: Check their quantities haven't changed
        blue_top_final = next(p for p in final_products if p['name'] == "Blue Top")
        sleeveless_dress_final = next(p for p in final_products if p['name'] == "Sleeveless Dress")

        assert blue_top_initial['quantity'] == blue_top_final['quantity'], \
            f"Blue Top quantity changed from {blue_top_initial['quantity']} to {blue_top_final['quantity']}"
        assert sleeveless_dress_initial['quantity'] == sleeveless_dress_final['quantity'], \
            f"Sleeveless Dress quantity changed from {sleeveless_dress_initial['quantity']} to {sleeveless_dress_final['quantity']}"

        print("✅ Step 15: Quantities unchanged for remaining products")

        print("\n" + "=" * 70)
        print("✅ TEST PASSED: Product successfully removed from cart!")
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