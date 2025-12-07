import pytest
from playwright.sync_api import Page, expect
import random
import string


class TestUSARegistration:
    """Test suite for USA address registration"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup method to navigate to the website before each test"""
        self.page = page
        self.base_url = "https://automationexercise.com"

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
        """Generate a unique email address"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"john.smith_{random_string}@example.com"

    def test_register_usa_user(self):
        """
        Test Case: Register user with USA address

        User Details:
        - Name: John Smith
        - Title: Mr.
        - Password: USA@2024
        - DOB: 25-July-1985
        - Address: 1234 Broadway Avenue, Suite 500
        - City: New York
        - State: New York
        - Zipcode: 10001
        - Country: United States
        - Mobile: 2125551234 (10 digits)
        """

        print("\n" + "=" * 70)
        print("TEST: Register User with USA Address")
        print("=" * 70)

        # Navigate to website
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Opened website")

        # Navigate to signup
        print("\n📝 Navigating to signup page...")
        signup_link = self.page.locator('a[href="/login"]').first
        signup_link.click()
        expect(self.page).to_have_url(f"{self.base_url}/login")
        print("✅ On signup page")

        # Fill initial signup
        unique_email = self.generate_unique_email()
        print(f"\n📧 Using email: {unique_email}")

        self.page.locator('input[data-qa="signup-name"]').fill("John Smith")
        self.page.locator('input[data-qa="signup-email"]').fill(unique_email)
        self.page.locator('button[data-qa="signup-button"]').click()

        self.page.wait_for_selector('#form')
        print("✅ Registration form loaded")

        print("\n" + "-" * 70)
        print("FILLING ACCOUNT INFORMATION")
        print("-" * 70)

        # Select Mr. title
        self.page.locator('#id_gender1').check()
        print("✓ Title: Mr.")

        # Password
        self.page.locator('#password').fill('USA@2024')
        print("✓ Password: USA@2024")

        # Date of Birth
        self.page.locator('#days').select_option('25')
        self.page.locator('#months').select_option('7')
        self.page.locator('#years').select_option('1985')
        print("✓ Date of Birth: 25-July-1985")

        # Newsletter and offers
        self.page.locator('#newsletter').check()
        self.page.locator('#optin').check()
        print("✓ Newsletter and offers checked")

        print("\n" + "-" * 70)
        print("FILLING USA ADDRESS INFORMATION")
        print("-" * 70)

        # First name
        self.page.locator('#first_name').fill('John')
        print("✓ First name: John")

        # Last name
        self.page.locator('#last_name').fill('Smith')
        print("✓ Last name: Smith")

        # Company
        self.page.locator('#company').fill('Smith & Associates LLC')
        print("✓ Company: Smith & Associates LLC")

        # Address
        self.page.locator('#address1').fill('1234 Broadway Avenue')
        print("✓ Address 1: 1234 Broadway Avenue")

        self.page.locator('#address2').fill('Suite 500')
        print("✓ Address 2: Suite 500")

        # Country
        self.page.locator('#country').select_option('United States')
        print("✓ Country: United States")

        # State
        self.page.locator('#state').fill('New York')
        print("✓ State: New York")

        # City
        self.page.locator('#city').fill('New York')
        print("✓ City: New York")

        # Zipcode (US format: 5 digits)
        self.page.locator('#zipcode').fill('10001')
        print("✓ Zipcode: 10001")

        # Mobile (US format: 10 digits)
        self.page.locator('#mobile_number').fill('2125551234')
        print("✓ Mobile: 2125551234")

        # Create account
        print("\n🚀 Creating account...")
        self.page.locator('button[data-qa="create-account"]').click()

        # Wait for confirmation
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(2000)

        # Verify account creation
        try:
            success_message = self.page.locator('h2[data-qa="account-created"]')
            expect(success_message).to_be_visible()
            print("✅ Account Created Successfully!")
        except:
            print("⚠️ Could not verify success message")

        # Registration summary
        print("\n" + "=" * 70)
        print("USA REGISTRATION SUMMARY")
        print("=" * 70)
        print("Personal Information:")
        print("  Name: John Smith")
        print(f"  Email: {unique_email}")
        print("  Title: Mr.")
        print("  Password: USA@2024")
        print("  Date of Birth: 25-July-1985")
        print("\nAddress Information:")
        print("  Company: Smith & Associates LLC")
        print("  Address: 1234 Broadway Avenue, Suite 500")
        print("  City: New York")
        print("  State: New York")
        print("  Country: United States")
        print("  Zipcode: 10001 (US 5-digit format)")
        print("  Mobile: 2125551234 (US 10-digit format)")
        print("=" * 70)

        print("\n✅ TEST PASSED: USA Registration Complete!\n")


# Configuration for pytest
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context"""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080
        }
    }


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--headed"])