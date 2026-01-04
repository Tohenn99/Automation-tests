"""
E2E Test Case 10: Trending Items - Fast Fashion Flash Shopping

Scenario: Fashion blogger quickly purchases trending items from
top brands before they sell out, needs rush delivery

File: test_e2e_10_trending_flash.py
"""

import pytest
from playwright.sync_api import Page
from POM.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)


class TestTrendingFlashShopping:
    """Test Case 10: Trending Items - Fast Fashion Flash Shopping"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for test"""
        self.page = page
        self.login_page = LoginPage(page)
        self.registration_page = RegistrationPage(page)
        self.products_page = ProductsPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.payment_page = PaymentPage(page)

    def test_trending_items_flash_shopping(self):
        """
        Test Case 10: Trending Items - Fast Fashion Flash Shopping

        Scenario: Fashion blogger/influencer purchases trending items
        from multiple brands for content creation with rush delivery

        Steps:
        1. Register fashion-conscious user (New Zealand)
        2. Quick shop from trending brand: BIBA (2 items)
        3. Quick shop from trending brand: Madame (2 items)
        4. Add graphic design item: "GRAPHIC DESIGN MEN T SHIRT - BLUE"
        5. Add popular item from Women's Tops
        6. Speed checkout with 6 trending items
        7. Add urgent delivery note for content creation deadline
        8. Request unboxing-friendly packaging
        9. Express payment processing
        10. Verify successful rush order

        Expected: Fast-paced shopping for trending items with rush
        delivery and content creator-specific packaging
        """

        print("\n" + "=" * 80)
        print("TEST 10: Trending Items - Fast Fashion Flash Shopping")
        print("=" * 80)

        # Test Data - Fashion blogger from New Zealand
        user_data = {
            'name': 'Sophia Chen',
            'email': TestDataFactory.generate_email(),
            'title': 'Mrs',
            'password': 'Fashion@2024',
            'dob': {'day': '25', 'month': '8', 'year': '1995'},
            'address': {
                'first_name': 'Sophia',
                'last_name': 'Chen',
                'company': 'Style Influencer NZ',
                'address1': '567 Queen Street',
                'address2': 'Studio 3A',
                'country': 'New Zealand',
                'state': 'Auckland',
                'city': 'Auckland',
                'zipcode': '1010',
                'mobile': '0221234567'
            }
        }
        payment_data = TestDataFactory.get_payment_data()

        print(f"\n1. REGISTRATION - Fashion Blogger: {user_data['name']}")
        print("-" * 80)
        print(f"Profile: Fashion Content Creator")
        print(f"Purpose: Trending items for social media content")

        # Register user
        self.login_page.navigate()
        self.login_page.signup(user_data['name'], user_data['email'])

        self.registration_page.fill_account_info(
            user_data['title'],
            user_data['password'],
            user_data['dob']
        )
        self.registration_page.fill_address_info(user_data['address'])
        self.registration_page.submit_registration()
        self.registration_page.continue_after_registration()

        print("✅ Fashion blogger account registered")

        print(f"\n2. FLASH SHOPPING - Trending Brands")
        print("-" * 80)
        print("⚡ Speed shopping for viral content...")

        trending_items = []

        # Quick shop BIBA (trending brand)
        self.products_page.navigate()
        self.products_page.filter_by_brand("Biba")
        print("🔥 Shopping BIBA (Trending Brand)")

        biba1 = self.products_page.add_nth_product(1, continue_shopping=True)
        trending_items.append(f"BIBA: {biba1}")
        print(f"⚡ Added: {biba1}")

        biba2 = self.products_page.add_nth_product(2, continue_shopping=True)
        trending_items.append(f"BIBA: {biba2}")
        print(f"⚡ Added: {biba2}")

        # Quick shop Madame (trending brand)
        self.products_page.navigate()
        self.products_page.filter_by_brand("Madame")
        print("🔥 Shopping MADAME (Trending Brand)")

        madame1 = self.products_page.add_nth_product(1, continue_shopping=True)
        trending_items.append(f"MADAME: {madame1}")
        print(f"⚡ Added: {madame1}")

        madame2 = self.products_page.add_nth_product(2, continue_shopping=True)
        trending_items.append(f"MADAME: {madame2}")
        print(f"⚡ Added: {madame2}")

        # Add graphic design trending item
        self.products_page.navigate()
        self.products_page.filter_by_brand("Mast & Harbour")
        print("🔥 Adding GRAPHIC DESIGN item (Viral on social media)")

        self.products_page.add_product_by_name(
            "GRAPHIC DESIGN MEN T SHIRT - BLUE",
            continue_shopping=True
        )
        trending_items.append("GRAPHIC DESIGN MEN T SHIRT - BLUE")
        print(f"⚡ Added: GRAPHIC DESIGN MEN T SHIRT - BLUE (Rs. 1389)")

        # Add popular women's top
        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Tops")
        print("🔥 Adding popular Women's Top")

        womens_top = self.products_page.add_nth_product(1, continue_shopping=False)
        trending_items.append(f"Women's: {womens_top}")
        print(f"⚡ Added: {womens_top}")

        print(f"\n3. TRENDING CART REVIEW")
        print("-" * 80)

        # Go to cart and verify
        self.products_page.go_to_cart()
        cart_products = self.cart_page.get_products()

        print(f"⚡ Flash Shopping Cart - {len(cart_products)} trending items:")
        print(f"{'=' * 70}")
        print(f"🔥 Trending Items for Content Creation:")

        for i, product in enumerate(cart_products, 1):
            print(f"  {i}. {product['name']}")
            print(f"     {product['price']} x {product['quantity']} = {product['total']}")

        print(f"{'=' * 70}")

        assert len(cart_products) >= 6, "Should have at least 6 trending items"

        # Verify graphic design item is in cart
        cart_names = [p['name'] for p in cart_products]
        assert "GRAPHIC DESIGN MEN T SHIRT - BLUE" in cart_names, "Graphic design item should be in cart"

        print("✅ Trending items cart verified")

        print(f"\n4. RUSH CHECKOUT - Content Deadline")
        print("-" * 80)

        # Proceed to checkout with content creator notes
        self.cart_page.proceed_to_checkout()

        content_creator_note = (
            "URGENT - FASHION CONTENT CREATION ORDER\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Content Creator: @SophiaStyleNZ (250K followers)\n"
            "Purpose: Fashion haul video & lookbook photoshoot\n"
            "\n"
            "DEADLINE REQUIREMENTS:\n"
            "⚡ RUSH DELIVERY NEEDED - Content deadline: Dec 16th\n"
            "📹 Video shoot scheduled: Dec 17th\n"
            "📸 Instagram posts planned: Dec 18th-20th\n"
            "\n"
            "PACKAGING REQUIREMENTS:\n"
            "📦 Please use AESTHETIC packaging (unboxing video)\n"
            "🎨 Include brand tags visible for camera\n"
            "✨ Arrange items neatly (will be filmed)\n"
            "📋 Include size/care cards (close-up shots needed)\n"
            "\n"
            "SOCIAL MEDIA CREDIT:\n"
            "Will tag brand in posts (combined reach: 250K+)\n"
            "Stories, Reels, and Feed posts planned\n"
            "YouTube haul video featuring all items\n"
            "\n"
            "Contact for urgent delivery coordination:\n"
            "Mobile: 022-123-4567 (Available 24/7)\n"
            "Email: sophia@styleinfluencer.nz\n"
            "\n"
            "Thank you for supporting content creators! 🎥✨"
        )

        self.checkout_page.add_comment(content_creator_note)
        self.checkout_page.place_order()

        print("✅ Rush order placed for content creation")
        print("   ⚡ Delivery: RUSH (Content deadline Dec 16)")
        print("   📹 Purpose: Fashion haul video")
        print("   📦 Packaging: Unboxing-friendly aesthetic")
        print("   📱 Audience: 250K+ followers")
        print("   🎥 Content: YouTube + Instagram")

        print(f"\n5. EXPRESS PAYMENT")
        print("-" * 80)

        # Complete payment quickly
        self.payment_page.fill_payment_details(payment_data)
        self.payment_page.confirm_payment()

        # Verify success
        order_success = self.payment_page.verify_success()
        assert order_success, "Rush fashion order should be successful"

        print("✅ Express payment completed")

        print("\n" + "=" * 80)
        print("✅ TEST 10 PASSED: Trending Flash Shopping Successful!")
        print("   Shopping Style: Fast fashion flash purchase")
        print("   Items: 6 trending pieces")
        print("   Brands: BIBA + MADAME + MAST & HARBOUR")
        print("   Special: GRAPHIC DESIGN viral item (Rs. 1389)")
        print("   Purpose: Content creation (250K+ reach)")
        print("   Delivery: RUSH for video deadline")
        print("   Packaging: Unboxing-friendly aesthetic")
        print("=" * 80 + "\n")


# Configuration for pytest
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser for E2E tests"""
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