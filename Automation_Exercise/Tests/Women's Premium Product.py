"""
E2E Test Case 1: Women's Category - Single Premium Product Purchase

Scenario: New user registers and purchases a single high-value item
from Women's Dress category

File: test_e2e_01_womens_premium.py - NE
"""

import pytest
from playwright.sync_api import Page
from Pages.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)


class TestWomensPremiumCheckout:
    """Test Case 1: Women's Category - Single Premium Product"""

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

    def test_womens_category_single_product_checkout(self):
        """
        Test Case 1: Women's Category - Single Premium Product Purchase

        Scenario: New user registers and purchases a single high-value item
        from Women's Dress category

        Steps:
        1. Register new USA user
        2. Navigate to Women > Dress category
        3. Add "Fancy Green Top" to cart
        4. Proceed to checkout
        5. Add delivery instructions
        6. Complete payment
        7. Verify order success

        Expected: Order placed successfully with correct product
        """

        print("\n" + "=" * 80)
        print("TEST 1: Women's Category - Single Premium Product")
        print("=" * 80)

        # Test Data
        user_data = TestDataFactory.get_user_data_usa()
        payment_data = TestDataFactory.get_payment_data()

        print(f"\n1. REGISTRATION - User: {user_data['name']}")
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

        print("✅ Registration completed")

        print(f"\n2. SHOPPING - Women's Category")
        print("-" * 80)

        # Browse and add product
        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "TOPS")
        print("✅ Filtered by Women > TOPS")

        self.products_page.add_product_by_name("Fancy Green Top", continue_shopping=False)
        print(f"✅ Added 'Fancy Green Top' to cart")

        print(f"\n3. CART REVIEW")
        print("-" * 80)

        # Go to cart and verify
        self.products_page.go_to_cart()
        cart_products = self.cart_page.get_products()

        print(f"Products in cart: {len(cart_products)}")
        for product in cart_products:
            print(f"  • {product['name']} - {product['price']} x {product['quantity']} = {product['total']}")

        assert len(cart_products) == 1, "Should have 1 product in cart"
        assert "Fancy Green Top" in cart_products[0]['name'] or "Green Top" in cart_products[0]['name']
        print("✅ Cart verified")

        print(f"\n4. CHECKOUT")
        print("-" * 80)

        # Proceed to checkout
        self.cart_page.proceed_to_checkout()
        self.checkout_page.add_comment("Please handle with care - premium item")
        self.checkout_page.place_order()
        print("✅ Placed order")

        print(f"\n5. PAYMENT")
        print("-" * 80)

        # Complete payment
        self.payment_page.fill_payment_details(payment_data)
        self.payment_page.confirm_payment()

        # Verify success
        order_success = self.payment_page.verify_success()
        assert order_success, "Order should be successful"

        print("✅ Payment completed")
        print("\n" + "=" * 80)
        print("✅ TEST 1 PASSED: Single premium product purchased successfully!")
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