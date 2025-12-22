"""
E2E Test Case 8: Winter Collection - Seasonal Shopping Spree

Scenario: Customer prepares for winter season by purchasing
winter-specific clothing items with bulk discount expectations

File: test_e2e_08_winter_seasonal.py
"""

import pytest
from playwright.sync_api import Page
from Pages.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)


class TestWinterSeasonalShopping:
    """Test Case 8: Winter Collection - Seasonal Shopping Spree"""

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

    def test_winter_collection_seasonal_shopping(self):
        """
        Test Case 8: Winter Collection - Seasonal Shopping Spree

        Scenario: Customer prepares for winter season by purchasing
        winter-specific clothing from multiple categories

        Steps:
        1. Register new Canadian user (cold climate)
        2. Search and add "Winter Top" from MAST & HARBOUR brand
        3. Add winter items from Women's category
        4. Add winter items from Men's category
        5. Add kids winter clothing
        6. Review seasonal cart with 6+ winter items
        7. Add seasonal shopping note about winter preparation
        8. Request careful packaging for winter items
        9. Complete payment for seasonal order
        10. Verify successful winter collection purchase

        Expected: Seasonal bulk winter order processed with special
        winter-specific packaging instructions
        """

        print("\n" + "=" * 80)
        print("TEST 8: Winter Collection - Seasonal Shopping Spree")
        print("=" * 80)

        # Test Data - Canadian user (winter climate)
        user_data = {
            'name': 'Robert Anderson',
            'email': TestDataFactory.generate_email(),
            'title': 'Mr',
            'password': 'Winter@2024',
            'dob': {'day': '5', 'month': '11', 'year': '1980'},
            'address': {
                'first_name': 'Robert',
                'last_name': 'Anderson',
                'company': 'Northern Supplies Ltd',
                'address1': '890 Winter Street',
                'address2': 'Suite 202',
                'country': 'Canada',
                'state': 'Alberta',
                'city': 'Calgary',
                'zipcode': 'T2P 1J9',
                'mobile': '4035551234'
            }
        }
        payment_data = TestDataFactory.get_payment_data()

        print(f"\n1. REGISTRATION - Winter Shopper: {user_data['name']}")
        print("-" * 80)

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

        print("✅ Registration completed - Calgary, Canada (Cold Climate)")

        print(f"\n2. WINTER COLLECTION SHOPPING")
        print("-" * 80)
        print("🌨️ Preparing for winter season...")

        added_products = []

        # Add Winter Top from MAST & HARBOUR brand
        self.products_page.navigate()
        self.products_page.filter_by_brand("Mast & Harbour")
        print("✅ Shopping MAST & HARBOUR brand")

        self.products_page.add_product_by_name("Winter Top", continue_shopping=True)
        added_products.append("Winter Top")
        print("❄️ Added: Winter Top (Rs. 600)")

        # Add winter items from Women's category
        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Tops")
        print("✅ Shopping Women > Tops for winter wear")

        product2 = self.products_page.add_nth_product(1, continue_shopping=True)
        added_products.append(product2)
        print(f"❄️ Added women's item: {product2}")

        product3 = self.products_page.add_nth_product(3, continue_shopping=True)
        added_products.append(product3)
        print(f"❄️ Added women's item: {product3}")

        # Add winter items from Men's category
        self.products_page.navigate()
        self.products_page.filter_by_category("Men", "Tshirts")
        print("✅ Shopping Men > Tshirts for winter layers")

        product4 = self.products_page.add_nth_product(1, continue_shopping=True)
        added_products.append(product4)
        print(f"❄️ Added men's item: {product4}")

        product5 = self.products_page.add_nth_product(2, continue_shopping=True)
        added_products.append(product5)
        print(f"❄️ Added men's item: {product5}")

        # Add kids winter clothing
        self.products_page.navigate()
        self.products_page.filter_by_category("Kids", "Tops & Shirts")
        print("✅ Shopping Kids > Tops & Shirts for winter")

        product6 = self.products_page.add_nth_product(1, continue_shopping=False)
        added_products.append(product6)
        print(f"❄️ Added kids winter item: {product6}")

        print(f"\n3. WINTER COLLECTION CART REVIEW")
        print("-" * 80)

        # Go to cart and verify
        self.products_page.go_to_cart()
        cart_products = self.cart_page.get_products()

        print(f"🌨️ Winter Collection Cart - {len(cart_products)} items:")
        print(f"{'=' * 70}")

        total_items = 0
        for i, product in enumerate(cart_products, 1):
            print(f"  ❄️ {i}. {product['name']}")
            print(f"     Price: {product['price']} x Qty: {product['quantity']} = {product['total']}")
            total_items += int(product['quantity'])

        print(f"{'=' * 70}")
        print(f"Total winter items: {total_items}")

        assert len(cart_products) >= 6, "Should have at least 6 winter items"
        assert "Winter Top" in [p['name'] for p in cart_products], "Winter Top should be in cart"
        print("✅ Winter collection cart verified")

        print(f"\n4. SEASONAL CHECKOUT")
        print("-" * 80)

        # Proceed to checkout with seasonal notes
        self.cart_page.proceed_to_checkout()

        seasonal_note = (
            "WINTER SEASON PREPARATION ORDER\n"
            "Calgary winter can reach -30°C - these items are essential!\n"
            "Please pack carefully - winter items need protection from moisture\n"
            "Bulk order for entire family for upcoming winter season\n"
            "If possible, include winter care tips/instructions\n"
            "Delivery address has heated reception - safe for winter delivery"
        )

        self.checkout_page.add_comment(seasonal_note)
        self.checkout_page.place_order()

        print("✅ Winter collection order placed")
        print("   🌨️ Season: Winter Preparation")
        print("   🏔️ Location: Calgary, Canada (-30°C climate)")
        print("   📦 Special: Moisture-proof packaging requested")
        print("   👨‍👩‍👧 Purpose: Entire family winter clothing")

        print(f"\n5. PAYMENT - Seasonal Order")
        print("-" * 80)

        # Complete payment
        self.payment_page.fill_payment_details(payment_data)
        self.payment_page.confirm_payment()

        # Verify success
        order_success = self.payment_page.verify_success()
        assert order_success, "Winter seasonal order should be successful"

        print("✅ Payment completed for winter collection")

        print("\n" + "=" * 80)
        print("✅ TEST 8 PASSED: Winter Collection Shopping Successful!")
        print("   Season: Winter Preparation")
        print("   Items: 6+ winter clothing items")
        print("   Categories: Women + Men + Kids")
        print("   Special: Winter-specific 'Winter Top' included")
        print("   Location: Calgary, Canada (Cold Climate)")
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