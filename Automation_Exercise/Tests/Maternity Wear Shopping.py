"""
Test Case 13: Maternity Wear Shopping
Expecting mother buying maternity and baby preparation items
"""

import pytest
from playwright.sync_api import Page
from Pages.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)


class TestMaternityWearShopping:
    """Test 13: Expecting mother buying maternity and baby preparation items"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.registration_page = RegistrationPage(page)
        self.products_page = ProductsPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.payment_page = PaymentPage(page)

    def test_maternity_preparation_order(self):
        """Expecting mother preparing for baby with maternity and baby clothes"""
        user_data = TestDataFactory.get_user_data_usa()
        user_data['name'] = 'Amanda Wilson'
        user_data['address']['first_name'] = 'Amanda'
        user_data['address']['last_name'] = 'Wilson'

        self.login_page.navigate()
        self.login_page.signup(user_data['name'], user_data['email'])
        self.registration_page.fill_account_info('Mrs', user_data['password'], user_data['dob'])
        self.registration_page.fill_address_info(user_data['address'])
        self.registration_page.submit_registration()
        self.registration_page.continue_after_registration()

        # Shop for maternity and baby items
        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Dress")
        self.products_page.add_nth_product(1, True)
        self.products_page.add_nth_product(2, True)

        self.products_page.navigate()
        self.products_page.filter_by_category("Kids", "Dress")
        self.products_page.add_nth_product(1, True)
        self.products_page.add_nth_product(2, False)

        self.products_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.add_comment(
            "MATERNITY PREPARATION ORDER\n"
            "Due date: February 2025\n"
            "Need comfortable maternity wear (size M-L)\n"
            "Baby clothes for newborn (0-3 months)\n"
            "Please use soft, gentle packaging\n"
            "Deliver to home address (I'm on bed rest)"
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