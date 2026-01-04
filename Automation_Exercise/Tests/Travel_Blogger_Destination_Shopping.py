"""
Test Case 17: Travel Blogger Destination Shopping
Travel blogger buying clothes for international trip
"""

import pytest
from playwright.sync_api import Page
from POM.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)


class TestTravelBloggerOrder:
    """Test 17: Travel blogger buying clothes for international trip"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.registration_page = RegistrationPage(page)
        self.products_page = ProductsPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.payment_page = PaymentPage(page)

    def test_travel_wardrobe_preparation(self):
        """Travel blogger preparing versatile wardrobe for Asia trip"""
        user_data = TestDataFactory.get_user_data_usa()
        user_data['name'] = 'Isabella Rodriguez'
        user_data['address']['company'] = 'Wanderlust Travel Blog'

        self.login_page.navigate()
        self.login_page.signup(user_data['name'], user_data['email'])
        self.registration_page.fill_account_info('Mrs', user_data['password'], user_data['dob'])
        self.registration_page.fill_address_info(user_data['address'])
        self.registration_page.submit_registration()
        self.registration_page.continue_after_registration()

        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Tops")
        self.products_page.add_nth_product(1, True)
        self.products_page.add_nth_product(2, True)

        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Dress")
        self.products_page.add_nth_product(1, True)

        self.products_page.navigate()
        self.products_page.filter_by_category("Women", "Saree")
        self.products_page.add_nth_product(1, False)

        self.products_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.add_comment(
            "TRAVEL BLOGGER - ASIA TRIP WARDROBE\n"
            "Blog: @WanderlustIsabella (150K followers)\n"
            "Trip: 3-month Asia backpacking (India, Thailand, Bali)\n"
            "Departure: December 28th (URGENT)\n"
            "Need: Lightweight, packable, wrinkle-resistant\n"
            "Climate: Tropical + some temples (modest coverage)\n"
            "Will feature outfits in travel vlogs\n"
            "Vacuum-sealed packaging preferred for space saving"
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