"""
E2E Test Case 6: Women's Saree Category - Special Occasion Purchase

Scenario: Customer purchases traditional sarees for a wedding event
with express delivery and gift wrapping

File: test_e2e_06_saree_occasion.py
"""

import pytest
from playwright.sync_api import Page
from Pages.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)


class TestSareeSpecialOccasion:
    """Test Case 6: Women's Saree Category - Special Occasion Purchase"""

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

    def test_saree_special_occasion_purchase(self):
        """
        Test Case 6: Women's Saree Category - Special Occasion Purchase

        Scenario: Customer purchases traditional sarees for a wedding event
        with express delivery and gift wrapping

        Steps:
        1. Register new user from India
        2. Navigate to Women > Saree category
        3. Add "Beautiful Peacock Blue Cotton Linen Saree" (Rs. 5000)
        4. Add another premium saree from the collection
        5. Navigate to Women > Dress category
        6. Add matching accessories/outfit
        7. Review cart with 3 special occasion items
        8. Proceed to checkout with event date and special instructions
        9. Add gift wrapping and express delivery note
        10. Complete payment
        11. Verify order success for special occasion

        Expected: High-value saree order with event-specific instructions processed
        """

        print("\n" + "=" * 80)
        print("TEST 6: Women's Saree Category - Special Occasion Purchase")
        print("=" * 80)

        # Test Data - India user for saree purchase
        user_data = {
            'name': 'Priya Sharma',
            'email': TestDataFactory.generate_email(),
            'title': 'Mrs',
            'password': 'India@2024',
            'dob': {'day': '10', 'month': '3', 'year': '1985'},
            'address': {
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'company': 'Sharma Textiles',
                'address1': '123 MG Road',
                'address2': 'Apartment 5C',
                'country': 'India',
                'state': 'Maharashtra',
                'city': 'Mumbai',
                'zipcode': '400001',
                'mobile': '9876543210'
            }
        }
        payment_data = TestDataFactory.get_payment_data()

        print(f"\n1. REGISTRATION - Customer: {user_data['name']}")
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

        print(f"\n2. SHOPPING - Saree Collection for Wedding")
        print("-" * 80)

        # Browse and add premium saree
        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Saree")
        print("✅ Filtered by Women > Saree")

        # Add the special peacock blue saree
        self.products_page.add_product_by_name(
            "Beautiful Peacock Blue Cotton Linen Saree",
            continue_shopping=True
        )
        print("✅ Added 'Beautiful Peacock Blue Cotton Linen Saree' (Rs. 5000)")

        # Add second saree
        saree2 = self.products_page.add_nth_product(2, continue_shopping=True)
        print(f"✅ Added second saree: {saree2}")

        # Add matching dress/top
        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Dress")
        print("✅ Browsing Women > Dress for matching outfit")

        dress = self.products_page.add_nth_product(1, continue_shopping=False)
        print(f"✅ Added matching outfit: {dress}")

        print(f"\n3. CART REVIEW - Special Occasion Order")
        print("-" * 80)

        # Go to cart and verify
        self.products_page.go_to_cart()
        cart_products = self.cart_page.get_products()

        print(f"Special occasion items in cart: {len(cart_products)}")
        total_value = 0
        for i, product in enumerate(cart_products, 1):
            print(f"  {i}. {product['name']}")
            print(f"     {product['price']} x {product['quantity']} = {product['total']}")

        assert len(cart_products) == 3, "Should have 3 special occasion items in cart"
        print("✅ Special occasion cart verified")

        print(f"\n4. CHECKOUT - Wedding Event Order")
        print("-" * 80)

        # Proceed to checkout with special instructions
        self.cart_page.proceed_to_checkout()

        special_instructions = (
            "WEDDING EVENT ORDER - Required by: December 20th\n"
            "Please gift wrap all items separately in premium packaging\n"
            "Include care instructions for sarees\n"
            "Express delivery required - Wedding is on Dec 22nd\n"
            "Contact on delivery: 9876543210"
        )

        self.checkout_page.add_comment(special_instructions)
        self.checkout_page.place_order()
        print("✅ Special occasion order placed with event date")
        print("   Event: Wedding (Dec 22nd)")
        print("   Delivery: Express by Dec 20th")
        print("   Special: Premium gift wrapping")

        print(f"\n5. PAYMENT - High Value Order")
        print("-" * 80)

        # Complete payment
        self.payment_page.fill_payment_details(payment_data)
        self.payment_page.confirm_payment()

        # Verify success
        order_success = self.payment_page.verify_success()
        assert order_success, "Special occasion order should be successful"

        print("✅ Payment completed for special occasion order")
        print("\n" + "=" * 80)
        print("✅ TEST 6 PASSED: Special occasion saree order successful!")
        print("   Order Type: Wedding Event Purchase")
        print("   Items: 2 Premium Sarees + 1 Matching Outfit")
        print("   Special Services: Express Delivery + Gift Wrapping")
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