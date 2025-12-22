"""
Test Case 18: Theater Costume Designer Order
Theater costume designer buying pieces for production
"""

import pytest
from playwright.sync_api import Page
from Pages.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)


class TestTheaterCostumeOrder:
    """Test 18: Theater costume designer buying pieces for production"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.registration_page = RegistrationPage(page)
        self.products_page = ProductsPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.payment_page = PaymentPage(page)

    def test_theater_costume_purchase(self):
        """Costume designer buying base pieces for theater production"""
        user_data = TestDataFactory.get_user_data_canada()
        user_data['name'] = 'Victoria Harper'
        user_data['address']['company'] = 'Community Theater Arts'

        self.login_page.navigate()
        self.login_page.signup(user_data['name'], user_data['email'])
        self.registration_page.fill_account_info('Mrs', user_data['password'], user_data['dob'])
        self.registration_page.fill_address_info(user_data['address'])
        self.registration_page.submit_registration()
        self.registration_page.continue_after_registration()

        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Dress")
        self.products_page.add_nth_product(1, True)
        self.products_page.add_nth_product(2, True)

        self.products_page.navigate()
        self.products_page.filter_by_category("Men", "Tshirts")
        self.products_page.add_nth_product(1, True)

        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Saree")
        self.products_page.add_nth_product(1, False)

        self.products_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.add_comment(
            "THEATER COSTUME DEPARTMENT ORDER\n"
            "Production: 'A Midsummer Night's Dream'\n"
            "Theater: Community Arts Center\n"
            "Costume Designer: Victoria Harper\n"
            "Opening Night: January 15, 2025\n"
            "Purpose: Base garments for costume alterations\n"
            "Will be: Dyed, embellished, altered for characters\n"
            "Budget: Theater production fund\n"
            "Invoice to: Arts Center Accounts Department\n"
            "Need receipt for theater records"
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