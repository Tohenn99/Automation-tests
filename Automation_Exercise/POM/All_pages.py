"""
Base Page Object Model - Foundation for all page objects
Follows SOLID principles and best OOP practices
"""

from playwright.sync_api import Page, expect
from abc import ABC
import random
import string


class BasePage(ABC):
    """Abstract base class for all page objects"""

    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://automationexercise.com"

    def navigate_to(self, path: str = ""):
        """Navigate to a specific path"""
        url = f"{self.base_url}{path}"
        self.page.goto(url)
        self.page.wait_for_load_state('networkidle')

    def handle_cookie_consent(self):
        """Handle cookie consent popup if it appears"""
        try:
            consent_button = self.page.locator('.fc-button.fc-cta-consent').first
            if consent_button.is_visible(timeout=5000):
                consent_button.click()
                self.page.wait_for_timeout(1000)
        except:
            pass

    def wait_for_element(self, selector: str, timeout: int = 5000):
        """Wait for element to be visible"""
        element = self.page.locator(selector)
        expect(element).to_be_visible(timeout=timeout)
        return element

    def scroll_to_element(self, selector: str):
        """Scroll element into view"""
        element = self.page.locator(selector)
        element.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        return element


class LoginPage(BasePage):
    """Page Object for Login/Signup functionality"""

    # Locators
    SIGNUP_NAME = 'input[data-qa="signup-name"]'
    SIGNUP_EMAIL = 'input[data-qa="signup-email"]'
    SIGNUP_BUTTON = 'button[data-qa="signup-button"]'

    def navigate(self):
        """Navigate to login page"""
        self.navigate_to("/login")
        self.handle_cookie_consent()

    def signup(self, name: str, email: str):
        """Fill and submit signup form"""
        self.page.locator(self.SIGNUP_NAME).fill(name)
        self.page.locator(self.SIGNUP_EMAIL).fill(email)
        self.page.locator(self.SIGNUP_BUTTON).click()
        self.page.wait_for_selector('#form')


class RegistrationPage(BasePage):
    """Page Object for Registration form"""

    # Locators
    TITLE_MR = '#id_gender1'
    TITLE_MRS = '#id_gender2'
    PASSWORD = '#password'
    DAY = '#days'
    MONTH = '#months'
    YEAR = '#years'
    NEWSLETTER = '#newsletter'
    OFFERS = '#optin'
    FIRST_NAME = '#first_name'
    LAST_NAME = '#last_name'
    COMPANY = '#company'
    ADDRESS1 = '#address1'
    ADDRESS2 = '#address2'
    COUNTRY = '#country'
    STATE = '#state'
    CITY = '#city'
    ZIPCODE = '#zipcode'
    MOBILE = '#mobile_number'
    CREATE_ACCOUNT = 'button[data-qa="create-account"]'
    CONTINUE = 'a[data-qa="continue-button"]'

    def fill_account_info(self, title: str, password: str, dob: dict):
        """Fill account information section"""
        if title.lower() == "mr":
            self.page.locator(self.TITLE_MR).check()
        else:
            self.page.locator(self.TITLE_MRS).check()

        self.page.locator(self.PASSWORD).fill(password)
        self.page.locator(self.DAY).select_option(dob['day'])
        self.page.locator(self.MONTH).select_option(dob['month'])
        self.page.locator(self.YEAR).select_option(dob['year'])
        self.page.locator(self.NEWSLETTER).check()
        self.page.locator(self.OFFERS).check()

    def fill_address_info(self, address_data: dict):
        """Fill address information section"""
        self.page.locator(self.FIRST_NAME).fill(address_data['first_name'])
        self.page.locator(self.LAST_NAME).fill(address_data['last_name'])
        self.page.locator(self.COMPANY).fill(address_data['company'])
        self.page.locator(self.ADDRESS1).fill(address_data['address1'])
        self.page.locator(self.ADDRESS2).fill(address_data['address2'])
        self.page.locator(self.COUNTRY).select_option(address_data['country'])
        self.page.locator(self.STATE).fill(address_data['state'])
        self.page.locator(self.CITY).fill(address_data['city'])
        self.page.locator(self.ZIPCODE).fill(address_data['zipcode'])
        self.page.locator(self.MOBILE).fill(address_data['mobile'])

    def submit_registration(self):
        """Submit registration form"""
        self.page.locator(self.CREATE_ACCOUNT).click()
        self.page.wait_for_load_state('networkidle')

    def continue_after_registration(self):
        """Click continue after successful registration"""
        self.wait_for_element(self.CONTINUE)
        self.page.locator(self.CONTINUE).click()  # ← Директно използвай page.locator
        self.page.wait_for_load_state('domcontentloaded')
        self.handle_cookie_consent()


class ProductsPage(BasePage):
    """Page Object for Products page"""

    # Locators
    PRODUCTS_LINK = 'a[href="/products"]'
    SINGLE_PRODUCT = '.single-products'
    ADD_TO_CART = '.overlay-content .add-to-cart'
    CART_MODAL = '#cartModal'
    CONTINUE_SHOPPING = 'button:has-text("Continue Shopping")'
    VIEW_CART = 'a:has-text("View Cart")'

    def navigate(self):
        """Navigate to products page"""
        self.page.locator(self.PRODUCTS_LINK).first.click()
        self.page.wait_for_selector('.features_items')

    def filter_by_category(self, category: str, subcategory: str):
        """Filter products by category and subcategory"""
        # Expand category
        category_link = self.page.locator(f'.panel-heading a[href="#{category}"]').first
        if 'collapsed' in (category_link.get_attribute('class') or ''):
            category_link.click()
            self.page.wait_for_timeout(1000)

        # Use JavaScript to click subcategory (bypasses visibility checks)
        subcategory_selector = f'#{category} a:has-text("{subcategory}")'
        self.page.eval_on_selector(
            subcategory_selector,
            'element => element.click()'
        )

        self.page.wait_for_selector('.features_items')
        self.page.wait_for_timeout(1000)

    def filter_by_brand(self, brand: str):
        """Filter products by brand"""
        brand_link = self.page.locator(f'.brands-name a:has-text("{brand}")').first
        brand_link.click()
        self.page.wait_for_selector('.features_items')
        self.page.wait_for_timeout(1000)

    def add_product_by_name(self, product_name: str, continue_shopping: bool = True):
        """Add a specific product to cart by name"""
        product = self.page.locator(
            f'.single-products:has(.productinfo p:text-is("{product_name}"))'
        ).first

        product.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        product.hover()
        self.page.wait_for_timeout(500)

        add_btn = product.locator(self.ADD_TO_CART).first
        add_btn.click()

        self.page.wait_for_selector(self.CART_MODAL, state='visible')

        if continue_shopping:
            self.page.locator(self.CONTINUE_SHOPPING).click()
            self.page.wait_for_selector(self.CART_MODAL, state='hidden')

    def add_nth_product(self, position: int, continue_shopping: bool = True):
        """Add nth product from current page"""
        products = self.page.locator(self.SINGLE_PRODUCT).all()

        if position > len(products):
            raise ValueError(f"Only {len(products)} products available")

        product = products[position - 1]
        product_name = product.locator('.productinfo p').first.inner_text()

        product.hover()
        self.page.wait_for_timeout(500)

        add_btn = product.locator(self.ADD_TO_CART).first
        add_btn.click()

        self.page.wait_for_selector(self.CART_MODAL, state='visible')

        if continue_shopping:
            self.page.locator(self.CONTINUE_SHOPPING).click()
            self.page.wait_for_selector(self.CART_MODAL, state='hidden')

        return product_name

    def go_to_cart(self):
        """Navigate to cart from modal"""
        self.page.locator(self.VIEW_CART).first.click()
        self.page.wait_for_load_state('networkidle')


class CartPage(BasePage):
    """Page Object for Shopping Cart"""

    # Locators
    CART_TABLE = '#cart_info_table tbody tr'
    PROCEED_TO_CHECKOUT = 'a.btn.btn-default.check_out'
    CART_LINK = 'a[href="/view_cart"]'

    def navigate(self):
        """Navigate to cart page"""
        self.page.locator(self.CART_LINK).first.click()
        self.page.wait_for_load_state('networkidle')

    def get_products(self):
        """Get list of products in cart"""
        rows = self.page.locator(self.CART_TABLE).all()
        products = []

        for row in rows:
            try:
                name = row.locator('.cart_description h4 a').inner_text()
                price = row.locator('.cart_price p').inner_text()
                quantity = row.locator('.cart_quantity button').inner_text()
                total = row.locator('.cart_total_price').inner_text()

                products.append({
                    'name': name,
                    'price': price,
                    'quantity': quantity,
                    'total': total
                })
            except:
                pass

        return products

    def proceed_to_checkout(self):
        """Click proceed to checkout button"""
        self.page.locator(self.PROCEED_TO_CHECKOUT).click()
        self.page.wait_for_load_state('networkidle')


class CheckoutPage(BasePage):
    """Page Object for Checkout page"""

    # Locators
    COMMENT = 'textarea[name="message"]'
    PLACE_ORDER = 'a[href="/payment"]'

    def add_comment(self, comment: str):
        """Add order comment"""
        comment_field = self.page.locator(self.COMMENT)
        comment_field.scroll_into_view_if_needed()
        comment_field.fill(comment)

    def place_order(self):
        """Click place order button"""
        self.page.locator(self.PLACE_ORDER).click()
        self.page.wait_for_load_state('networkidle')


class PaymentPage(BasePage):
    """Page Object for Payment page"""

    # Locators
    NAME_ON_CARD = 'input[name="name_on_card"]'
    CARD_NUMBER = 'input[name="card_number"]'
    CVC = 'input[name="cvc"]'
    EXPIRY_MONTH = 'input[name="expiry_month"]'
    EXPIRY_YEAR = 'input[name="expiry_year"]'
    PAY_BUTTON = 'button[data-qa="pay-button"]'

    def fill_payment_details(self, payment_data: dict):
        """Fill payment form"""
        self.page.locator(self.NAME_ON_CARD).fill(payment_data['name'])
        self.page.locator(self.CARD_NUMBER).fill(payment_data['card_number'])
        self.page.locator(self.CVC).fill(payment_data['cvc'])
        self.page.locator(self.EXPIRY_MONTH).fill(payment_data['expiry_month'])
        self.page.locator(self.EXPIRY_YEAR).fill(payment_data['expiry_year'])

    def confirm_payment(self):
        """Click pay and confirm order"""
        self.page.locator(self.PAY_BUTTON).click()
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(2000)

    def verify_success(self):
        """Verify order success"""
        try:
            success = self.page.locator('p:has-text("Congratulations")')
            return success.is_visible(timeout=5000)
        except:
            return False


class TestDataFactory:
    """Factory class for generating test data"""

    @staticmethod
    def generate_email():
        """Generate unique email"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"testuser_{random_string}@example.com"

    @staticmethod
    def get_user_data_usa():
        """Get USA user data"""
        return {
            'name': 'John Smith',
            'email': TestDataFactory.generate_email(),
            'title': 'Mr',
            'password': 'Test@2024',
            'dob': {'day': '15', 'month': '6', 'year': '1990'},
            'address': {
                'first_name': 'John',
                'last_name': 'Smith',
                'company': 'Tech Corp USA',
                'address1': '123 Main Street',
                'address2': 'Suite 500',
                'country': 'United States',
                'state': 'California',
                'city': 'Los Angeles',
                'zipcode': '90001',
                'mobile': '3105551234'
            }
        }

    @staticmethod
    def get_user_data_canada():
        """Get Canada user data"""
        return {
            'name': 'Sarah Johnson',
            'email': TestDataFactory.generate_email(),
            'title': 'Mrs',
            'password': 'Canada@2024',
            'dob': {'day': '22', 'month': '9', 'year': '1988'},
            'address': {
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'company': 'Maple Tech Inc',
                'address1': '456 King Street',
                'address2': 'Unit 12',
                'country': 'Canada',
                'state': 'Ontario',
                'city': 'Toronto',
                'zipcode': 'M5H 1A1',
                'mobile': '4165551234'
            }
        }

    @staticmethod
    def get_payment_data():
        """Get payment details"""
        return {
            'name': 'Test User',
            'card_number': '4532015112830366',
            'cvc': '871',
            'expiry_month': '12',
            'expiry_year': '2027'
        }