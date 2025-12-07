import pytest
from playwright.sync_api import Page, expect


class TestRemoveSpecificProduct:
    """Test suite for removing a specific product from cart"""

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

    def add_product_to_cart_by_name(self, product_name, continue_shopping=True):
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

        self.added_products.append(product_name)

    def view_cart(self):
        """Navigate to cart page"""
        print("\n🛒 Viewing cart...")
        view_cart_link = self.page.locator('a:has-text("View Cart")').first
        view_cart_link.click()
        expect(self.page).to_have_url(f"{self.base_url}/view_cart")
        print("✅ On cart page")

    def get_cart_products_detailed(self):
        """Get detailed information about products in cart"""
        cart_rows = self.page.locator('#cart_info_table tbody tr').all()

        products = []
        for row in cart_rows:
            try:
                product_name = row.locator('.cart_description h4 a').inner_text()
                quantity = row.locator('.cart_quantity button').inner_text()
                price = row.locator('.cart_price p').inner_text()
                total = row.locator('.cart_total_price').inner_text()

                products.append({
                    'name': product_name,
                    'quantity': quantity,
                    'price': price,
                    'total': total,
                    'row': row
                })
            except:
                pass

        return products

    def locate_product_row(self, product_name):
        """Locate a specific product row in the cart table"""
        print(f"\n🔍 Locating '{product_name}' row in cart table...")

        # Find the row containing the specific product
        product_row = self.page.locator(
            f'#cart_info_table tbody tr:has(.cart_description h4 a:text-is("{product_name}"))'
        ).first

        # Check if row exists
        if product_row.count() > 0:
            print(f"✅ Found '{product_name}' row")
            return product_row
        else:
            print(f"❌ '{product_name}' row not found")
            return None

    def remove_product_by_name(self, product_name):
        """Remove a specific product from cart by clicking its X button"""
        print(f"\n🗑️ Removing '{product_name}' from cart...")

        # Find the row containing the product
        product_row = self.page.locator(
            f'#cart_info_table tbody tr:has(.cart_description h4 a:text-is("{product_name}"))'
        ).first

        # Locate the orange X button in the delete column (far right)
        delete_btn = product_row.locator('.cart_delete a.cart_quantity_delete').first

        print(f"🎯 Found orange X button for '{product_name}' in Total column")

        # Click the X button
        delete_btn.click()

        # Wait for page to reload
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(1000)

        print(f"✅ Clicked X button - '{product_name}' removed")

    def verify_product_removed(self, product_name):
        """Verify that a product is no longer in the cart"""
        print(f"\n🔎 Checking if '{product_name}' is removed...")

        # Try to find the product row
        product_row = self.page.locator(
            f'#cart_info_table tbody tr:has(.cart_description h4 a:text-is("{product_name}"))'
        )

        if product_row.count() == 0:
            print(f"✅ Confirmed: '{product_name}' row is removed from cart")
            return True
        else:
            print(f"❌ Warning: '{product_name}' row still exists in cart")
            return False

    def test_remove_men_tshirt_from_cart(self):
        """
        Test Case: Add multiple products and remove Men Tshirt specifically - 06

        Steps:
        1. Open browser
        2. Go to http://automationexercise.com
        3. Add multiple products to cart (Blue Top, Men Tshirt, Sleeveless Dress)
        4. Navigate to cart page by clicking View Cart
        5. Locate Men Tshirt row in cart table
        6. Find the orange X button on the far right of Total column for Men Tshirt
        7. Click on the X button
        8. Check if Men Tshirt row is removed
        9. Count remaining products in cart
        """

        print("\n" + "=" * 70)
        print("TEST: Remove Specific Product (Men Tshirt) from Cart")
        print("=" * 70)

        # Step 1 & 2: Open browser and navigate to website
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Step 1-2: Opened http://automationexercise.com")

        # Navigate to products page
        self.go_to_products_page()

        # Step 3: Add multiple products to cart
        print("\n" + "-" * 70)
        print("ADDING PRODUCTS TO CART")
        print("-" * 70)

        self.add_product_to_cart_by_name("Blue Top", continue_shopping=True)
        self.add_product_to_cart_by_name("Men Tshirt", continue_shopping=True)
        self.add_product_to_cart_by_name("Sleeveless Dress", continue_shopping=False)

        print(f"\n✅ Step 3: Added {len(self.added_products)} products:")
        for i, product in enumerate(self.added_products, 1):
            print(f"   {i}. {product}")

        # Step 4: Navigate to cart page
        self.view_cart()
        print("✅ Step 4: On cart page")

        # Display initial cart state
        print("\n" + "-" * 70)
        print("INITIAL CART STATE")
        print("-" * 70)

        initial_products = self.get_cart_products_detailed()
        print(f"Total products in cart: {len(initial_products)}")

        for i, product in enumerate(initial_products, 1):
            print(f"{i}. {product['name']}")
            print(f"   Price: {product['price']} | Quantity: {product['quantity']} | Total: {product['total']}")

        assert len(initial_products) == 3, f"Expected 3 products, found {len(initial_products)}"

        # Step 5: Locate Men Tshirt row
        men_tshirt_row = self.locate_product_row("Men Tshirt")
        assert men_tshirt_row is not None, "Men Tshirt row not found in cart"
        print("✅ Step 5: Located Men Tshirt row in cart table")

        # Step 6: Find the orange X button
        print("✅ Step 6: Found orange X button in Total column for Men Tshirt")

        # Step 7: Click the X button
        self.remove_product_by_name("Men Tshirt")
        print("✅ Step 7: Clicked X button")

        # Step 8: Check if Men Tshirt row is removed
        is_removed = self.verify_product_removed("Men Tshirt")
        assert is_removed, "Men Tshirt was not removed from cart"
        print("✅ Step 8: Men Tshirt row is removed")

        # Step 9: Count remaining products in cart
        print("\n" + "-" * 70)
        print("FINAL CART STATE")
        print("-" * 70)

        final_products = self.get_cart_products_detailed()
        print(f"Total products remaining: {len(final_products)}")

        for i, product in enumerate(final_products, 1):
            print(f"{i}. {product['name']}")
            print(f"   Price: {product['price']} | Quantity: {product['quantity']} | Total: {product['total']}")

        print("✅ Step 9: Counted remaining products")

        # Verify final state
        assert len(final_products) == 2, f"Expected 2 products, found {len(final_products)}"

        final_product_names = [p['name'] for p in final_products]
        assert "Blue Top" in final_product_names, "Blue Top should still be in cart"
        assert "Sleeveless Dress" in final_product_names, "Sleeveless Dress should still be in cart"
        assert "Men Tshirt" not in final_product_names, "Men Tshirt should be removed"

        print("\n" + "=" * 70)
        print("✅ TEST PASSED: Men Tshirt successfully removed!")
        print(f"   Initial products: {len(initial_products)}")
        print(f"   Final products: {len(final_products)}")
        print("   Remaining: Blue Top, Sleeveless Dress")
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