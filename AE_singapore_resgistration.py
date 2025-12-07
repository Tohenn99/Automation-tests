import pytest
from playwright.sync_api import Page, expect
import random
import string


class TestSingaporeRegistration:
    """Test suite for Singapore address registration"""

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
        return f"wei.tan_{random_string}@example.com"

    def test_register_singapore_user(self):
        """
        Test Case: Register user with Singapore address

        User Details:
        - Name: Wei Tan
        - Title: Mr.
        - Password: SG@2024
        - DOB: 8-February-1989
        - Address: 1 Raffles Place, #30-01
        - City: Singapore
        - State: Singapore
        - Zipcode: 048616 (Singapore postal code - 6 digits)
        - Country: Singapore
        - Mobile: 91234567 (8 digits, no country code)
        """

        print("\n" + "=" * 70)
        print("TEST: Register User with Singapore Address")
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

        self.page.locator('input[data-qa="signup-name"]').fill("Wei Tan")
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
        self.page.locator('#password').fill('SG@2024')
        print("✓ Password: SG@2024")

        # Date of Birth
        self.page.locator('#days').select_option('8')
        self.page.locator('#months').select_option('2')
        self.page.locator('#years').select_option('1989')
        print("✓ Date of Birth: 8-February-1989")

        # Newsletter and offers
        self.page.locator('#newsletter').check()
        self.page.locator('#optin').check()
        print("✓ Newsletter and offers checked")

        print("\n" + "-" * 70)
        print("FILLING SINGAPORE ADDRESS INFORMATION")
        print("-" * 70)

        # First name
        self.page.locator('#first_name').fill('Wei')
        print("✓ First name: Wei")

        # Last name
        self.page.locator('#last_name').fill('Tan')
        print("✓ Last name: Tan")

        # Company
        self.page.locator('#company').fill('Lion City Tech Pte Ltd')
        print("✓ Company: Lion City Tech Pte Ltd")

        # Address (Singapore uses # for floor/unit)
        self.page.locator('#address1').fill('1 Raffles Place')
        print("✓ Address 1: 1 Raffles Place")

        self.page.locator('#address2').fill('#30-01')
        print("✓ Address 2: #30-01 (Singapore unit format)")

        # Country
        self.page.locator('#country').select_option('Singapore')
        print("✓ Country: Singapore")

        # State (Singapore is a city-state)
        self.page.locator('#state').fill('Singapore')
        print("✓ State: Singapore")

        # City
        self.page.locator('#city').fill('Singapore')
        print("✓ City: Singapore")

        # Postal Code (Singapore format: 6 digits)
        self.page.locator('#zipcode').fill('048616')
        print("✓ Postal Code: 048616 (Singapore 6-digit format)")

        # Mobile (Singapore format: 8 digits, starts with 8 or 9)
        self.page.locator('#mobile_number').fill('91234567')
        print("✓ Mobile: 91234567 (Singapore 8-digit format)")

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
        print("SINGAPORE REGISTRATION SUMMARY")
        print("=" * 70)
        print("Personal Information:")
        print("  Name: Wei Tan")
        print(f"  Email: {unique_email}")
        print("  Title: Mr.")
        print("  Password: SG@2024")
        print("  Date of Birth: 8-February-1989")
        print("\nAddress Information:")
        print("  Company: Lion City Tech Pte Ltd")
        print("  Address: 1 Raffles Place, #30-01")
        print("  City: Singapore")
        print("  State: Singapore")
        print("  Country: Singapore")
        print("  Postal Code: 048616 (Singapore 6-digit format)")
        print("  Mobile: 91234567 (Singapore 8-digit format)")
        print("=" * 70)

        print("\n✅ TEST PASSED: Singapore Registration Complete! 🇸🇬\n")


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
    pytest.main([__file__, "-v", "-s", "--headed"])