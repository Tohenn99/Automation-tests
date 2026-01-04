"""
Test Case 21: Fashion Photography Stylist Order
Fashion stylist buying pieces for magazine photoshoot
"""

import pytest
from playwright.sync_api import Page
from POM import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)


class TestFashionStylistOrder:
    """Test 21: Fashion stylist buying pieces for magazine photoshoot"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.registration_page = RegistrationPage(page)
        self.products_page = ProductsPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.payment_page = PaymentPage(page)

    def test_photoshoot_wardrobe_collection(self):
        """Fashion stylist ordering diverse pieces for editorial photoshoot"""
        user_data = TestDataFactory.get_user_data_usa()
        user_data['name'] = 'Sophia Chen'
        user_data['address']['company'] = 'Vogue Style Studios'
        user_data['address']['first_name'] = 'Sophia'
        user_data['address']['last_name'] = 'Chen'

        self.login_page.navigate()
        self.login_page.signup(user_data['name'], user_data['email'])
        self.registration_page.fill_account_info('Ms', user_data['password'], user_data['dob'])
        self.registration_page.fill_address_info(user_data['address'])
        self.registration_page.submit_registration()
        self.registration_page.continue_after_registration()

        # Order diverse pieces for fashion shoot
        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Dress")
        self.products_page.add_nth_product(1, True)
        self.products_page.add_nth_product(3, True)

        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Saree")
        self.products_page.add_nth_product(1, True)

        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Tops")
        self.products_page.add_nth_product(1, True)
        self.products_page.add_nth_product(2, False)

        self.products_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.add_comment(
            "FASHION EDITORIAL PHOTOSHOOT ORDER\n"
            "Studio: Vogue Style Studios\n"
            "Lead Stylist: Sophia Chen\n"
            "Project: 'Global Fusion' Editorial Spread\n"
            "Magazine: Modern Fashion Quarterly - Spring Issue\n"
            "Shoot Date: December 20-22, 2024\n"
            "Theme: Cross-cultural fashion fusion\n"
            "Models: 2 female models (size 2-4)\n"
            "Photographer: James Rodriguez\n"
            "NOTE: Items will be styled, photographed, and returned\n"
            "Need tags intact for return policy\n"
            "Rush delivery required - photoshoot confirmed\n"
            "Invoice: Production Account VG-2024-Q4\n"
            "Contact: sophia.chen@voguestudios.com"
        )
        self.checkout_page.place_order()
        self.payment_page.fill_payment_details(TestDataFactory.get_payment_data())
        self.payment_page.confirm_payment()
        assert self.payment_page.verify_success()


# Pytest configuration
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1920, "height": 1080}, "no_viewport": False}


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--headed"])