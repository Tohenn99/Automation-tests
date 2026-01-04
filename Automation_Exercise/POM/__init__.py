"""
Page Object Model - All POM Export
Import all page classes from All_pages.py for easier access
"""

from .All_pages import (
    BasePage,
    LoginPage,
    RegistrationPage,
    ProductsPage,
    CartPage,
    CheckoutPage,
    PaymentPage,
    TestDataFactory
)

__all__ = [
    'BasePage',
    'LoginPage',
    'RegistrationPage',
    'ProductsPage',
    'CartPage',
    'CheckoutPage',
    'PaymentPage',
    'TestDataFactory'
]