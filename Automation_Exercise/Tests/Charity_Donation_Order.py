"""
E2E Test Case 12: Charity Donation Order - Humanitarian Purchase

Scenario: NGO worker purchases clothing for charity distribution
to underprivileged communities with donation receipt requirements

File: test_e2e_12_charity_donation.py
"""

import pytest
from playwright.sync_api import Page
from Pages.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)


class TestCharityDonationOrder:
    """Test Case 12: Charity Donation Order - Humanitarian Purchase"""

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

    def test_charity_donation_clothing_order(self):
        """
        Test Case 12: Charity Donation Order - Humanitarian Purchase

        Scenario: NGO/Charity worker purchases essential clothing
        for distribution to underprivileged communities

        Steps:
        1. Register NGO worker account (India-based charity)
        2. Add practical women's clothing (for beneficiaries)
        3. Add practical men's clothing (for beneficiaries)
        4. Add kids essential clothing (for children)
        5. Add basic items from affordable brands
        6. Review charity donation cart (8+ essential items)
        7. Add NGO details and donation project information
        8. Request tax-exempt donation receipt
        9. Add beneficiary distribution details
        10. Complete payment with charity fund details
        11. Verify successful humanitarian order

        Expected: Bulk practical order with charity/NGO-specific
        documentation and tax-exempt receipt requirements
        """

        print("\n" + "=" * 80)
        print("TEST 12: Charity Donation Order - Humanitarian Purchase")
        print("=" * 80)

        # Test Data - NGO worker from India
        user_data = {
            'name': 'Rajesh Kumar',
            'email': TestDataFactory.generate_email(),
            'title': 'Mr',
            'password': 'Hope@2024',
            'dob': {'day': '20', 'month': '1', 'year': '1975'},
            'address': {
                'first_name': 'Rajesh',
                'last_name': 'Kumar',
                'company': 'Hope Foundation India',
                'address1': 'NGO Complex, Gandhi Nagar',
                'address2': 'Social Welfare Wing',
                'country': 'India',
                'state': 'Gujarat',
                'city': 'Ahmedabad',
                'zipcode': '380001',
                'mobile': '9876543210'
            }
        }
        payment_data = TestDataFactory.get_payment_data()
        payment_data['name'] = 'Hope Foundation India'  # Charity account

        print(f"\n1. NGO REGISTRATION")
        print("-" * 80)
        print(f"Organization: {user_data['address']['company']}")
        print(f"NGO Worker: {user_data['name']}")
        print(f"Purpose: Clothing donation for underprivileged")
        print(f"Registration: 80G Certified Charity")

        # Register NGO account
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

        print("✅ NGO account registered")

        print(f"\n2. HUMANITARIAN CLOTHING SHOPPING")
        print("-" * 80)
        print("🤝 Purchasing essentials for charity distribution...")

        charity_items = []
        beneficiary_counts = {'women': 0, 'men': 0, 'kids': 0}

        # Women's essential clothing
        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Tops")
        print("👗 Category: Women's Tops (For female beneficiaries)")

        women1 = self.products_page.add_nth_product(1, continue_shopping=True)
        charity_items.append(f"Women's: {women1}")
        beneficiary_counts['women'] += 1
        print(f"🤝 Added: {women1}")

        women2 = self.products_page.add_nth_product(2, continue_shopping=True)
        charity_items.append(f"Women's: {women2}")
        beneficiary_counts['women'] += 1
        print(f"🤝 Added: {women2}")

        # Women's saree (traditional/practical)
        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Saree")
        print("👗 Category: Women's Saree (Traditional clothing)")

        saree = self.products_page.add_nth_product(1, continue_shopping=True)
        charity_items.append(f"Saree: {saree}")
        beneficiary_counts['women'] += 1
        print(f"🤝 Added: {saree}")

        # Men's essential clothing
        self.products_page.navigate()
        self.products_page.filter_by_category("Men", "Tshirts")
        print("👔 Category: Men's Tshirts (For male beneficiaries)")

        men1 = self.products_page.add_nth_product(1, continue_shopping=True)
        charity_items.append(f"Men's: {men1}")
        beneficiary_counts['men'] += 1
        print(f"🤝 Added: {men1}")

        men2 = self.products_page.add_nth_product(2, continue_shopping=True)
        charity_items.append(f"Men's: {men2}")
        beneficiary_counts['men'] += 1
        print(f"🤝 Added: {men2}")

        men3 = self.products_page.add_nth_product(3, continue_shopping=True)
        charity_items.append(f"Men's: {men3}")
        beneficiary_counts['men'] += 1
        print(f"🤝 Added: {men3}")

        # Kids essential clothing
        self.products_page.navigate()
        self.products_page.filter_by_category("Kids", "Tops & Shirts")
        print("👶 Category: Kids Clothing (For children)")

        kids1 = self.products_page.add_nth_product(1, continue_shopping=True)
        charity_items.append(f"Kids: {kids1}")
        beneficiary_counts['kids'] += 1
        print(f"🤝 Added: {kids1}")

        kids2 = self.products_page.add_nth_product(2, continue_shopping=False)
        charity_items.append(f"Kids: {kids2}")
        beneficiary_counts['kids'] += 1
        print(f"🤝 Added: {kids2}")

        print(f"\n3. CHARITY DONATION CART REVIEW")
        print("-" * 80)

        # Go to cart and verify
        self.products_page.go_to_cart()
        cart_products = self.cart_page.get_products()

        print(f"🤝 Humanitarian Clothing Donation Order:")
        print(f"{'=' * 70}")
        print(f"Organization: Hope Foundation India")
        print(f"Purpose: Distribution to underprivileged communities")
        print(f"Total items: {len(cart_products)}")
        print(f"{'=' * 70}")
        print(f"Beneficiary Breakdown:")
        print(f"  • Women: {beneficiary_counts['women']} items")
        print(f"  • Men: {beneficiary_counts['men']} items")
        print(f"  • Children: {beneficiary_counts['kids']} items")
        print(f"{'=' * 70}")

        for i, product in enumerate(cart_products, 1):
            print(f"  🤝 {i}. {product['name']}")
            print(f"     {product['price']} x {product['quantity']}")

        print(f"{'=' * 70}")

        assert len(cart_products) >= 8, "Should have at least 8 charity items"
        print("✅ Charity donation cart verified")

        print(f"\n4. NGO CHECKOUT WITH DOCUMENTATION")
        print("-" * 80)

        # Proceed to checkout with NGO details
        self.cart_page.proceed_to_checkout()

        ngo_documentation = (
            "CHARITY DONATION ORDER - HOPE FOUNDATION INDIA\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "NGO Registration: 80G/12AA Certified (Tax-Exempt)\n"
            "Registration Number: NGO/IND/2015/012345\n"
            "PAN: AABCH1234F\n"
            "Contact: Rajesh Kumar - Program Director\n"
            "\n"
            "PROJECT DETAILS:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Project Name: Winter Relief Program 2024\n"
            "Project Code: WRP-2024-DEC\n"
            "Target Area: Rural Gujarat villages\n"
            "Beneficiaries: 50 families (approx 200 individuals)\n"
            "Distribution Date: December 18-20, 2024\n"
            "\n"
            "BENEFICIARY BREAKDOWN:\n"
            "• Women: {women_count} essential clothing items\n"
            "• Men: {men_count} essential clothing items\n"
            "• Children: {kids_count} essential clothing items\n"
            "\n"
            "DOCUMENTATION REQUIREMENTS:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "✓ Tax-exempt 80G donation receipt required\n"
            "✓ Itemized invoice with NGO registration details\n"
            "✓ Donation certificate for donor records\n"
            "✓ Bill format: As per Income Tax Act guidelines\n"
            "\n"
            "DELIVERY INSTRUCTIONS:\n"
            "• Deliver to: NGO Complex, Gandhi Nagar, Ahmedabad\n"
            "• Attention: Social Welfare Wing\n"
            "• Contact: +91-9876543210\n"
            "• Best time: Mon-Sat, 10 AM - 5 PM\n"
            "• Security clearance: Mention 'Hope Foundation'\n"
            "\n"
            "PACKAGING:\n"
            "• Simple, practical packaging (no luxury wrapping)\n"
            "• Easy to sort and distribute\n"
            "• Size labels clearly visible\n"
            "• Separate women's/men's/kids items if possible\n"
            "\n"
            "FUNDING:\n"
            "Source: Community Donation Fund\n"
            "Donor: Anonymous Corporate Sponsor\n"
            "Budget Code: WRP-CLOTHING-2024\n"
            "\n"
            "SOCIAL IMPACT:\n"
            "This order will provide essential clothing to 50 families\n"
            "from economically disadvantaged communities in rural Gujarat.\n"
            "Your support helps restore dignity and provide warmth.\n"
            "\n"
            "For donation receipt queries:\n"
            "Email: accounts@hopefoundation.org.in\n"
            "Phone: +91-79-2550-1234\n"
            "\n"
            "Thank you for supporting our humanitarian mission! 🙏"
        ).format(
            women_count=beneficiary_counts['women'],
            men_count=beneficiary_counts['men'],
            kids_count=beneficiary_counts['kids']
        )

        self.checkout_page.add_comment(ngo_documentation)
        self.checkout_page.place_order()

        print("✅ Charity donation order placed")
        print("   🤝 Organization: Hope Foundation India (80G Certified)")
        print("   📋 Project: Winter Relief Program 2024")
        print("   👥 Beneficiaries: 50 families (~200 people)")
        print("   📍 Location: Rural Gujarat villages")
        print("   📅 Distribution: Dec 18-20, 2024")
        print("   📄 Documentation: 80G receipt + donation certificate")

        print(f"\n5. CHARITY FUND PAYMENT")
        print("-" * 80)

        # Complete payment
        self.payment_page.fill_payment_details(payment_data)
        self.payment_page.confirm_payment()

        # Verify success
        order_success = self.payment_page.verify_success()
        assert order_success, "Charity donation order should be successful"

        print("✅ Charity payment completed")

        print("\n" + "=" * 80)
        print("✅ TEST 12 PASSED: Charity Donation Order Successful!")
        print("   Order Type: Humanitarian clothing donation")
        print("   Organization: Hope Foundation India (Registered NGO)")
        print("   Items: 8+ essential clothing pieces")
        print("   Beneficiaries: Women (3) + Men (3) + Kids (2)")
        print("   Project: Winter Relief Program 2024")
        print("   Target: 50 families in rural Gujarat")
        print("   Documentation:")
        print("     • 80G Tax-exempt receipt")
        print("     • NGO registration details")
        print("     • Donation certificate")
        print("     • Itemized invoice")
        print("   Social Impact: 200+ individuals benefited")
        print("   Purpose: Restoring dignity, providing warmth")
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