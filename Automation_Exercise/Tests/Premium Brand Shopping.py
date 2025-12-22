"""
E2E Test Case 5: Premium Brand Shopping - Luxury Purchase Journey

Scenario: Fashion-conscious user purchases premium items from
high-end brands with special packaging request

File: test_e2e_05_premium_brands.py
"""

import pytest
from playwright.sync_api import Page
from Pages.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)


class TestPremiumBrandShopping:
    """Test Case 5: Premium Brand Shopping - Luxury Purchase"""

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

    def test_brand_focused_premium_shopping_checkout(self):
        """
        Test Case 5: Premium Brand Shopping - Luxury Purchase Journey

        Scenario: Fashion-conscious user purchases premium items from
        high-end brands with special packaging request

        Steps:
        1. Register new user with premium profile
        2. Browse and add premium brand products (BIBA, Madame)
        3. Add multiple premium items
        4. Review high-value cart
        5. Add premium packaging and delivery instructions
        6. Complete payment for premium order
        7. Verify successful premium purchase

        Expected: Premium multi-brand order with special instructions processed
        """

        print("\n" + "=" * 80)
        print("TEST 5: Premium Brand Shopping - Luxury Purchase")
        print("=" * 80)

        # Test Data
        user_data = TestDataFactory.get_user_data_usa()
        user_data['name'] = 'Elizabeth Thompson'
        user_data['address']['first_name'] = 'Elizabeth'
        user_data['address']['last_name'] = 'Thompson'
        user_data['address']['company'] = 'Thompson Fashion House'
        payment_data = TestDataFactory.get_payment_data()

        print(f"\n1. REGISTRATION - Premium Customer: {user_data['name']}")
        print("-" * 80)

        # Register
        self.login_page.navigate()
        self.login_page.signup(user_data['name'], user_data['email'])

        self.registration_page.fill_account_info(
            'Mrs',
            user_data['password'],
            user_data['dob']
        )
        self.registration_page.fill_address_info(user_data['address'])
        self.registration_page.submit_registration()
        self.registration_page.continue_after_registration()

        print("✅ Premium customer registered")

        print(f"\n2. PREMIUM BRAND SHOPPING")
        print("-" * 80)

        # BIBA brand product
        self.products_page.navigate()
        self.products_page.filter_by_brand("Biba")
        print("✅ Browsing BIBA premium brand")

        biba_product1 = self.products_page.add_nth_product(1, continue_shopping=True)
        print(f"✅ Added from BIBA: {biba_product1}")

        biba_product2 = self.products_page.add_nth_product(2, continue_shopping=True)
        print(f"✅ Added from BIBA: {biba_product2}")

        # Madame brand product
        self.products_page.navigate()
        self.products_page.filter_by_brand("Madame")
        print("✅ Browsing MADAME premium brand")

        madame_product1 = self.products_page.add_nth_product(1, continue_shopping=True)
        print(f"✅ Added from MADAME: {madame_product1}")

        madame_product2 = self.products_page.add_nth_product(2, continue_shopping=False)
        print(f"✅ Added from MADAME: {madame_product2}")

        print(f"\n3. PREMIUM CART REVIEW")
        print("-" * 80)

        # Review premium cart
        self.products_page.go_to_cart()
        cart_products = self.cart_page.get_products()

        print(f"Premium items in cart: {len(cart_products)}")

        for i, product in enumerate(cart_products, 1):
            print(f"  {i}. {product['name']}")
            print(f"     {product['price']} x {product['quantity']} = {product['total']}")

        assert len(cart_products) == 4, "Should have 4 premium products"
        print("✅ Premium cart verified")

        print(f"\n4. PREMIUM CHECKOUT")
        print("-" * 80)

        # Checkout with premium instructions
        self.cart_page.proceed_to_checkout()
        self.checkout_page.add_comment(
            "PREMIUM ORDER: Please use luxury gift packaging. "
            "Include authentication certificates. "
            "Signature required on delivery."
        )
        self.checkout_page.place_order()
        print("✅ Premium order placed with special instructions")

        print(f"\n5. PREMIUM PAYMENT")
        print("-" * 80)

        # Payment
        self.payment_page.fill_payment_details(payment_data)
        self.payment_page.confirm_payment()

        order_success = self.payment_page.verify_success()
        assert order_success, "Premium order should be successful"

        print("✅ Premium payment completed")
        print("\n" + "=" * 80)
        print("✅ TEST 5 PASSED: Premium brand order successful!")
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