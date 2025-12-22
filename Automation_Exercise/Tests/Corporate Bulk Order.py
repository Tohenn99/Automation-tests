"""
E2E Test Case 9: Corporate Bulk Order - Employee Gift Program

Scenario: HR manager purchases bulk clothing items as employee
gifts/uniforms with corporate billing and multiple delivery addresses

File: test_e2e_09_corporate_bulk.py
"""

import pytest
from playwright.sync_api import Page
from Pages.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)


class TestCorporateBulkOrder:
    """Test Case 9: Corporate Bulk Order - Employee Gift Program"""

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

    def test_corporate_bulk_gift_order(self):
        """
        Test Case 9: Corporate Bulk Order - Employee Gift Program

        Scenario: HR manager purchases bulk clothing items as employee
        gifts for company anniversary celebration

        Steps:
        1. Register corporate account (HR Manager)
        2. Add same product multiple times by re-adding (simulating bulk)
        3. Add products from Men's category (for male employees)
        4. Add products from Women's category (for female employees)
        5. Add unisex items from multiple brands
        6. Review large corporate cart (8+ items)
        7. Add corporate purchase order details
        8. Include bulk discount request and invoice requirements
        9. Add company anniversary celebration note
        10. Complete payment with corporate card details
        11. Verify successful bulk corporate order

        Expected: Large corporate order with business-specific
        instructions and invoice requirements processed
        """

        print("\n" + "=" * 80)
        print("TEST 9: Corporate Bulk Order - Employee Gift Program")
        print("=" * 80)

        # Test Data - Corporate account
        user_data = {
            'name': 'Jessica Martinez',
            'email': TestDataFactory.generate_email(),
            'title': 'Mrs',
            'password': 'Corporate@2024',
            'dob': {'day': '12', 'month': '4', 'year': '1983'},
            'address': {
                'first_name': 'Jessica',
                'last_name': 'Martinez',
                'company': 'TechVision Solutions Inc',
                'address1': '5000 Innovation Drive',
                'address2': 'HR Department - Floor 8',
                'country': 'United States',
                'state': 'California',
                'city': 'San Francisco',
                'zipcode': '94105',
                'mobile': '4155551234'
            }
        }
        payment_data = TestDataFactory.get_payment_data()
        payment_data['name'] = 'TechVision Solutions Inc'  # Corporate card

        print(f"\n1. CORPORATE REGISTRATION")
        print("-" * 80)
        print(f"Company: {user_data['address']['company']}")
        print(f"HR Manager: {user_data['name']}")
        print(f"Purpose: Employee Gift Program")

        # Register corporate account
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

        print("✅ Corporate account registered")

        print(f"\n2. BULK CORPORATE SHOPPING")
        print("-" * 80)
        print("🏢 Ordering employee gifts for 10th anniversary...")

        added_products = []

        # Add multiple Men's items for male employees
        self.products_page.navigate()
        self.products_page.filter_by_category("Men", "Tshirts")
        print("✅ Shopping Men > Tshirts (for male employees)")

        product1 = self.products_page.add_nth_product(1, continue_shopping=True)
        added_products.append(f"Men's: {product1}")
        print(f"🎁 Added: {product1}")

        product2 = self.products_page.add_nth_product(2, continue_shopping=True)
        added_products.append(f"Men's: {product2}")
        print(f"🎁 Added: {product2}")

        product3 = self.products_page.add_nth_product(3, continue_shopping=True)
        added_products.append(f"Men's: {product3}")
        print(f"🎁 Added: {product3}")

        # Add multiple Women's items for female employees
        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Tops")
        print("✅ Shopping Women > Tops (for female employees)")

        product4 = self.products_page.add_nth_product(1, continue_shopping=True)
        added_products.append(f"Women's: {product4}")
        print(f"🎁 Added: {product4}")

        product5 = self.products_page.add_nth_product(2, continue_shopping=True)
        added_products.append(f"Women's: {product5}")
        print(f"🎁 Added: {product5}")

        product6 = self.products_page.add_nth_product(3, continue_shopping=True)
        added_products.append(f"Women's: {product6}")
        print(f"🎁 Added: {product6}")

        # Add branded unisex items
        self.products_page.navigate()
        self.products_page.filter_by_brand("Polo")
        print("✅ Shopping POLO brand (unisex corporate gifts)")

        product7 = self.products_page.add_nth_product(1, continue_shopping=True)
        added_products.append(f"POLO: {product7}")
        print(f"🎁 Added: {product7}")

        self.products_page.navigate()
        self.products_page.filter_by_brand("H&M")
        print("✅ Shopping H&M brand (unisex corporate gifts)")

        product8 = self.products_page.add_nth_product(1, continue_shopping=False)
        added_products.append(f"H&M: {product8}")
        print(f"🎁 Added: {product8}")

        print(f"\n3. CORPORATE CART REVIEW")
        print("-" * 80)

        # Go to cart and verify
        self.products_page.go_to_cart()
        cart_products = self.cart_page.get_products()

        print(f"🏢 Corporate Bulk Order Cart:")
        print(f"{'=' * 70}")
        print(f"Company: TechVision Solutions Inc")
        print(f"Event: 10th Anniversary Celebration")
        print(f"Items in cart: {len(cart_products)}")
        print(f"{'=' * 70}")

        for i, product in enumerate(cart_products, 1):
            print(f"  🎁 {i}. {product['name']}")
            print(f"     {product['price']} x {product['quantity']} = {product['total']}")

        print(f"{'=' * 70}")

        total_quantity = sum(int(p['quantity']) for p in cart_products)
        assert total_quantity >= 8, f"Should have at least 8 items total (got {total_quantity})"
        print(f"✅ Corporate bulk cart verified: {len(cart_products)} unique products, {total_quantity} total items")

        print(f"\n4. CORPORATE CHECKOUT")
        print("-" * 80)

        # Proceed to checkout with corporate details
        self.cart_page.proceed_to_checkout()

        corporate_note = (
            "CORPORATE BULK ORDER - TechVision Solutions Inc\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Purchase Order #: PO-2024-GIFT-001\n"
            "Department: Human Resources\n"
            "Cost Center: HR-GIFTS-2024\n"
            "Event: Company 10th Anniversary Celebration\n"
            "\n"
            "EMPLOYEE GIFT DISTRIBUTION:\n"
            "• Male employees: Men's T-shirts\n"
            "• Female employees: Women's Tops\n"
            "• All staff: Branded unisex items\n"
            "\n"
            "REQUIREMENTS:\n"
            "• Invoice required with company Tax ID: 94-1234567\n"
            "• Bill to: Accounts Payable Department\n"
            "• Payment terms: Net 30\n"
            "• Bulk discount: Please apply corporate rate if available\n"
            "• Gift wrapping: Individual wrapping for each item\n"
            "• Include gift cards with company anniversary message\n"
            "\n"
            "DELIVERY:\n"
            "• Deliver to: HR Department, Floor 8\n"
            "• Contact: Jessica Martinez - HR Manager\n"
            "• Phone: (415) 555-1234\n"
            "• Delivery date needed: Before Dec 15th (Anniversary Dec 18th)\n"
            "\n"
            "Thank you for supporting our employee appreciation program!"
        )

        self.checkout_page.add_comment(corporate_note)
        self.checkout_page.place_order()

        print("✅ Corporate bulk order placed")
        print("   🏢 Company: TechVision Solutions Inc")
        print("   📋 PO Number: PO-2024-GIFT-001")
        print("   🎉 Event: 10th Anniversary")
        print("   👥 Recipients: All employees")
        print("   💳 Payment: Corporate account (Net 30)")
        print("   🎁 Special: Individual gift wrapping + cards")

        print(f"\n5. CORPORATE PAYMENT")
        print("-" * 80)

        # Complete payment with corporate card
        self.payment_page.fill_payment_details(payment_data)
        self.payment_page.confirm_payment()

        # Verify success
        order_success = self.payment_page.verify_success()
        assert order_success, "Corporate bulk order should be successful"

        print("✅ Corporate payment completed")

        print("\n" + "=" * 80)
        print("✅ TEST 9 PASSED: Corporate Bulk Order Successful!")
        print("   Order Type: Employee Gift Program")
        print("   Company: TechVision Solutions Inc")
        print("   Items: 8+ employee gifts")
        print("   Categories: Men's + Women's + Unisex Brands")
        print("   Purpose: 10th Anniversary Celebration")
        print("   Special: PO#, Tax ID, Invoice, Net 30, Gift Wrap")
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