import pytest
from playwright.sync_api import Page, expect


class TestRemoveAllProductsFromCart:
    """Test suite for removing all products from cart"""

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

    def add_nth_product_to_cart(self, position, continue_shopping=True):
        """Add the nth product from current page to cart"""
        print(f"🛒 Adding product #{position} to cart...")

        # Get all products on the page
        products = self.page.locator('.single-products').all()

        if position > len(products):
            raise Exception(f"Only {len(products)} products available, cannot add product #{position}")

        # Get the specific product
        product = products[position - 1]

        # Get product name for tracking
        product_name = product.locator('.productinfo p').first.inner_text()

        # Hover over the product
        product.hover()
        self.page.wait_for_timeout(500)

        # Click Add to Cart button
        add_to_cart_btn = product.locator('.overlay-content .add-to-cart').first
        add_to_cart_btn.click()

        # Wait for modal
        self.page.wait_for_selector('#cartModal', state='visible')

        if continue_shopping:
            continue_btn = self.page.locator('button:has-text("Continue Shopping")')
            continue_btn.click()
            self.page.wait_for_selector('#cartModal', state='hidden')
            print(f"✅ Added '{product_name}' - Continued shopping")
        else:
            print(f"✅ Added '{product_name}'")

        self.added_products.append(product_name)
        return product_name

    def view_cart(self):
        """Navigate to cart page"""
        print("\n🛒 Viewing cart...")
        view_cart_link = self.page.locator('a:has-text("View Cart")').first
        view_cart_link.click()
        expect(self.page).to_have_url(f"{self.base_url}/view_cart")
        print("✅ On cart page")

    def get_cart_products(self):
        """Get all products currently in cart"""
        cart_rows = self.page.locator('#cart_info_table tbody tr').all()
        products = []

        for row in cart_rows:
            try:
                product_name = row.locator('.cart_description h4 a').inner_text()
                products.append(product_name)
            except:
                pass

        return products

    def remove_first_product(self):
        """Remove the first product from cart by clicking X button"""
        # Get the first product row
        first_row = self.page.locator('#cart_info_table tbody tr').first

        # Get product name before removing
        try:
            product_name = first_row.locator('.cart_description h4 a').inner_text()
        except:
            product_name = "Unknown"

        print(f"🗑️ Removing first product: '{product_name}'")

        # Click the X button
        delete_btn = first_row.locator('.cart_delete a.cart_quantity_delete').first
        delete_btn.click()

        # Wait for page to reload
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(1000)

        print(f"✅ Removed '{product_name}'")

    def check_cart_empty_message(self):
        """Check if cart shows empty message"""
        try:
            # Check for empty cart indicator - could be empty tbody or specific message
            cart_rows = self.page.locator('#cart_info_table tbody tr').all()

            if len(cart_rows) == 0:
                return True, "Cart table is empty"

            # Check for "Cart is empty" text anywhere on page
            empty_message = self.page.locator('text=Cart is empty')
            if empty_message.is_visible(timeout=2000):
                return True, "Cart is empty message displayed"

            # Check if there's a specific empty state
            empty_cart = self.page.locator('#empty_cart')
            if empty_cart.is_visible(timeout=2000):
                return True, "Empty cart element visible"

            return False, f"{len(cart_rows)} products still in cart"

        except:
            return False, "Could not determine cart state"

    def test_remove_all_products_from_cart(self):
        """
        Test Case: Add 4 products and remove all of them - 07

        Steps:
        1. Open Chrome browser
        2. Navigate to http://automationexercise.com
        3. Add 4 different products to cart
        4. Go to cart page by clicking View Cart
        5. Click X button for first product
        6. Click X button for second product
        7. Click X button for third product
        8. Click X button for fourth product
        9. Observe cart page content
        10. Check if any products remain
        """

        print("\n" + "=" * 70)
        print("TEST: Remove All Products from Cart")
        print("=" * 70)

        # Step 1 & 2: Open browser and navigate to website
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Step 1-2: Opened http://automationexercise.com")

        # Navigate to products page
        self.go_to_products_page()

        # Step 3: Add 4 different products to cart
        print("\n" + "-" * 70)
        print("ADDING 4 PRODUCTS TO CART")
        print("-" * 70)

        self.add_nth_product_to_cart(1, continue_shopping=True)
        self.add_nth_product_to_cart(2, continue_shopping=True)
        self.add_nth_product_to_cart(3, continue_shopping=True)
        self.add_nth_product_to_cart(4, continue_shopping=False)

        print(f"\n✅ Step 3: Added {len(self.added_products)} products to cart")

        # Step 4: Go to cart page
        self.view_cart()
        print("✅ Step 4: On cart page")

        # Verify initial cart state
        initial_products = self.get_cart_products()
        print(f"\nInitial cart contents ({len(initial_products)} items):")
        for i, product in enumerate(initial_products, 1):
            print(f"  {i}. {product}")

        assert len(initial_products) == 4, f"Expected 4 products, found {len(initial_products)}"

        # Steps 5-8: Remove all products one by one
        print("\n" + "=" * 70)
        print("REMOVING PRODUCTS ONE BY ONE")
        print("=" * 70)

        # Step 5: Remove first product
        print("\n--- Removal 1 ---")
        self.remove_first_product()
        remaining = self.get_cart_products()
        print(f"Remaining products: {len(remaining)}")
        print("✅ Step 5: Removed first product")

        # Step 6: Remove second product (which is now first)
        if len(remaining) > 0:
            print("\n--- Removal 2 ---")
            self.remove_first_product()
            remaining = self.get_cart_products()
            print(f"Remaining products: {len(remaining)}")
            print("✅ Step 6: Removed second product")

        # Step 7: Remove third product (which is now first)
        if len(remaining) > 0:
            print("\n--- Removal 3 ---")
            self.remove_first_product()
            remaining = self.get_cart_products()
            print(f"Remaining products: {len(remaining)}")
            print("✅ Step 7: Removed third product")

        # Step 8: Remove fourth product (which is now first)
        if len(remaining) > 0:
            print("\n--- Removal 4 ---")
            self.remove_first_product()
            remaining = self.get_cart_products()
            print(f"Remaining products: {len(remaining)}")
            print("✅ Step 8: Removed fourth product")

        # Step 9: Observe cart page content
        print("\n" + "=" * 70)
        print("OBSERVING CART PAGE CONTENT")
        print("=" * 70)

        self.page.wait_for_timeout(1000)

        # Step 10: Check if any products remain
        final_products = self.get_cart_products()
        is_empty, message = self.check_cart_empty_message()

        print(f"\nFinal cart state:")
        print(f"  Products in cart: {len(final_products)}")
        print(f"  Cart empty: {is_empty}")
        print(f"  Message: {message}")

        if len(final_products) > 0:
            print("\n⚠️ Products still in cart:")
            for i, product in enumerate(final_products, 1):
                print(f"  {i}. {product}")

        print("✅ Step 9-10: Observed cart page and checked for remaining products")

        # Final verification
        print("\n" + "=" * 70)
        if len(final_products) == 0:
            print("✅ TEST PASSED: All products successfully removed from cart!")
            print("   Cart is now empty.")
        else:
            print(f"⚠️ TEST COMPLETED: {len(final_products)} product(s) still in cart")
            print("   (This may be expected behavior - empty cart may show differently)")
        print("=" * 70 + "\n")

        # Assertion - cart should be empty
        assert len(final_products) == 0, f"Cart should be empty but contains {len(final_products)} product(s)"


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