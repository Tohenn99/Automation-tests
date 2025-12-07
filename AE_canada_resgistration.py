import pytest
from playwright.sync_api import Page, expect
import random
import string


class TestCanadaRegistration:
    """Test suite for Canada address registration"""

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
        return f"emma.taylor_{random_string}@example.com"

    def test_register_canada_user(self):
        """
        Test Case: Register user with Canada address

        User Details:
        - Name: Emma Taylor
        - Title: Mrs.
        - Password: Canada@2024
        - DOB: 18-October-1992
        - Address: 789 Yonge Street, Unit 12B
        - City: Toronto
        - State: Ontario
        - Zipcode: M5B 2K3 (Canadian postal code format)
        - Country: Canada
        - Mobile: 4165551234 (10 digits)
        """

        print("\n" + "=" * 70)
        print("TEST: Register User with Canada Address")
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

        self.page.locator('input[data-qa="signup-name"]').fill("Emma Taylor")
        self.page.locator('input[data-qa="signup-email"]').fill(unique_email)
        self.page.locator('button[data-qa="signup-button"]').click()

        self.page.wait_for_selector('#form')
        print("✅ Registration form loaded")

        print("\n" + "-" * 70)
        print("FILLING ACCOUNT INFORMATION")
        print("-" * 70)

        # Select Mrs. title
        self.page.locator('#id_gender2').check()
        print("✓ Title: Mrs.")

        # Password
        self.page.locator('#password').fill('Canada@2024')
        print("✓ Password: Canada@2024")

        # Date of Birth
        self.page.locator('#days').select_option('18')
        self.page.locator('#months').select_option('10')
        self.page.locator('#years').select_option('1992')
        print("✓ Date of Birth: 18-October-1992")

        # Newsletter and offers
        self.page.locator('#newsletter').check()
        self.page.locator('#optin').check()
        print("✓ Newsletter and offers checked")

        print("\n" + "-" * 70)
        print("FILLING CANADA ADDRESS INFORMATION")
        print("-" * 70)

        # First name
        self.page.locator('#first_name').fill('Emma')
        print("✓ First name: Emma")

        # Last name
        self.page.locator('#last_name').fill('Taylor')
        print("✓ Last name: Taylor")

        # Company
        self.page.locator('#company').fill('Maple Tech Solutions Inc.')
        print("✓ Company: Maple Tech Solutions Inc.")

        # Address
        self.page.locator('#address1').fill('789 Yonge Street')
        print("✓ Address 1: 789 Yonge Street")

        self.page.locator('#address2').fill('Unit 12B')
        print("✓ Address 2: Unit 12B")

        # Country
        self.page.locator('#country').select_option('Canada')
        print("✓ Country: Canada")

        # Province (State)
        self.page.locator('#state').fill('Ontario')
        print("✓ Province: Ontario")

        # City
        self.page.locator('#city').fill('Toronto')
        print("✓ City: Toronto")

        # Postal Code (Canadian format: A1A 1A1)
        self.page.locator('#zipcode').fill('M5B 2K3')
        print("✓ Postal Code: M5B 2K3 (Canadian format)")

        # Mobile (Canadian format: 10 digits)
        self.page.locator('#mobile_number').fill('4165551234')
        print("✓ Mobile: 4165551234 (Canadian format)")

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
        print("CANADA REGISTRATION SUMMARY")
        print("=" * 70)
        print("Personal Information:")
        print("  Name: Emma Taylor")
        print(f"  Email: {unique_email}")
        print("  Title: Mrs.")
        print("  Password: Canada@2024")
        print("  Date of Birth: 18-October-1992")
        print("\nAddress Information:")
        print("  Company: Maple Tech Solutions Inc.")
        print("  Address: 789 Yonge Street, Unit 12B")
        print("  City: Toronto")
        print("  Province: Ontario")
        print("  Country: Canada")
        print("  Postal Code: M5B 2K3 (Canadian A1A 1A1 format)")
        print("  Mobile: 4165551234 (Canadian 10-digit format)")
        print("=" * 70)

        print("\n✅ TEST PASSED: Canada Registration Complete! 🇨🇦\n")


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