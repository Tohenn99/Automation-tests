"""
Test Case 15: Fitness Instructor Workout Wear
Fitness instructor buying activewear for training sessions
"""

import pytest
from playwright.sync_api import Page
from POM.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)


class TestFitnessInstructorOrder:
    """Test 15: Fitness instructor buying activewear for training sessions"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.registration_page = RegistrationPage(page)
        self.products_page = ProductsPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.payment_page = PaymentPage(page)

    def test_activewear_instructor_bulk(self):
        """Fitness instructor ordering multiple workout outfits for daily training"""
        user_data = TestDataFactory.get_user_data_usa()
        user_data['name'] = 'Marcus Johnson'
        user_data['address']['company'] = 'FitLife Gym & Training'

        self.login_page.navigate()
        self.login_page.signup(user_data['name'], user_data['email'])
        self.registration_page.fill_account_info('Mr', user_data['password'], user_data['dob'])
        self.registration_page.fill_address_info(user_data['address'])
        self.registration_page.submit_registration()
        self.registration_page.continue_after_registration()

        self.products_page.navigate()
        self.products_page.filter_by_category("Men", "Tshirts")
        for i in range(1, 6):
            self.products_page.add_nth_product(i, i < 5)

        self.products_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.add_comment(
            "FITNESS INSTRUCTOR PROFESSIONAL ORDER\n"
            "Gym: FitLife Training Center\n"
            "Need: 5 workout shirts for weekly training rotation\n"
            "Must be: Breathable, moisture-wicking preferred\n"
            "Size: XL (athletic fit)\n"
            "Used for: Personal training sessions, group classes\n"
            "Logo embroidery available? (for branding)"
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