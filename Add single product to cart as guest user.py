import pytest
from playwright.sync_api import Page, expect


class TestAddToCartModal:
    """Test suite for verifying add to cart modal behavior"""

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
                print("✅ Cookie consent accepted")
        except:
            pass

    def test_add_to_cart_modal_verification(self):
        """
        Test Case: Verify Add to Cart Modal and Its Elements - 01

        Steps:
        1. Open Chrome browser
        2. Enter URL http://automationexercise.com in address bar
        3. Press Enter key
        4. Click on Products link in top navigation menu
        5. Scroll down to find Blue Top product
        6. Hover mouse over Blue Top product image
        7. Click on Add to cart button
        8. Observe the popup modal that appears
        9. Read the success message displayed
        10. Check if View Cart and Continue Shopping buttons are visible
        """

        print("\n" + "=" * 70)
        print("TEST: Add to Cart Modal Verification")
        print("=" * 70)

        # Step 1-3: Open browser, enter URL, and press Enter
        print("\n🌐 Opening Chrome browser and navigating to website...")
        self.page.goto(self.base_url)

        # Verify page loaded
        expect(self.page).to_have_title("Automation Exercise")
        print("✅ Step 1-3: Opened http://automationexercise.com")

        # Handle cookie consent
        self.handle_cookie_consent()

        # Step 4: Click on Products link in top navigation menu
        print("\n📄 Clicking on Products link...")
        products_link = self.page.locator('a[href="/products"]').first
        products_link.click()

        # Wait for products page to load
        self.page.wait_for_selector('.features_items')
        expect(self.page).to_have_url(f"{self.base_url}/products")
        print("✅ Step 4: Clicked Products link in top navigation")

        # Step 5: Scroll down to find Blue Top product
        print("\n🔍 Scrolling to find Blue Top product...")

        # Find Blue Top product
        blue_top_product = self.page.locator('.single-products:has(.productinfo p:text-is("Blue Top"))').first

        # Scroll the product into view
        blue_top_product.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        # Verify Blue Top is visible
        expect(blue_top_product).to_be_visible()
        print("✅ Step 5: Found and scrolled to Blue Top product")

        # Step 6: Hover mouse over Blue Top product image
        print("\n🖱️ Hovering over Blue Top product...")
        blue_top_product.hover()
        self.page.wait_for_timeout(1000)  # Wait for overlay to appear
        print("✅ Step 6: Hovered mouse over Blue Top product image")

        # Step 7: Click on Add to cart button
        print("\n🛒 Clicking Add to cart button...")
        add_to_cart_btn = blue_top_product.locator('.overlay-content .add-to-cart').first

        # Verify button is visible after hover
        expect(add_to_cart_btn).to_be_visible()

        add_to_cart_btn.click()
        print("✅ Step 7: Clicked Add to cart button")

        # Step 8: Observe the popup modal that appears
        print("\n📋 Observing popup modal...")

        # Wait for modal to appear
        modal = self.page.locator('#cartModal')
        expect(modal).to_be_visible(timeout=5000)

        # Wait for modal animation to complete
        self.page.wait_for_timeout(1000)

        print("✅ Step 8: Popup modal appeared")

        # Step 9: Read the success message displayed
        print("\n✉️ Reading success message...")

        # Locate the success message in the modal
        success_message = self.page.locator('#cartModal .modal-body p').first

        # Get the message text
        message_text = success_message.inner_text()

        print(f"📝 Success message: '{message_text}'")
        print("✅ Step 9: Success message read successfully")

        # Verify the message content
        assert "added" in message_text.lower(), f"Expected 'added' in message, got: {message_text}"

        # Step 10: Check if View Cart and Continue Shopping buttons are visible
        print("\n🔘 Checking for buttons in modal...")

        # Locate View Cart button
        view_cart_button = self.page.locator('#cartModal a:has-text("View Cart")')

        # Locate Continue Shopping button
        continue_shopping_button = self.page.locator('#cartModal button:has-text("Continue Shopping")')

        # Verify both buttons are visible
        print("\n📊 Button Visibility Check:")

        if view_cart_button.is_visible():
            print("   ✅ View Cart button is VISIBLE")
        else:
            print("   ❌ View Cart button is NOT visible")

        if continue_shopping_button.is_visible():
            print("   ✅ Continue Shopping button is VISIBLE")
        else:
            print("   ❌ Continue Shopping button is NOT visible")

        # Assertions
        expect(view_cart_button).to_be_visible()
        expect(continue_shopping_button).to_be_visible()

        print("\n✅ Step 10: Both View Cart and Continue Shopping buttons are visible")

        # Additional verification - get button texts
        view_cart_text = view_cart_button.inner_text()
        continue_shopping_text = continue_shopping_button.inner_text()

        print("\n" + "-" * 70)
        print("MODAL CONTENT SUMMARY")
        print("-" * 70)
        print(f"Success Message: {message_text}")
        print(f"View Cart Button: '{view_cart_text}' (Visible: ✓)")
        print(f"Continue Shopping Button: '{continue_shopping_text}' (Visible: ✓)")
        print("-" * 70)

        # Take a moment to observe the modal
        print("\n⏸️ Pausing to observe modal (2 seconds)...")
        self.page.wait_for_timeout(2000)

        print("\n" + "=" * 70)
        print("✅ TEST PASSED: Add to Cart Modal Verified Successfully!")
        print("   - Product added to cart")
        print("   - Success message displayed")
        print("   - View Cart button visible")
        print("   - Continue Shopping button visible")
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