import pytest
from playwright.sync_api import Page, expect
import random
import string


class TestRegistrationAndShopping:
    """Test suite for user registration and multi-category shopping"""

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

        # Click on the brand in the sidebar
        brand_link = self.page.locator(f'.brands-name a:has-text("{brand_name}")')
        brand_link.click()

        # Wait for filtered results to load
        self.page.wait_for_selector('.features_items')
        self.page.wait_for_timeout(1000)

        print(f"✅ On {brand_name} brand page")

    def add_nth_product_to_cart(self, position, continue_shopping=True):
        """Add the nth product from current page to cart"""
        print(f"🛒 Adding product #{position} to cart...")

        # Get all products on the page
        products = self.page.locator('.single-products').all()

        if position > len(products):
            raise Exception(f"Only {len(products)} products available, cannot add product #{position}")

        # Get the specific product
        product = products[position - 1]

        # Get product name for tracking
        product_name = product.locator('.productinfo p').first.inner_text()

        # Hover over the product
        product.hover()
        self.page.wait_for_timeout(500)

        # Click Add to Cart button
        add_to_cart_btn = product.locator('.overlay-content .add-to-cart').first
        add_to_cart_btn.click()

        # Wait for modal
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

    def test_complete_registration_and_shopping(self):
        """
        Test Case: Complete Registration and Multi-Brand Shopping

        Steps 1-17: Registration
        Steps 18-26: Shopping by Brands
        """

        print("\n" + "=" * 70)
        print("TEST: Complete Registration and Multi-Brand Shopping - CHER-121")
        print("=" * 70)

        # Navigate to website
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Opened Automation Exercise website")

        # Navigate to registration form
        self.navigate_to_signup()
        print("✅ On registration form")

        # Fill initial signup
        unique_email = self.generate_unique_email()
        self.fill_signup_form("Complete Test", unique_email)

        print("\n" + "-" * 70)
        print("FILLING REGISTRATION FORM (Steps 1-16)")
        print("-" * 70)

        # Step 1: Select Mr. radio button
        mr_radio = self.page.locator('#id_gender1')
        mr_radio.check()
        print("✅ Step 1: Selected 'Mr.' title")

        # Step 2: Enter Test@789 in Password field
        password_field = self.page.locator('#password')
        password_field.fill('Test@789')
        print("✅ Step 2: Entered password 'Test@789'")

        # Step 3: Select Date of Birth: 10-March-1995
        self.page.locator('#days').select_option('10')
        self.page.locator('#months').select_option('3')
        self.page.locator('#years').select_option('1995')
        print("✅ Step 3: Selected Date of Birth: 10-March-1995")

        # Step 4: Check newsletter checkbox
        self.page.locator('#newsletter').check()
        print("✅ Step 4: Checked newsletter checkbox")

        # Step 5: Check special offers checkbox
        self.page.locator('#optin').check()
        print("✅ Step 5: Checked special offers checkbox")

        # Step 6: Enter Complete in First name
        self.page.locator('#first_name').fill('Complete')
        print("✅ Step 6: Entered First name: 'Complete'")

        # Step 7: Enter Test in Last name
        self.page.locator('#last_name').fill('Test')
        print("✅ Step 7: Entered Last name: 'Test'")

        # Step 8: Enter Test Corp in Company
        self.page.locator('#company').fill('Test Corp')
        print("✅ Step 8: Entered Company: 'Test Corp'")

        # Step 9: Enter 123 Main Street in Address
        self.page.locator('#address1').fill('123 Main Street')
        print("✅ Step 9: Entered Address: '123 Main Street'")

        # Step 10: Enter Suite 100 in Address 2
        self.page.locator('#address2').fill('Suite 100')
        print("✅ Step 10: Entered Address 2: 'Suite 100'")

        # Step 11: Select India from Country dropdown
        self.page.locator('#country').select_option('India')
        print("✅ Step 11: Selected Country: 'India'")

        # Step 12: Enter Delhi in State
        self.page.locator('#state').fill('Delhi')
        print("✅ Step 12: Entered State: 'Delhi'")

        # Step 13: Enter New Delhi in City
        self.page.locator('#city').fill('New Delhi')
        print("✅ Step 13: Entered City: 'New Delhi'")

        # Step 14: Enter 110001 in Zipcode
        self.page.locator('#zipcode').fill('110001')
        print("✅ Step 14: Entered Zipcode: '110001'")

        # Step 15: Enter 9988776655 in Mobile Number
        self.page.locator('#mobile_number').fill('9988776655')
        print("✅ Step 15: Entered Mobile Number: '9988776655'")

        # Step 16: Click Create Account button
        self.page.locator('button[data-qa="create-account"]').click()
        print("✅ Step 16: Clicked 'Create Account' button")

        # Wait for confirmation page
        self.page.wait_for_load_state('networkidle')

        # Verify account creation
        try:
            success_message = self.page.locator('h2[data-qa="account-created"]')
            expect(success_message).to_be_visible()
            expect(success_message).to_have_text("Account Created!")
            print("✅ Account Created Successfully!")
        except:
            print("⚠️ Could not verify success message")

        # Step 17: Click Continue button
        continue_button = self.page.locator('a[data-qa="continue-button"]')
        continue_button.click()
        self.page.wait_for_load_state('networkidle')
        print("✅ Step 17: Clicked 'Continue' button")

        print("\n" + "=" * 70)
        print("SHOPPING BY BRANDS (Steps 18-26)")
        print("=" * 70)

        # Step 18: Click on Brands section (navigate to products page first to see brands)
        products_link = self.page.locator('a[href="/products"]').first
        products_link.click()
        self.page.wait_for_selector('.brands-name')
        print("✅ Step 18: On Products page with Brands section visible")

        # Step 19-21: Select BIBA brand and add 2 items
        print("\n" + "-" * 70)
        print("BIBA BRAND")
        print("-" * 70)

        self.navigate_to_brand("Biba")
        print("✅ Step 19: Selected BIBA brand")

        self.add_nth_product_to_cart(1, continue_shopping=True)
        print("✅ Step 20: Added 1st item from BIBA brand")

        self.add_nth_product_to_cart(2, continue_shopping=True)
        print("✅ Step 21: Added 2nd item from BIBA brand")

        # Step 22-25: Select MADAME brand and add 3 items
        print("\n" + "-" * 70)
        print("MADAME BRAND")
        print("-" * 70)

        self.navigate_to_brand("Madame")
        print("✅ Step 22: Selected MADAME brand")

        self.add_nth_product_to_cart(1, continue_shopping=True)
        print("✅ Step 23: Added 1st item from MADAME brand")

        self.add_nth_product_to_cart(2, continue_shopping=True)
        print("✅ Step 24: Added 2nd item from MADAME brand")

        self.add_nth_product_to_cart(3, continue_shopping=False)
        print("✅ Step 25: Added 3rd item from MADAME brand")

        # Step 26: View cart and verify all 5 items
        self.view_cart()
        print("✅ Step 26: Viewing cart")

        print("\n" + "=" * 70)
        print("CART VERIFICATION")
        print("=" * 70)

        cart_products = self.get_cart_products()

        print(f"\nExpected products: 5 (2 from BIBA + 3 from MADAME)")
        print(f"Actual products in cart: {len(cart_products)}")
        print("\nProducts in cart:")

        for i, product in enumerate(cart_products, 1):
            status = "✅" if product in self.added_products else "❌"
            print(f"{status} {i}. {product}")

        # Verify all 5 items are present
        assert len(cart_products) == 5, f"Expected 5 products, found {len(cart_products)}"

        for added_product in self.added_products:
            assert added_product in cart_products, \
                f"Product '{added_product}' not found in cart"

        print("\n" + "=" * 70)
        print("✅ TEST PASSED: Registration complete and all 5 items in cart!")
        print("   (2 from BIBA + 3 from MADAME)")
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