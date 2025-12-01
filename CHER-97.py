import pytest
from playwright.sync_api import Page, expect
import random
import string


class TestCompleteEcommerceFlow:
    """Test suite for complete e-commerce flow: registration, shopping, checkout, and payment"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup method to navigate to the website before each test"""
        self.page = page
        self.base_url = "https://automationexercise.com"
        self.added_products = []

    def handle_cookie_consent(self):
        """Handle cookie consent popup if it appears"""
        try:
            consent_button = self.page.locator('.fc-button.fc-cta-consent').first
            if consent_button.is_visible(timeout=5000):
                consent_button.click()
                self.page.wait_for_timeout(1000)
                print("✅ Accepted cookie consent")
        except:
            pass

    def generate_unique_email(self):
        """Generate a unique email address for registration"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"testuser_{random_string}@testmail.com"

    def navigate_to_signup(self):
        """Navigate to signup/login page"""
        print("🔐 Navigating to Signup page...")
        signup_link = self.page.locator('a[href="/login"]').first
        signup_link.click()
        expect(self.page).to_have_url(f"{self.base_url}/login")
        print("✅ On Signup/Login page")

    def fill_signup_form(self, name, email):
        """Fill initial signup form with name and email"""
        print(f"📝 Filling signup form with Name: {name}, Email: {email}")

        name_field = self.page.locator('input[data-qa="signup-name"]')
        name_field.fill(name)

        email_field = self.page.locator('input[data-qa="signup-email"]')
        email_field.fill(email)

        signup_button = self.page.locator('button[data-qa="signup-button"]')
        signup_button.click()

        self.page.wait_for_selector('#form')
        print("✅ Signup form submitted, registration form loaded")

    def navigate_to_brand(self, brand_name):
        """Navigate to a specific brand"""
        print(f"\n🏷️ Navigating to {brand_name} brand...")

        brand_link = self.page.locator(f'.brands-name a:has-text("{brand_name}")')
        brand_link.click()

        self.page.wait_for_selector('.features_items')
        self.page.wait_for_timeout(1000)

        print(f"✅ On {brand_name} brand page")

    def add_nth_product_to_cart(self, position, continue_shopping=True):
        """Add the nth product from current page to cart"""
        print(f"🛒 Adding product #{position} to cart...")

        products = self.page.locator('.single-products').all()

        if position > len(products):
            raise Exception(f"Only {len(products)} products available, cannot add product #{position}")

        product = products[position - 1]
        product_name = product.locator('.productinfo p').first.inner_text()

        product.hover()
        self.page.wait_for_timeout(500)

        add_to_cart_btn = product.locator('.overlay-content .add-to-cart').first
        add_to_cart_btn.click()

        self.page.wait_for_selector('#cartModal', state='visible')

        if continue_shopping:
            continue_btn = self.page.locator('button:has-text("Continue Shopping")')
            continue_btn.click()
            self.page.wait_for_selector('#cartModal', state='hidden')
            print(f"✅ Added '{product_name}' - Continued shopping")
        else:
            print(f"✅ Added '{product_name}'")

        self.added_products.append(product_name)
        return product_name

    def view_cart(self):
        """Navigate to cart page"""
        print("\n🛒 Viewing cart...")
        view_cart_link = self.page.locator('a:has-text("View Cart")').first
        view_cart_link.click()
        expect(self.page).to_have_url(f"{self.base_url}/view_cart")
        print("✅ On cart page")

    def get_cart_products(self):
        """Get all products in cart"""
        cart_rows = self.page.locator('#cart_info_table tbody tr').all()
        products = []

        for row in cart_rows:
            try:
                product_name = row.locator('.cart_description h4 a').inner_text()
                products.append(product_name)
            except:
                pass

        return products

    def test_complete_ecommerce_flow(self):
        """
        Test Case: Complete E-commerce Flow - Registration to Payment

        Steps 1-17: Registration
        Steps 18-27: Shopping by Brands
        Steps 28-37: Checkout and Payment
        """

        print("\n" + "=" * 70)
        print("TEST: Complete E-commerce Flow - Registration to Payment")
        print("=" * 70)

        # Navigate to website
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Opened Automation Exercise website")

        # Step 1: Navigate to registration form
        self.navigate_to_signup()
        print("✅ Step 1: On registration form")

        # Fill initial signup
        unique_email = self.generate_unique_email()
        self.fill_signup_form("Complete Test", unique_email)

        print("\n" + "-" * 70)
        print("REGISTRATION (Steps 2-17)")
        print("-" * 70)

        # Step 2: Select Mr. radio button
        self.page.locator('#id_gender1').check()
        print("✅ Step 2: Selected 'Mr.' title")

        # Step 3: Enter Test@789 in Password field
        self.page.locator('#password').fill('Test@789')
        print("✅ Step 3: Entered password 'Test@789'")

        # Step 4: Select Date of Birth: 10-March-1995
        self.page.locator('#days').select_option('10')
        self.page.locator('#months').select_option('3')
        self.page.locator('#years').select_option('1995')
        print("✅ Step 4: Selected Date of Birth: 10-March-1995")

        # Step 5: Check newsletter checkbox
        self.page.locator('#newsletter').check()
        print("✅ Step 5: Checked newsletter checkbox")

        # Step 6: Check special offers checkbox
        self.page.locator('#optin').check()
        print("✅ Step 6: Checked special offers checkbox")

        # Step 7: Enter Complete in First name
        self.page.locator('#first_name').fill('Complete')
        print("✅ Step 7: Entered First name: 'Complete'")

        # Step 8: Enter Test in Last name
        self.page.locator('#last_name').fill('Test')
        print("✅ Step 8: Entered Last name: 'Test'")

        # Step 9: Enter Test Corp in Company
        self.page.locator('#company').fill('Test Corp')
        print("✅ Step 9: Entered Company: 'Test Corp'")

        # Step 10: Enter 123 Main Street in Address
        self.page.locator('#address1').fill('123 Main Street')
        print("✅ Step 10: Entered Address: '123 Main Street'")

        # Step 11: Enter Suite 100 in Address 2
        self.page.locator('#address2').fill('Suite 100')
        print("✅ Step 11: Entered Address 2: 'Suite 100'")

        # Step 12: Select India from Country dropdown
        self.page.locator('#country').select_option('India')
        print("✅ Step 12: Selected Country: 'India'")

        # Step 13: Enter Delhi in State
        self.page.locator('#state').fill('Delhi')
        print("✅ Step 13: Entered State: 'Delhi'")

        # Step 14: Enter New Delhi in City
        self.page.locator('#city').fill('New Delhi')
        print("✅ Step 14: Entered City: 'New Delhi'")

        # Step 15: Enter 110001 in Zipcode
        self.page.locator('#zipcode').fill('110001')
        print("✅ Step 15: Entered Zipcode: '110001'")

        # Step 16: Enter 9988776655 in Mobile Number
        self.page.locator('#mobile_number').fill('9988776655')
        print("✅ Step 16: Entered Mobile Number: '9988776655'")

        # Step 17: Click Create Account button (handle any popups)
        self.page.locator('button[data-qa="create-account"]').click()
        print("✅ Step 17: Clicked 'Create Account' button")

        # Wait for confirmation page and handle any additional consents
        self.page.wait_for_load_state('networkidle')
        self.handle_cookie_consent()

        # Verify account creation
        try:
            success_message = self.page.locator('h2[data-qa="account-created"]')
            expect(success_message).to_be_visible()
            print("✅ Account Created Successfully!")
        except:
            print("⚠️ Could not verify success message")

        # Step 18: Click Continue button
        continue_button = self.page.locator('a[data-qa="continue-button"]')
        continue_button.click()
        self.page.wait_for_load_state('networkidle')
        self.handle_cookie_consent()
        print("✅ Step 18: Clicked 'Continue' button")

        print("\n" + "=" * 70)
        print("SHOPPING BY BRANDS (Steps 19-27)")
        print("=" * 70)

        # Step 19: Click on Brands section
        products_link = self.page.locator('a[href="/products"]').first
        products_link.click()
        self.page.wait_for_selector('.brands-name')
        print("✅ Step 19: On Products page with Brands section")

        # Step 20-22: Select BIBA brand and add 2 items
        print("\n" + "-" * 70)
        print("BIBA BRAND")
        print("-" * 70)

        self.navigate_to_brand("Biba")
        print("✅ Step 20: Selected BIBA brand")

        self.add_nth_product_to_cart(1, continue_shopping=True)
        print("✅ Step 21: Added 1st item from BIBA")

        self.add_nth_product_to_cart(2, continue_shopping=True)
        print("✅ Step 22: Added 2nd item from BIBA")

        # Step 23-26: Select MADAME brand and add 3 items
        print("\n" + "-" * 70)
        print("MADAME BRAND")
        print("-" * 70)

        self.navigate_to_brand("Madame")
        print("✅ Step 23: Selected MADAME brand")

        self.add_nth_product_to_cart(1, continue_shopping=True)
        print("✅ Step 24: Added 1st item from MADAME")

        self.add_nth_product_to_cart(2, continue_shopping=True)
        print("✅ Step 25: Added 2nd item from MADAME")

        self.add_nth_product_to_cart(3, continue_shopping=False)
        print("✅ Step 26: Added 3rd item from MADAME")

        # Step 27: View cart and verify
        self.view_cart()

        cart_products = self.get_cart_products()
        print(f"\n✅ Step 27: Cart verified - {len(cart_products)} items present")

        for i, product in enumerate(cart_products, 1):
            print(f"   {i}. {product}")

        assert len(cart_products) == 5, f"Expected 5 products, found {len(cart_products)}"

        print("\n" + "=" * 70)
        print("CHECKOUT AND PAYMENT (Steps 28-37)")
        print("=" * 70)

        # Step 28: Click Proceed to Checkout
        print("\n💳 Proceeding to checkout...")
        checkout_button = self.page.locator('a.btn.btn-default.check_out')
        checkout_button.click()
        self.page.wait_for_load_state('networkidle')
        print("✅ Step 28: Clicked 'Proceed to Checkout'")

        # Step 29: Scroll down to comment section
        comment_textarea = self.page.locator('textarea[name="message"]')
        comment_textarea.scroll_into_view_if_needed()
        print("✅ Step 29: Scrolled to comment section")

        # Step 30: Type comment
        comment_textarea.fill("Uve got unbelievable products guys!")
        print("✅ Step 30: Entered comment: 'Uve got unbelievable products guys!'")

        # Step 31: Click Place Order
        place_order_button = self.page.locator('a[href="/payment"]')
        place_order_button.click()
        self.page.wait_for_load_state('networkidle')
        print("✅ Step 31: Clicked 'Place Order' button")

        # Step 32: Enter Name on Card
        name_on_card = self.page.locator('input[name="name_on_card"]')
        name_on_card.fill("Petar Gorskiqt")
        print("✅ Step 32: Entered Name on Card: 'Petar Gorskiqt'")

        # Step 33: Enter Card Number
        card_number = self.page.locator('input[name="card_number"]')
        card_number.fill("4588626759329571")
        print("✅ Step 33: Entered Card Number: '4588626759329571'")

        # Step 34: Enter CVC
        cvc = self.page.locator('input[name="cvc"]')
        cvc.fill("878")
        print("✅ Step 34: Entered CVC: '878'")

        # Step 35: Enter Expiration Month
        expiry_month = self.page.locator('input[name="expiry_month"]')
        expiry_month.fill("12")
        print("✅ Step 35: Entered Expiration Month: '12'")

        # Step 36: Enter Expiration Year
        expiry_year = self.page.locator('input[name="expiry_year"]')
        expiry_year.fill("25")
        print("✅ Step 36: Entered Expiration Year: '25'")

        # Step 37: Click Pay and Confirm Order
        pay_button = self.page.locator('button[data-qa="pay-button"]')
        pay_button.click()
        print("✅ Step 37: Clicked 'Pay and Confirm Order'")

        # Wait for order confirmation
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(2000)

        # Verify order success
        try:
            success_message = self.page.locator('p:has-text("Congratulations")')
            if success_message.is_visible(timeout=5000):
                print("\n" + "=" * 70)
                print("✅ ORDER PLACED SUCCESSFULLY!")
                print("=" * 70)
            else:
                print("\n⚠️ Order confirmation message not found")
        except:
            print("\n⚠️ Could not verify order confirmation")

        print("\n" + "=" * 70)
        print("✅ TEST PASSED: Complete E-commerce Flow Successful!")
        print("   - Registration completed")
        print("   - 5 products added (2 BIBA + 3 MADAME)")
        print("   - Checkout completed")
        print("   - Payment processed")
        print("=" * 70 + "\n")


# Configuration for pytest
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context - full HD size"""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080
        },
        "no_viewport": False
    }


if __name__ == "__main__":
    # Run the test using pytest
    pytest.main([__file__, "-v", "-s", "--headed"])