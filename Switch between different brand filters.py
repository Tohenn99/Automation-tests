import pytest
from playwright.sync_api import Page, expect


class TestBrandFilters:
    """Test suite for testing brand filter functionality"""

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

    def get_brand_heading(self):
        """Get the current brand heading from the page"""
        try:
            heading = self.page.locator('.features_items h2.title').first
            if heading.is_visible(timeout=3000):
                return heading.inner_text()
            return None
        except:
            return None

    def count_products(self):
        """Count the number of products displayed"""
        products = self.page.locator('.single-products').all()
        return len(products)

    def test_brand_filter_navigation(self):
        """
        Test Case: Filter products by different brands - 25

        Steps:
        1. Open browser
        2. Go to http://automationexercise.com
        3. Click Products
        4. Click on POLO (6) brand
        5. Observe POLO products load
        6. Note the product count and heading
        7. Click on MADAME (5) brand from sidebar
        8. Observe page changes to MADAME products
        9. Note the new product count and heading
        10. Click on BIBA (5) brand
        11. Observe page changes to BIBA products
        12. Check if each filter worked correctly
        """

        print("\n" + "=" * 70)
        print("TEST: Brand Filter Navigation")
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

        self.page.wait_for_selector('.features_items')
        expect(self.page).to_have_url(f"{self.base_url}/products")
        print("✅ Step 3: Clicked Products - On products page")

        # Scroll to brands section to ensure it's visible
        brands_section = self.page.locator('.brands_products')
        brands_section.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        # Step 4: Click on POLO (6) brand
        print("\n" + "=" * 70)
        print("FILTERING BY POLO BRAND")
        print("=" * 70)

        polo_link = self.page.locator('.brands-name a:has-text("Polo")')
        expect(polo_link).to_be_visible()

        polo_text = polo_link.inner_text()
        print(f"🔗 Clicking: '{polo_text}'")

        polo_link.click()

        # Wait for page to update
        self.page.wait_for_selector('.features_items')
        self.page.wait_for_timeout(1000)
        print("✅ Step 4: Clicked on POLO brand")

        # Step 5 & 6: Observe POLO products and note count/heading
        print("\n📊 Observing POLO products...")

        polo_heading = self.get_brand_heading()
        polo_count = self.count_products()

        print(f"   Heading: {polo_heading}")
        print(f"   Product count: {polo_count}")

        # Verify we're on POLO brand page
        assert "polo" in polo_heading.lower() if polo_heading else False, \
            f"Expected POLO in heading, got: {polo_heading}"

        print("✅ Step 5-6: POLO products loaded and counted")

        # Step 7: Click on MADAME (5) brand from sidebar
        print("\n" + "=" * 70)
        print("FILTERING BY MADAME BRAND")
        print("=" * 70)

        madame_link = self.page.locator('.brands-name a:has-text("Madame")')
        expect(madame_link).to_be_visible()

        madame_text = madame_link.inner_text()
        print(f"🔗 Clicking: '{madame_text}'")

        madame_link.click()

        # Wait for page to update
        self.page.wait_for_selector('.features_items')
        self.page.wait_for_timeout(1000)
        print("✅ Step 7: Clicked on MADAME brand from sidebar")

        # Step 8 & 9: Observe page changes to MADAME products
        print("\n📊 Observing MADAME products...")

        madame_heading = self.get_brand_heading()
        madame_count = self.count_products()

        print(f"   Heading: {madame_heading}")
        print(f"   Product count: {madame_count}")

        # Verify we're on MADAME brand page
        assert "madame" in madame_heading.lower() if madame_heading else False, \
            f"Expected MADAME in heading, got: {madame_heading}"

        # Verify products changed
        assert madame_heading != polo_heading, \
            "Page heading should change from POLO to MADAME"

        print("✅ Step 8-9: Page changed to MADAME products")

        # Step 10: Click on BIBA (5) brand
        print("\n" + "=" * 70)
        print("FILTERING BY BIBA BRAND")
        print("=" * 70)

        biba_link = self.page.locator('.brands-name a:has-text("Biba")')
        expect(biba_link).to_be_visible()

        biba_text = biba_link.inner_text()
        print(f"🔗 Clicking: '{biba_text}'")

        biba_link.click()

        # Wait for page to update
        self.page.wait_for_selector('.features_items')
        self.page.wait_for_timeout(1000)
        print("✅ Step 10: Clicked on BIBA brand")

        # Step 11: Observe page changes to BIBA products
        print("\n📊 Observing BIBA products...")

        biba_heading = self.get_brand_heading()
        biba_count = self.count_products()

        print(f"   Heading: {biba_heading}")
        print(f"   Product count: {biba_count}")

        # Verify we're on BIBA brand page
        assert "biba" in biba_heading.lower() if biba_heading else False, \
            f"Expected BIBA in heading, got: {biba_heading}"

        # Verify products changed
        assert biba_heading != madame_heading, \
            "Page heading should change from MADAME to BIBA"

        print("✅ Step 11: Page changed to BIBA products")

        # Step 12: Check if each filter worked correctly
        print("\n" + "=" * 70)
        print("FILTER VERIFICATION - Step 12")
        print("=" * 70)

        print("\n✓ Filter Results Summary:")
        print(f"   1. POLO: {polo_count} products - Heading: '{polo_heading}'")
        print(f"   2. MADAME: {madame_count} products - Heading: '{madame_heading}'")
        print(f"   3. BIBA: {biba_count} products - Heading: '{biba_heading}'")

        # Verify all filters worked
        filters_passed = True

        # Check POLO filter
        if "polo" in polo_heading.lower() and polo_count > 0:
            print("\n   ✅ POLO filter: PASSED")
        else:
            print("\n   ❌ POLO filter: FAILED")
            filters_passed = False

        # Check MADAME filter
        if "madame" in madame_heading.lower() and madame_count > 0:
            print("   ✅ MADAME filter: PASSED")
        else:
            print("   ❌ MADAME filter: FAILED")
            filters_passed = False

        # Check BIBA filter
        if "biba" in biba_heading.lower() and biba_count > 0:
            print("   ✅ BIBA filter: PASSED")
        else:
            print("   ❌ BIBA filter: FAILED")
            filters_passed = False

        # Check that headings are different
        all_different = (
                polo_heading != madame_heading and
                madame_heading != biba_heading and
                polo_heading != biba_heading
        )

        if all_different:
            print("   ✅ All brand pages are DIFFERENT")
        else:
            print("   ❌ Some brand pages are the SAME")
            filters_passed = False

        print("\n✅ Step 12: Filter verification completed")

        # Final assertions
        assert filters_passed, "All brand filters should work correctly"

        # Summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print("Brand Filter Tests:")
        print(f"   • POLO: {polo_count} products found")
        print(f"   • MADAME: {madame_count} products found")
        print(f"   • BIBA: {biba_count} products found")
        print("\nResult: All filters working correctly ✓")
        print("=" * 70)

        print("\n✅ TEST PASSED: All Brand Filters Work Correctly!\n")


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