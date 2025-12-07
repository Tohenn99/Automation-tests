import pytest
from playwright.sync_api import Page, expect


class TestBrandProductToCart:
    """Test suite for adding specific brand product to cart"""

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

    def test_add_brand_product_to_cart(self):
        """
        Test Case: Add MAST & HARBOUR product to cart - 43

        Steps:
        1. Open Chrome browser
        2. Navigate to http://automationexercise.com
        3. Click Products menu
        4. Scroll to BRANDS section in sidebar
        5. Click MAST & HARBOUR (3) link
        6. Find GRAPHIC DESIGN MEN T SHIRT - BLUE product
        7. Read product price (Rs. 1389)
        8. Click Add to cart button
        9. Click Continue Shopping
        10. Navigate to Cart using Cart menu
        """

        print("\n" + "=" * 70)
        print("TEST: Add MAST & HARBOUR Product to Cart")
        print("=" * 70)

        # Step 1 & 2: Open browser and navigate to website
        print("\n🌐 Opening browser and navigating...")
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Step 1-2: Opened http://automationexercise.com")

        # Step 3: Click Products menu
        print("\n📄 Clicking Products menu...")
        products_link = self.page.locator('a[href="/products"]').first
        products_link.click()

        # Wait for products page to load
        self.page.wait_for_selector('.features_items')
        expect(self.page).to_have_url(f"{self.base_url}/products")
        print("✅ Step 3: Clicked Products menu")

        # Step 4: Scroll to BRANDS section in sidebar
        print("\n🏷️ Scrolling to BRANDS section...")
        brands_section = self.page.locator('.brands_products')
        brands_section.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        # Verify brands section is visible
        expect(brands_section).to_be_visible()
        print("✅ Step 4: Scrolled to BRANDS section in sidebar")

        # Step 5: Click MAST & HARBOUR link
        print("\n🔗 Clicking MAST & HARBOUR brand...")
        mast_harbour_link = self.page.locator('.brands-name a:has-text("Mast & Harbour")')

        # Verify link is visible
        expect(mast_harbour_link).to_be_visible()

        # Get the full text to see the count
        brand_text = mast_harbour_link.inner_text()
        print(f"   Brand link text: '{brand_text}'")

        mast_harbour_link.click()

        # Wait for brand products to load
        self.page.wait_for_selector('.features_items')
        self.page.wait_for_timeout(1000)
        print("✅ Step 5: Clicked MAST & HARBOUR link")

        # Step 6: Find GRAPHIC DESIGN MEN T SHIRT - BLUE product
        print("\n🔍 Finding GRAPHIC DESIGN MEN T SHIRT - BLUE product...")

        # Look for the specific product
        product_name = "GRAPHIC DESIGN MEN T SHIRT - BLUE"
        product_container = self.page.locator(f'.single-products:has(.productinfo p:text-is("{product_name}"))').first

        # Scroll product into view
        product_container.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        # Verify product is visible
        expect(product_container).to_be_visible()
        print(f"✅ Step 6: Found '{product_name}' product")

        # Step 7: Read product price
        print("\n💰 Reading product price...")

        # Get the price from the product
        price_element = product_container.locator('.productinfo h2')
        product_price = price_element.inner_text()

        print(f"   Product: {product_name}")
        print(f"   Price: {product_price}")
        print("✅ Step 7: Read product price")

        # Verify the price matches expected
        assert "Rs. 1389" in product_price or "1389" in product_price, \
            f"Expected price Rs. 1389, found {product_price}"
        print(f"   ✓ Price verified: {product_price}")

        # Step 8: Click Add to cart button
        print("\n🛒 Adding product to cart...")

        # Hover over product to reveal Add to cart button
        product_container.hover()
        self.page.wait_for_timeout(500)

        # Click Add to cart button
        add_to_cart_btn = product_container.locator('.overlay-content .add-to-cart').first
        expect(add_to_cart_btn).to_be_visible()
        add_to_cart_btn.click()

        # Wait for modal to appear
        self.page.wait_for_selector('#cartModal', state='visible')
        print("✅ Step 8: Clicked Add to cart button")
        print("   Modal appeared")

        # Step 9: Click Continue Shopping
        print("\n🔄 Clicking Continue Shopping...")
        continue_shopping_btn = self.page.locator('button:has-text("Continue Shopping")')
        expect(continue_shopping_btn).to_be_visible()
        continue_shopping_btn.click()

        # Wait for modal to disappear
        self.page.wait_for_selector('#cartModal', state='hidden')
        print("✅ Step 9: Clicked Continue Shopping")

        # Step 10: Navigate to Cart using Cart menu
        print("\n🛒 Navigating to Cart...")
        cart_link = self.page.locator('a[href="/view_cart"]').first
        cart_link.click()

        # Wait for cart page to load
        expect(self.page).to_have_url(f"{self.base_url}/view_cart")
        self.page.wait_for_timeout(1000)
        print("✅ Step 10: Navigated to Cart using Cart menu")

        # Verify product is in cart
        print("\n" + "-" * 70)
        print("CART VERIFICATION")
        print("-" * 70)

        cart_product = self.page.locator(
            f'#cart_info_table tbody tr:has(.cart_description h4 a:text-is("{product_name}"))')

        if cart_product.count() > 0:
            print(f"✅ Product found in cart: {product_name}")

            # Get cart price
            cart_price = cart_product.locator('.cart_price p').inner_text()
            print(f"   Price in cart: {cart_price}")

            # Get quantity
            cart_quantity = cart_product.locator('.cart_quantity button').inner_text()
            print(f"   Quantity: {cart_quantity}")

            # Get total
            cart_total = cart_product.locator('.cart_total_price').inner_text()
            print(f"   Total: {cart_total}")
        else:
            print(f"❌ Product NOT found in cart: {product_name}")

        # Final assertion
        assert cart_product.count() > 0, f"Product '{product_name}' should be in cart"

        print("\n" + "=" * 70)
        print("✅ TEST PASSED: Product Successfully Added to Cart!")
        print("   Brand: MAST & HARBOUR")
        print(f"   Product: {product_name}")
        print(f"   Price: {product_price}")
        print("   Status: In Cart ✓")
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
    pytest.main([__file__, "-v", "-s", "--headed"])