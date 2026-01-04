"""
Test Case 16: College Student Budget Shopping
College student on tight budget buying essentials
"""

import pytest
from playwright.sync_api import Page
from POM.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)

class TestCollegeStudentBudget:
    """Test 16: College student on tight budget buying essentials"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.registration_page = RegistrationPage(page)
        self.products_page = ProductsPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.payment_page = PaymentPage(page)

    def test_student_budget_essentials(self):
        """College student buying basic essentials on student budget"""
        user_data = TestDataFactory.get_user_data_canada()
        user_data['name'] = 'Alex Chen'
        user_data['address']['address1'] = 'University Residence Hall'
        user_data['address']['address2'] = 'Room 305'

        self.login_page.navigate()
        self.login_page.signup(user_data['name'], user_data['email'])
        self.registration_page.fill_account_info('Mr', user_data['password'],
                                                 {'day': '15', 'month': '9', 'year': '2002'})
        self.registration_page.fill_address_info(user_data['address'])
        self.registration_page.submit_registration()
        self.registration_page.continue_after_registration()

        self.products_page.navigate()
        self.products_page.filter_by_category("Men", "Tshirts")
        self.products_page.add_nth_product(1, True)
        self.products_page.add_nth_product(2, True)

        self.products_page.navigate()
        self.products_page.filter_by_category("Men", "Jeans")
        self.products_page.add_nth_product(1, False)

        self.products_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.add_comment(
            "COLLEGE STUDENT ORDER\n"
            "University: McGill University\n"
            "Student ID: 260123456\n"
            "Budget: Tight student budget\n"
            "Deliver to: University residence (sign for package)\n"
            "Availability: Between classes (2-4 PM best)\n"
            "Note: First online order, please confirm delivery time"
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