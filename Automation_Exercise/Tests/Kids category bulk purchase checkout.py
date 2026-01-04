"""
Test Case 3: Kids category bulk purchase checkout
"""

import pytest
from playwright.sync_api import Page
from POM.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)


class TestKidsBulkOrder:
    """
    Test Case 3: Kids category bulk purchase checkout
    """

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test"""
        self.page = page
        self.login_page = LoginPage(page)
        self.registration_page = RegistrationPage(page)
        self.products_page = ProductsPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.payment_page = PaymentPage(page)

    def test_03_kids_category_bulk_purchase_checkout(self):
        """
        Test Case 3: Kids Category - Bulk Purchase with Multiple Quantities

        Scenario: Parent buys multiple kids items in bulk for family

        Steps:
        1. Register new user
        2. Browse Kids category
        3. Add multiple kids products
        4. Add products from different kids subcategories
        5. Review bulk order in cart
        6. Add family delivery note
        7. Complete payment for bulk order
        8. Verify successful bulk purchase

        Expected: Large order with multiple kids items processed successfully
        """

        print("\n" + "=" * 80)
        print("TEST 3: Kids Category - Bulk Family Purchase")
        print("=" * 80)

        # Test Data
        user_data = TestDataFactory.get_user_data_usa()
        user_data['name'] = 'Jennifer Martinez'
        user_data['address']['first_name'] = 'Jennifer'
        user_data['address']['last_name'] = 'Martinez'
        payment_data = TestDataFactory.get_payment_data()

        print(f"\n1. REGISTRATION - User: {user_data['name']}")
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

        print("✅ Registration completed")

        print(f"\n2. SHOPPING - Kids Category Bulk Purchase")
        print("-" * 80)

        # Add multiple kids products
        self.products_page.navigate()
        self.products_page.filter_by_category("Kids", "Dress")
        print("✅ Browsing Kids > Dress")

        product1 = self.products_page.add_nth_product(1, continue_shopping=True)
        print(f"✅ Added: {product1}")

        product2 = self.products_page.add_nth_product(2, continue_shopping=True)
        print(f"✅ Added: {product2}")

        # Add from different kids subcategory
        self.products_page.navigate()
        self.products_page.filter_by_category("Kids", "Tops & Shirts")
        print("✅ Browsing Kids > Tops & Shirts")

        product3 = self.products_page.add_nth_product(1, continue_shopping=True)
        print(f"✅ Added: {product3}")

        product4 = self.products_page.add_nth_product(2, continue_shopping=False)
        print(f"✅ Added: {product4}")

        print(f"\n3. CART REVIEW - Bulk Order")
        print("-" * 80)

        # Review cart
        self.products_page.go_to_cart()
        cart_products = self.cart_page.get_products()

        print(f"Total items in cart: {len(cart_products)}")
        total_value = 0
        for i, product in enumerate(cart_products, 1):
            print(f"  {i}. {product['name']}")
            print(f"     {product['price']} x {product['quantity']}")

        assert len(cart_products) >= 4, "Should have at least 4 products"
        print("✅ Bulk cart verified")

        print(f"\n4. CHECKOUT - Family Order")
        print("-" * 80)

        # Checkout
        self.cart_page.proceed_to_checkout()
        self.checkout_page.add_comment("Bulk order for kids - please ensure all sizes are correct")
        self.checkout_page.place_order()
        print("✅ Bulk order placed")

        print(f"\n5. PAYMENT")
        print("-" * 80)

        # Payment
        self.payment_page.fill_payment_details(payment_data)
        self.payment_page.confirm_payment()

        order_success = self.payment_page.verify_success()
        assert order_success, "Bulk order should be successful"

        print("✅ Bulk payment completed")
        print("\n" + "=" * 80)
        print("✅ TEST 3 PASSED: Bulk kids order completed successfully!")
        print("=" * 80 + "\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--headed", "--tb=short"])