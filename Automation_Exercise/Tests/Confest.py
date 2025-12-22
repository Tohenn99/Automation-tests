import pytest
from playwright.sync_api import Page
from Pages.All_pages import (
    LoginPage, RegistrationPage, ProductsPage,
    CartPage, CheckoutPage, PaymentPage, TestDataFactory
)



# Fixtures for all Page Objects
@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Fixture for LoginPage"""
    return LoginPage(page)


@pytest.fixture
def registration_page(page: Page) -> RegistrationPage:
    """Fixture for RegistrationPage"""
    return RegistrationPage(page)


@pytest.fixture
def products_page(page: Page) -> ProductsPage:
    """Fixture for ProductsPage"""
    return ProductsPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    """Fixture for CartPage"""
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    """Fixture for CheckoutPage"""
    return CheckoutPage(page)


@pytest.fixture
def payment_page(page: Page) -> PaymentPage:
    """Fixture for PaymentPage"""
    return PaymentPage(page)


# Fixtures for Test Data
@pytest.fixture
def user_data_usa():
    """USA user test data"""
    return TestDataFactory.get_user_data_usa()


@pytest.fixture
def user_data_canada():
    """Canada user test data"""
    return TestDataFactory.get_user_data_canada()


@pytest.fixture
def payment_data():
    """Payment test data"""
    return TestDataFactory.get_payment_data()


# Browser configuration
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Browser context configuration"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }