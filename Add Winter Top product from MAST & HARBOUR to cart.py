import pytest
from playwright.sync_api import Page, expect


class TestWinterTopToCart:
    """Test suite for adding Winter Top from MAST & HARBOUR to cart"""

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

    def test_add_winter_top_to_cart(self):
        """
        Test Case: Add Winter Top from MAST & HARBOUR to cart - 42

        Steps:
        1. Open browser
        2. Go to http://automationexercise.com
        3. Click Products
        4. Scroll to BRANDS section
        5. Click MAST & HARBOUR (3) brand link
        6. Locate Winter Top product
        7. Check price is Rs. 600
        8. Hover over product image
        9. Click Add to cart button
        10. Read success message
        11. Click View Cart
        12. Check if Winter Top appears in cart
        """

        print("\n" + "=" * 70)
        print("TEST: Add Winter Top from MAST & HARBOUR to Cart")
        print("=" * 70)

        # Step 1 & 2: Open browser and navigate to website
        print("\n🌐 Opening browser and navigating to website...")
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Step 1-2: Opened http://automationexercise.com")

        # Step 3: Click Products
        print("\n📄 Clicking Products...")
        products_link = self.page.locator('a[href="/products"]').first
        products_link.click()

        # Wait for products page to load
        self.page.wait_for_selector('.features_items')
        expect(self.page).to_have_url(f"{self.base_url}/products")
        print("✅ Step 3: Clicked Products")

        # Step 4: Scroll to BRANDS section
        print("\n🏷️ Scrolling to BRANDS section...")
        brands_section = self.page.locator('.brands_products')
        brands_section.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        expect(brands_section).to_be_visible()
        print("✅ Step 4: Scrolled to BRANDS section")

        # Step 5: Click MAST & HARBOUR brand link
        print("\n🔗 Clicking MAST & HARBOUR brand link...")
        mast_harbour_link = self.page.locator('.brands-name a:has-text("Mast & Harbour")')

        expect(mast_harbour_link).to_be_visible()

        # Get the link text with count
        brand_text = mast_harbour_link.inner_text()
        print(f"   Clicking: '{brand_text}'")

        mast_harbour_link.click()

        # Wait for brand products to load
        self.page.wait_for_selector('.features_items')
        self.page.wait_for_timeout(1000)
        print("✅ Step 5: Clicked MAST & HARBOUR brand link")

        # Step 6: Locate Winter Top product
        print("\n🔍 Locating Winter Top product...")

        product_name = "Winter Top"
        product_container = self.page.locator(f'.single-products:has(.productinfo p:text-is("{product_name}"))').first

        # Scroll product into view
        product_container.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        expect(product_container).to_be_visible()
        print(f"✅ Step 6: Located '{product_name}' product")

        # Step 7: Check price is Rs. 600
        print("\n💰 Checking product price...")

        price_element = product_container.locator('.productinfo h2')
        product_price = price_element.inner_text()

        print(f"   Product: {product_name}")
        print(f"   Price: {product_price}")

        # Verify the price
        assert "Rs. 600" in product_price or "600" in product_price, \
            f"Expected price Rs. 600, found {product_price}"

        print("✅ Step 7: Price verified as Rs. 600")

        # Step 8: Hover over product image
        print("\n🖱️ Hovering over product image...")
        product_container.hover()
        self.page.wait_for_timeout(1000)
        print("✅ Step 8: Hovered over product image")

        # Step 9: Click Add to cart button
        print("\n🛒 Clicking Add to cart button...")

        add_to_cart_btn = product_container.locator('.overlay-content .add-to-cart').first
        expect(add_to_cart_btn).to_be_visible()
        add_to_cart_btn.click()

        # Wait for modal to appear
        self.page.wait_for_selector('#cartModal', state='visible')
        print("✅ Step 9: Clicked Add to cart button")

        # Step 10: Read success message
        print("\n📨 Reading success message...")

        success_message_element = self.page.locator('#cartModal .modal-body p').first
        success_message = success_message_element.inner_text()

        print(f"   Success message: '{success_message}'")

        # Verify message contains expected text
        assert "added" in success_message.lower(), \
            f"Expected 'added' in message, got: {success_message}"

        print("✅ Step 10: Success message read")

        # Step 11: Click View Cart
        print("\n🛒 Clicking View Cart...")

        view_cart_btn = self.page.locator('#cartModal a:has-text("View Cart")')
        expect(view_cart_btn).to_be_visible()
        view_cart_btn.click()

        # Wait for cart page to load
        expect(self.page).to_have_url(f"{self.base_url}/view_cart")
        self.page.wait_for_timeout(1000)
        print("✅ Step 11: Clicked View Cart and navigated to cart page")

        # Step 12: Check if Winter Top appears in cart
        print("\n" + "-" * 70)
        print("CART VERIFICATION - Step 12")
        print("-" * 70)

        cart_product_row = self.page.locator(
            f'#cart_info_table tbody tr:has(.cart_description h4 a:text-is("{product_name}"))'
        )

        if cart_product_row.count() > 0:
            print(f"✅ '{product_name}' FOUND in cart!")

            # Get detailed cart information
            try:
                cart_product_name = cart_product_row.locator('.cart_description h4 a').inner_text()
                cart_price = cart_product_row.locator('.cart_price p').inner_text()
                cart_quantity = cart_product_row.locator('.cart_quantity button').inner_text()
                cart_total = cart_product_row.locator('.cart_total_price').inner_text()

                print(f"\n   Product Details in Cart:")
                print(f"   • Name: {cart_product_name}")
                print(f"   • Price: {cart_price}")
                print(f"   • Quantity: {cart_quantity}")
                print(f"   • Total: {cart_total}")
            except Exception as e:
                print(f"   ⚠️ Could not read all cart details: {str(e)}")
        else:
            print(f"❌ '{product_name}' NOT FOUND in cart!")

        print("\n✅ Step 12: Verified Winter Top appears in cart")

        # Final assertion
        assert cart_product_row.count() > 0, \
            f"Product '{product_name}' should be present in cart"

        # Summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print("Brand: MAST & HARBOUR")
        print(f"Product: {product_name}")
        print(f"Price: {product_price}")
        print(f"Success Message: {success_message}")
        print("Status: ✅ Product successfully added to cart")
        print("=" * 70)

        print("\n✅ TEST PASSED: Winter Top Successfully Added and Verified!\n")


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