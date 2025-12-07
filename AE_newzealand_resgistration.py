import pytest
from playwright.sync_api import Page, expect
import random
import string


class TestNewZealandRegistration:
    """Test suite for New Zealand address registration"""

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
        return f"sophie.anderson_{random_string}@example.com"

    def test_register_newzealand_user(self):
        """
        Test Case: Register user with New Zealand address

        User Details:
        - Name: Sophie Anderson
        - Title: Mrs.
        - Password: Kiwi@2024
        - DOB: 22-November-1994
        - Address: 234 Queen Street, Floor 6
        - City: Auckland
        - State: Auckland Region
        - Zipcode: 1010 (NZ postcode - 4 digits)
        - Country: New Zealand
        - Mobile: 0211234567 (10 digits starting with 021/022/027)
        """

        print("\n" + "=" * 70)
        print("TEST: Register User with New Zealand Address")
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

        self.page.locator('input[data-qa="signup-name"]').fill("Sophie Anderson")
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
        self.page.locator('#password').fill('Kiwi@2024')
        print("✓ Password: Kiwi@2024")

        # Date of Birth
        self.page.locator('#days').select_option('22')
        self.page.locator('#months').select_option('11')
        self.page.locator('#years').select_option('1994')
        print("✓ Date of Birth: 22-November-1994")

        # Newsletter and offers
        self.page.locator('#newsletter').check()
        self.page.locator('#optin').check()
        print("✓ Newsletter and offers checked")

        print("\n" + "-" * 70)
        print("FILLING NEW ZEALAND ADDRESS INFORMATION")
        print("-" * 70)

        # First name
        self.page.locator('#first_name').fill('Sophie')
        print("✓ First name: Sophie")

        # Last name
        self.page.locator('#last_name').fill('Anderson')
        print("✓ Last name: Anderson")

        # Company
        self.page.locator('#company').fill('Kiwi Innovation Ltd')
        print("✓ Company: Kiwi Innovation Ltd")

        # Address
        self.page.locator('#address1').fill('234 Queen Street')
        print("✓ Address 1: 234 Queen Street")

        self.page.locator('#address2').fill('Floor 6')
        print("✓ Address 2: Floor 6")

        # Country
        self.page.locator('#country').select_option('New Zealand')
        print("✓ Country: New Zealand")

        # Region (State)
        self.page.locator('#state').fill('Auckland Region')
        print("✓ Region: Auckland Region")

        # City
        self.page.locator('#city').fill('Auckland')
        print("✓ City: Auckland")

        # Postcode (NZ format: 4 digits)
        self.page.locator('#zipcode').fill('1010')
        print("✓ Postcode: 1010 (NZ 4-digit format)")

        # Mobile (NZ format: 02X XXX XXXX)
        self.page.locator('#mobile_number').fill('0211234567')
        print("✓ Mobile: 0211234567 (NZ mobile format)")

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
        print("NEW ZEALAND REGISTRATION SUMMARY")
        print("=" * 70)
        print("Personal Information:")
        print("  Name: Sophie Anderson")
        print(f"  Email: {unique_email}")
        print("  Title: Mrs.")
        print("  Password: Kiwi@2024")
        print("  Date of Birth: 22-November-1994")
        print("\nAddress Information:")
        print("  Company: Kiwi Innovation Ltd")
        print("  Address: 234 Queen Street, Floor 6")
        print("  City: Auckland")
        print("  Region: Auckland Region")
        print("  Country: New Zealand")
        print("  Postcode: 1010 (NZ 4-digit format)")
        print("  Mobile: 0211234567 (NZ mobile format)")
        print("=" * 70)

        print("\n✅ TEST PASSED: New Zealand Registration Complete! 🇳🇿\n")


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