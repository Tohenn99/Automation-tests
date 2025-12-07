import pytest
from playwright.sync_api import Page, expect


class TestSareeProductWithRemoval:
    """Test suite for adding saree product and managing cart"""

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

    def add_product_to_cart(self, product_name, continue_shopping=True):
        """Add a product to cart by name"""
        print(f"🛒 Adding '{product_name}' to cart...")

        product_container = self.page.locator(
            f'.single-products:has(.productinfo p:text-is("{product_name}"))'
        ).first

        product_container.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        product_container.hover()
        self.page.wait_for_timeout(500)

        add_to_cart_btn = product_container.locator('.overlay-content .add-to-cart').first
        add_to_cart_btn.click()

        self.page.wait_for_selector('#cartModal', state='visible')

        if continue_shopping:
            continue_btn = self.page.locator('button:has-text("Continue Shopping")')
            continue_btn.click()
            self.page.wait_for_selector('#cartModal', state='hidden')
            print(f"✅ Added '{product_name}' - Continued shopping")
        else:
            print(f"✅ Added '{product_name}'")

        self.added_products.append(product_name)

    def add_nth_product_to_cart(self, position, continue_shopping=True):
        """Add nth product from current page"""
        products = self.page.locator('.single-products').all()

        if position > len(products):
            raise Exception(f"Only {len(products)} products available")

        product = products[position - 1]
        product_name = product.locator('.productinfo p').first.inner_text()

        product.hover()
        self.page.wait_for_timeout(500)

        add_to_cart_btn = product.locator('.overlay-content .add-to-cart').first
        add_to_cart_btn.click()

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

    def remove_first_product(self):
        """Remove the first product from cart"""
        first_row = self.page.locator('#cart_info_table tbody tr').first

        try:
            product_name = first_row.locator('.cart_description h4 a').inner_text()
        except:
            product_name = "Unknown"

        print(f"🗑️ Removing: '{product_name}'")

        delete_btn = first_row.locator('.cart_delete a.cart_quantity_delete').first
        delete_btn.click()

        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(1000)

        print(f"✅ Removed '{product_name}'")
        return product_name

    def get_cart_products(self):
        """Get all products in cart"""
        cart_rows = self.page.locator('#cart_info_table tbody tr').all()
        products = []

        for row in cart_rows:
            try:
                product_name = row.locator('.cart_description h4 a').inner_text()
                products.append(product_name)
            except:
                pass

        return products

    def test_saree_product_with_removal(self):
        """
        Test Case: Add saree product, add 3 more products, remove the 3, verify saree remains - 13

        Steps:
        - Open browser
        - Navigate to http://automationexercise.com
        - Click Products menu
        - Locate WOMEN in CATEGORY section
        - Click plus to expand WOMEN category
        - Click on Saree subcategory
        - Observe page heading WOMEN - SAREE PRODUCTS
        - Scroll through saree products
        - Find Beautiful Peacock Blue Cotton Linen Saree
        - Read price (Rs. 5000)
        - Click Add to cart button
        - Click Continue Shopping
        - Add 3 more products from any category
        - Click View Cart link
        - Check product details in cart
        - Remove all 3 additional products by clicking their X buttons
        - Verify the saree product remains in the cart
        """

        print("\n" + "=" * 70)
        print("TEST: Saree Product with Additional Products Removal")
        print("=" * 70)

        # Open browser and navigate
        print("\n🌐 Opening browser and navigating...")
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Opened http://automationexercise.com")

        # Click Products menu
        print("\n📄 Clicking Products menu...")
        products_link = self.page.locator('a[href="/products"]').first
        products_link.click()

        self.page.wait_for_selector('.features_items')
        expect(self.page).to_have_url(f"{self.base_url}/products")
        print("✅ Clicked Products menu")

        # Locate WOMEN in CATEGORY section
        print("\n🔍 Locating WOMEN category...")
        women_category = self.page.locator('.panel-heading a[href="#Women"]').first
        women_category.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        expect(women_category).to_be_visible()
        print("✅ Located WOMEN in CATEGORY section")

        # Click plus to expand WOMEN category
        print("\n➕ Expanding WOMEN category...")
        women_category.click()
        self.page.wait_for_timeout(500)
        print("✅ Expanded WOMEN category")

        # Click on Saree subcategory
        print("\n🔗 Clicking Saree subcategory...")
        saree_link = self.page.locator('#Women a:has-text("Saree")').first
        expect(saree_link).to_be_visible()
        saree_link.click()

        self.page.wait_for_selector('.features_items')
        self.page.wait_for_timeout(1000)
        print("✅ Clicked Saree subcategory")

        # Observe page heading
        print("\n📋 Observing page heading...")
        heading = self.page.locator('.features_items h2.title').first
        heading_text = heading.inner_text()

        print(f"   Heading: {heading_text}")

        assert "women" in heading_text.lower() and "saree" in heading_text.lower(), \
            f"Expected 'WOMEN - SAREE PRODUCTS' in heading, got: {heading_text}"

        print("✅ Page heading verified: WOMEN - SAREE PRODUCTS")

        # Scroll through saree products
        print("\n📜 Scrolling through saree products...")
        products_section = self.page.locator('.features_items')
        products_section.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        print("✅ Scrolled through saree products")

        # Find Beautiful Peacock Blue Cotton Linen Saree
        print("\n🔍 Finding Beautiful Peacock Blue Cotton Linen Saree...")

        saree_name = "Beautiful Peacock Blue Cotton Linen Saree"
        saree_product = self.page.locator(
            f'.single-products:has(.productinfo p:text-is("{saree_name}"))'
        ).first

        saree_product.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        expect(saree_product).to_be_visible()
        print(f"✅ Found '{saree_name}'")

        # Read price
        print("\n💰 Reading price...")
        price_element = saree_product.locator('.productinfo h2')
        saree_price = price_element.inner_text()

        print(f"   Price: {saree_price}")

        assert "Rs. 5000" in saree_price or "5000" in saree_price, \
            f"Expected price Rs. 5000, found {saree_price}"

        print("✅ Price verified: Rs. 5000")

        # Add to cart
        print("\n🛒 Adding saree to cart...")
        self.add_product_to_cart(saree_name, continue_shopping=True)

        # Add 3 more products from any category
        print("\n" + "=" * 70)
        print("ADDING 3 MORE PRODUCTS")
        print("=" * 70)

        # Go back to all products
        products_link = self.page.locator('a[href="/products"]').first
        products_link.click()
        self.page.wait_for_selector('.features_items')
        self.page.wait_for_timeout(1000)

        print("\n📦 Adding 3 additional products...")
        self.add_nth_product_to_cart(1, continue_shopping=True)
        self.add_nth_product_to_cart(2, continue_shopping=True)
        self.add_nth_product_to_cart(3, continue_shopping=False)

        print(f"\n✅ Added 3 more products (Total: {len(self.added_products)} products)")

        # Click View Cart link
        print("\n🛒 Clicking View Cart...")
        view_cart_link = self.page.locator('a:has-text("View Cart")').first
        view_cart_link.click()

        expect(self.page).to_have_url(f"{self.base_url}/view_cart")
        self.page.wait_for_timeout(1000)
        print("✅ Navigated to cart page")

        # Check product details in cart
        print("\n" + "-" * 70)
        print("INITIAL CART STATE")
        print("-" * 70)

        initial_products = self.get_cart_products()
        print(f"Total products in cart: {len(initial_products)}")

        for i, product in enumerate(initial_products, 1):
            marker = "🎯" if product == saree_name else "  "
            print(f"{marker} {i}. {product}")

        assert len(initial_products) == 4, f"Expected 4 products, found {len(initial_products)}"
        assert saree_name in initial_products, f"Saree should be in cart"

        # Remove all 3 additional products
        print("\n" + "=" * 70)
        print("REMOVING 3 ADDITIONAL PRODUCTS")
        print("=" * 70)

        removed_products = []

        for i in range(3):
            print(f"\n--- Removal {i + 1} ---")

            # Get current products before removal
            current_products = self.get_cart_products()

            # Find first product that is NOT the saree
            product_to_remove = None
            for product in current_products:
                if product != saree_name:
                    product_to_remove = product
                    break

            if product_to_remove:
                # Find and click X button for this specific product
                product_row = self.page.locator(
                    f'#cart_info_table tbody tr:has(.cart_description h4 a:text-is("{product_to_remove}"))'
                ).first

                print(f"🗑️ Removing: '{product_to_remove}'")

                delete_btn = product_row.locator('.cart_delete a.cart_quantity_delete').first
                delete_btn.click()

                self.page.wait_for_load_state('networkidle')
                self.page.wait_for_timeout(1000)

                removed_products.append(product_to_remove)
                print(f"✅ Removed '{product_to_remove}'")

                remaining = self.get_cart_products()
                print(f"Remaining products: {len(remaining)}")

        print(f"\n✅ Removed {len(removed_products)} products")

        # Verify the saree product remains
        print("\n" + "=" * 70)
        print("FINAL VERIFICATION")
        print("=" * 70)

        final_products = self.get_cart_products()

        print(f"\nFinal cart contents ({len(final_products)} product(s)):")
        for i, product in enumerate(final_products, 1):
            print(f"   ✅ {i}. {product}")

        # Assertions
        assert len(final_products) == 1, \
            f"Expected 1 product in cart, found {len(final_products)}"

        assert saree_name in final_products, \
            f"Saree '{saree_name}' should remain in cart"

        assert final_products[0] == saree_name, \
            f"Only the saree should remain, found: {final_products[0]}"

        print(f"\n✅ VERIFIED: '{saree_name}' remains in cart")
        print(f"✅ All 3 additional products successfully removed")

        # Summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Saree Product: {saree_name}")
        print(f"Price: {saree_price}")
        print(f"\nProducts added: {len(self.added_products)}")
        print(f"Products removed: {len(removed_products)}")
        print(f"Products remaining: {len(final_products)}")
        print("\nResult: ✅ Saree product remains in cart after removals")
        print("=" * 70)

        print("\n✅ TEST PASSED: Saree Product Verified in Cart!\n")


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
    pytest.main([__file__, "-v", "-s", "--headed"])