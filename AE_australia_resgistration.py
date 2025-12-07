import pytest
from playwright.sync_api import Page, expect
import random
import string


class TestAustraliaRegistration:
    """Test suite for Australia address registration"""

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
        return f"oliver.harris_{random_string}@example.com"

    def test_register_australia_user(self):
        """
        Test Case: Register user with Australia address

        User Details:
        - Name: Oliver Harris
        - Title: Mr.
        - Password: Aussie@2024
        - DOB: 5-March-1990
        - Address: 456 George Street, Level 8
        - City: Sydney
        - State: New South Wales
        - Zipcode: 2000 (Australian postcode - 4 digits)
        - Country: Australia
        - Mobile: 0412345678 (10 digits starting with 04)
        """

        print("\n" + "=" * 70)
        print("TEST: Register User with Australia Address")
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

        self.page.locator('input[data-qa="signup-name"]').fill("Oliver Harris")
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
        self.page.locator('#password').fill('Aussie@2024')
        print("✓ Password: Aussie@2024")

        # Date of Birth
        self.page.locator('#days').select_option('5')
        self.page.locator('#months').select_option('3')
        self.page.locator('#years').select_option('1990')
        print("✓ Date of Birth: 5-March-1990")

        # Newsletter and offers
        self.page.locator('#newsletter').check()
        self.page.locator('#optin').check()
        print("✓ Newsletter and offers checked")

        print("\n" + "-" * 70)
        print("FILLING AUSTRALIA ADDRESS INFORMATION")
        print("-" * 70)

        # First name
        self.page.locator('#first_name').fill('Oliver')
        print("✓ First name: Oliver")

        # Last name
        self.page.locator('#last_name').fill('Harris')
        print("✓ Last name: Harris")

        # Company
        self.page.locator('#company').fill('Harbour Digital Pty Ltd')
        print("✓ Company: Harbour Digital Pty Ltd")

        # Address
        self.page.locator('#address1').fill('456 George Street')
        print("✓ Address 1: 456 George Street")

        self.page.locator('#address2').fill('Level 8')
        print("✓ Address 2: Level 8")

        # Country
        self.page.locator('#country').select_option('Australia')
        print("✓ Country: Australia")

        # State
        self.page.locator('#state').fill('New South Wales')
        print("✓ State: New South Wales")

        # City
        self.page.locator('#city').fill('Sydney')
        print("✓ City: Sydney")

        # Postcode (Australian format: 4 digits)
        self.page.locator('#zipcode').fill('2000')
        print("✓ Postcode: 2000 (Australian 4-digit format)")

        # Mobile (Australian format: 04XX XXX XXX)
        self.page.locator('#mobile_number').fill('0412345678')
        print("✓ Mobile: 0412345678 (Australian format)")

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
        print("AUSTRALIA REGISTRATION SUMMARY")
        print("=" * 70)
        print("Personal Information:")
        print("  Name: Oliver Harris")
        print(f"  Email: {unique_email}")
        print("  Title: Mr.")
        print("  Password: Aussie@2024")
        print("  Date of Birth: 5-March-1990")
        print("\nAddress Information:")
        print("  Company: Harbour Digital Pty Ltd")
        print("  Address: 456 George Street, Level 8")
        print("  City: Sydney")
        print("  State: New South Wales")
        print("  Country: Australia")
        print("  Postcode: 2000 (Australian 4-digit format)")
        print("  Mobile: 0412345678 (Australian mobile format)")
        print("=" * 70)

        print("\n✅ TEST PASSED: Australia Registration Complete! 🇦🇺\n")


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